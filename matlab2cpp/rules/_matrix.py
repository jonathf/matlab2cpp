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
from ._code_block import Statement
from . import assign, armadillo as arma


def Vector(node):
    """A (row-)vector
    """

    if node.value == "scalarsonly":
        return "", ", ", ""

    if node.type == "string":
        return "", " + ", "" 

    nodes = map(str, node)

    #max mem in list and type list
    try:
        mem = max([int(n.mem) if n.num else -1 for n in node])
    except:
        mem = -1
    mem_type = ["uword", "sword", "float", "double", "cx_double"]
    
    #Join columns: a = [0, my_rowvec, b]
    for i in xrange(len(nodes)):
        # scalars must be converted first
        if node[i].value or node[i].dim == 0: # value=scalarsonly
            node[i].include("m2cpp")
            if mem != -1:
                nodes[i] = "m2cpp::srow<" + mem_type[mem] + ">(" + nodes[i] + ")"
            else:
                nodes[i] = "m2cpp::srow(" + nodes[i] + ")"

    if nodes:
        return reduce(lambda x,y: ("arma::join_rows(%s, %s)" % (x, y)), nodes)
    return ""


def Matrix(node):

    # ensure all vectors in matrix same length
    m = len(node[0])
    if any([len(n)-m for n in node if n.value == "scalarsonly"]):
        shape = str([len(n) for n in node if n.value == "scalarsonly"])
        node.error("shape missmatch %s" % shape)

    if node.type == "string":
        if len(node) > 1:
            return "", " + ", ""
        return "", " ", ""

    #clims in imagesc needs two {{ and }} for the python implementation
    if node.parent.name in ("imagesc", "wigb") and \
      len(node) == 1 and len(node[0]) > 1:
        if all([n.dim == 0 for n in node[0]]):
            return "{{", ", ", "}}"
        #{ } around arma::join_rows()
        return "{", ", ", "}"
        
    # non-numerical elements in matrix
    if not node.num:
        if len(node[0]) == 1 and node[0][0].cls == "Colon":
            return "", ", ", ""
        return "{", ", ", "}"

    dims = {n.dim for n in node}

    # single vector with no content
    if len(node) == 1 and len(node[0]) == 0:
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

        # if node.parent.cls in ("Assign", "Statement"):
        #     node.parent.backend = "matrix"

        return "{", ", ", "}"


    # mix of scalars and colvecs, scalar and matrix, scalar and vec and matrix
    elif dims in ({0,1}, {1}, {0,3}, {0,1,3}):

        # make string of each vector in matrix
        nodes = []
        for i in xrange(len(node)):

            #max mem in list and type list
            try:
                mem = max([int(n.mem) if n.num else -1 for n in node])
            except:
                mem = -1
            mem_type = ["uword", "sword", "float", "double", "cx_double"]
            
            # scalars must be converted first
            if node[i].value or node[i].dim == 0: # value=scalarsonly
                node[i].include("m2cpp")
                if mem != -1:
                    nodes.append("m2cpp::scol<" + mem_type[mem] + ">(" + str(node[i]) + ")")
                else:
                    nodes.append("m2cpp::scol(" + str(node[i]) + ")")
            else:
                nodes.append(str(node[i]))

    # mix of rowvecs and matrices, mix of columnvecs and matrices
    elif dims in ({2}, {3}, {2,3}, {1,3}):

        # make string of each vector in matrix
        nodes = []
        for i in xrange(len(node)):
            
            # decomposed vectors should be moved to own lines
            if node[i].value:
                nodes.append(str(node[i].auxiliary()))
            else:
                nodes.append(str(node[i]))

    try:
        if node.parent.name in ("imagesc", "wigb"):
            return "{" + reduce(lambda a,b: ("arma::join_cols(%s, %s)" % (a,b)), nodes) + "}"
        return reduce(lambda a,b: ("arma::join_cols(%s, %s)" % (a,b)), nodes)
    except:
        node.error("No match for handling matrix arg found")
        return "{", ", ", "}"


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

            if node.prop["ctype"] == "mat":
                return type + " _" + node[0].name + " [] = %(1)s ;\n"+\
                "%(0)s = %(ctype)s(_" + node[0].name + ", %(rows)s, 1, false) ;"
            else:
                return type + " _" + node[0].name + " [] = %(1)s ;\n"+\
                "%(0)s = %(ctype)s(_" + node[0].name + ", %(rows)s, false) ;"

            # use uniform initialization
            #return "%(0)s = %(1)s ;"

        # rowvec
        elif rhs.dim == 2:

            # save number of cols as 'cols'
            node["cols"] = len(node[1][0])*len(node[1])

            if node.prop["ctype"] == "mat":
                return type + " _" + node[0].name + " [] = %(1)s ;\n"+\
                "%(0)s = %(ctype)s(_" + node[0].name + ", 1, %(cols)s, false) ;"
            else:
                return type + " _" + node[0].name + " [] = %(1)s ;\n"+\
                "%(0)s = %(ctype)s(_" + node[0].name + ", %(cols)s, false) ;"

            # use uniform initialization
            #return "%(0)s = %(1)s ;"

        # matrix
        elif rhs.dim == 3:
            # save number of rows and columns
            node["rows"] = len(node[1][0])
            node["cols"] = len(node[1])
            return type + " _" + node[0].name + " [] = %(1)s ;\n"+\
            "%(0)s = arma::strans(%(ctype)s(_" + node[0].name + ", %(rows)s, %(cols)s, false)) ;"

            # use uniform initialization
            #my_list = node[1].children
            #my_list = ["{" + str(elem) + "}" for elem in my_list]
            #return "%(0)s = {" + ", ".join(my_list) + "} ;"

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
