"""
Matrix declaration rules

Nodes
-----
Matrix : Matrix container
    Example: "[x;y]"
    Contains: Vector, ...

Vector : (Column)-Vector container
    Contains: Expr, ...
"""
from _code_block import Statement
import assign
import armadillo as arma


def Vector(node):
    """A (row-)vector
    """

    if node.value == "scalarsonly":
        return "", ", ", ""

    return reduce(lambda x,y: ("arma::join_rows(%s, %s)" % (x, y)), nodes)


def Matrix(node):

    # ensure all vectors in matrix same length
    m = len(node[0])
    if any([len(n)-m for n in node if n.value == "scalarsonly"]):
        shape = str([len(n) for n in node if n.value == "scalarsonly"])
        node.error("shape missmatch %s" % shape)

    # non-numerical elements in matrix
    if not node.num:
        return "{", ", ", "}"

    dims = {n.dim for n in node}

    # single vector with no content
    if len(node) == 1 and len(node[0]) == 0:
        node.num = False
        return "{", ", ", "}"

    # everything on scalarsonly form
    elif all([n.value for n in node]):

        # Inline matrices are moved to own lines
        if node.parent.cls not in ("Assign", "Statement") and \
                    node.parent.backend != "reserved":
            if node.parent.cls in ("Get", "Set") and node.mem != 0:
                if node.parent.type == "TYPE":
                    node.type = (node.dim, 3)
                else:
                    node.type = (node.dim, 0)
            return str(node.auxiliary())

        if node.parent.cls in ("Assign", "Statement"):
            node.parent.backend = "matrix"

        return "{", ", ", "}"


    # mix of scalars and colvecs
    elif dims in ({0,1}, {1}):

        # make string of each vector in matrix
        nodes = []
        for i in xrange(len(node)):

            # scalars must be converted first
            if node[i].value or node[i].dim == 0: # value=scalarsonly
                node[i].include("scol")
                nodes.append("m2cpp::scol(" + str(node[i]) + ")")

            else:
                nodes.append(str(node[i]))

    # mix of rowvecs and matrices
    elif dims in ({2}, {3}, {2,3}):

        # make string of each vector in matrix
        nodes = []
        for i in xrange(len(node)):
            
            # decomposed vectors should be moved to own lines
            if node[i].value:
                nodes.append(str(node[i].auxiliary()))
            else:
                nodes.append(str(node[i]))

    return reduce(lambda a,b: ("arma::join_cols(%s, %s)" % (a,b)), nodes)



def Assign(node):

    #left-hand-side, right-hand-side
    lhs, rhs = node

    assert rhs.cls in ("Matrix", "Cell")

    # no content in matrix
    if len(rhs[0]) == 0:
        return "%(0)s.reset() ;"

    # non-numerical values in matrix or variable assign
    if not lhs.num or not rhs.num:
        return "%(0)s = %(1)s ;"

    # new local variable 'ctype' contains convertion type
    node.type = node["ctype"] = node[0].type
    dim = node.dim
    node.dim = 0

    # decomposed matrix
    if rhs.value:

        type = node.type
        if type == "int":
            type = "sword"

        # scalar
        if rhs.dim == 0:
            return arma.scalar_assign(node)

        # colvec
        elif rhs.dim == 1:

            # save number of rows as 'rows'
            node["rows"] = len(node[1][0])*len(node[1])

            return type + " _" + node[0].name + " [] = %(1)s ;\n"+\
                "%(0)s = %(ctype)s(_" + node[0].name + ", %(rows)s, false) ;"

        # rowvec
        elif rhs.dim == 2:

            # save number of cols as 'cols'
            node["cols"] = len(node[1][0])*len(node[1])
            return type + " _" + node[0].name + " [] = %(1)s ;\n"+\
                "%(0)s = %(ctype)s(_" + node[0].name + ", %(cols)s, false) ;"

        # matrix
        elif rhs.dim == 3:
            # save number of rows and columns
            node["rows"] = len(node[1][0])
            node["cols"] = len(node[1])
            return type + " _" + node[0].name + " [] = %(1)s ;\n"+\
        "%(0)s = %(ctype)s(_" + node[0].name + ", %(rows)s, %(cols)s, false) ;"

        assert False

    else:
        node.dim = dim

    return assign.Assign(node)


Var = "%(name)s"

def Cell(node):

    # move inline cells to own lines
    if node.parent.cls not in ("Assign", "Assigns"):
        node.auxiliary()

    return "{", ", ", "}"
