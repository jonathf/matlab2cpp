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

    # dimensionality in vector
    dims = {n.dim for n in node}

    # non-numerical elements in vector
    if None in dims or [n for n in node if not n.num]:
        return "", ", ", ""

    # single element in vector
    if len(node) == 1:

        if dims == {0}:
            # holder value to determine if vector is in decomposed state
            node.value = "decomposed"
        else:
            node.value = ""

        node.dim = list(dims)[0]
        return "%(0)s"

    # only colvecs
    elif dims == {1}:
        node.value = ""
        node.dim = 1
        nodes = [str(n) for n in node]

    # Decomposed row
    if dims == {0}:
        node.value = "decomposed"
        node.dim = 2
        return "", ", ", ""

    # only rowvecs
    elif dims == {2}:

        node.value = "", ", ", ""
        node.dim = 2
        nodes = [str(n) for n in node]

    # mix of scalars and rowvecs
    elif dims == {0,2}:

        node.value = ""
        node.dim = 2

        nodes = []
        for i in xrange(len(node)):
            if node[i].dim == 0:
                node[i].include("srow")
                nodes.append("m2cpp::srow("+ str(node[i]) + ")")
            else:
                nodes.append(str(node[i]))


    # mix of matrices and colvecs
    elif dims in ({3}, {1,3}):

        node.value = ""
        node.dim = 3
        nodes = [str(n) for n in node]

    else:
        types = "{"+", ".join([n.type for n in node])+"}"
        node.error("Row-wise concatination trouble: %s" % types)
        nodes = [str(n) for n in node]

    node.value = ""
    if len(nodes) == 0:
        return ""

    elif len(nodes) == 1:
        return "%(0)s"

    return reduce(lambda x,y: ("arma::join_rows(%s, %s)" % (x, y)), nodes)


def Matrix(node):

    # ensure all vectors in matrix same length
    m = len(node[0])
    if any([len(n)-m for n in node if n.value == "decomposed"]):
        shape = str([len(n) for n in node if n.value == "decomposed"])
        node.error("shape missmatch %s" % shape)

    dims = {n.dim for n in node}

    # non-numerical elements in matrix
    if None in dims:
        return "[", ", ", "]"

    # single vector with no content
    if len(node) == 1 and len(node[0]) == 0:
        node.num = False
        return ""

    # everything on decomposed form
    elif all([n.value for n in node]):
        node.value = "decomposed"

        # set dimensions
        ax0, ax1 = len(node), len(node[0])
        if ax0 > 1:
            if ax1 > 1:
                node.dim = 3#matrix
            else:
                node.dim = 1#rowvec
        else:
            if ax1 > 1:
                node.dim = 2#colvec
            else:
                node.dim = 0#scalar

        # Inline matrices are moved to own lines
        if node.parent.cls not in ("Assign", "Statement") and \
                    node.parent.backend != "reserved":
            if node.parent.cls in ("Get", "Set") and node.mem != 0:
                node.type = (node.dim, 0)
            return str(node.auxiliary())

        if node.parent.cls in ("Assign", "Statement"):
            node.parent.backend = "matrix"

        return "{", ", ", "}"


    # only scalars in matrix
    # should be the same as decomposed form
    elif dims == {0}:

        # configure dimensions
        if len(node) > 1:
            if len(node[0]) > 1:
                node.dim = 3#matrix
            else:
                node.dim = 2#rowvec
        else:
            if len(node[0]) > 1:
                node.dim = 1#colvec
            else:
                node.dim = 0#scalar

        if node.parent.cls in ("Assign", "Statement"):
            node.parent.backend = "matrix"
            return ""
        if node.parent.cls in ("Get", "Set") and node.mem != 0:
            node.type = (node.dim, 0)
        return str(node.auxiliary())

    # mix of scalars and colvecs
    elif dims in ({0,1}, {1}):

        # configure dimensions
        if len(node[0])>1:
            node.dim = 3#matrix
        else:
            node.dim = 1#colvec

        # make string of each vector in matrix
        nodes = []
        for i in xrange(len(node)):

            # scalars must be converted first
            if node[i].value or node[i].dim == 0: # value=decomposed
                node[i].include("scol")
                nodes.append("m2cpp::scol(" + str(node[i]) + ")")

            else:
                nodes.append(str(node[i]))

    # mix of rowvecs and matrices
    elif dims in ({2}, {3}, {2,3}):

        # configure dimensiosn
        if dims == {2} and len(node)==1:
            node.dim = 2#rowvec
        else:
            node.dim = 3#matrix

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

            return type + " _%(0)s [] = %(1)s ;\n"+\
                    "%(0)s = %(ctype)s(_%(0)s, %(rows)s, false) ;"

        # rowvec
        elif rhs.dim == 2:

            # save number of cols as 'cols'
            node["cols"] = len(node[1][0])*len(node[1])
            return type + " _%(0)s [] = %(1)s ;\n"+\
                    "%(0)s = %(ctype)s(_%(0)s, %(cols)s, false) ;"

        # matrix
        elif rhs.dim == 3:
            # save number of rows and columns
            node["rows"] = len(node[1][0])
            node["cols"] = len(node[1])
            return type + " _%(0)s [] = %(1)s ;\n"+\
        "%(0)s = %(ctype)s(_%(0)s, %(rows)s, %(cols)s, false) ;"

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
