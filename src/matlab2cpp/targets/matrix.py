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


def Vector(node):

    dims = {n.dim for n in node}
    if None in dims:
        return "", ", ", ""

    if [n for n in node if not n.num]:
        node.value = "decomposed"
        return "", ", ", ""

    if len(node) == 1 and dims == {0}:
        node.dim = 0
        node.value = "decomposed"
        return "", ", ", ""

    # Decomposed row
    if dims == {0}:
        node.value = "decomposed"
        node.dim = 2
        return "", ", ", ""

    # Concatenate rows
    elif dims == {2}:

        node.value = ""
        node.dim = 2
        nodes = [str(n) for n in node]

    elif dims == {0,2}:

        node.value = ""
        node.dim = 2

        nodes = []
        for i in xrange(len(node)):
            if node[i].dim == 0:
                node[i].auxiliary((2, node.mem))
            nodes.append(str(node[i]))

    # Concatenate mats
    elif dims in ({1}, {3}, {1,3}):

        node.value = ""
        node.dim = 3
        nodes = [str(n) for n in node]

    else:
        return ""

    return reduce(lambda x,y: ("arma::join_rows(%s, %s)" % (x, y)), nodes)


def Matrix(node):

    dims = {n.dim for n in node}

    if None in dims:
        return "[", ", ", "]"

    if len(node) == 1 and len(node[0]) == 0:
        node.dim = 0
        if node.parent["class"] in ("Assign", "Statement"):
            node.parent["backend"] = "matrix"
        return ""

    elif all([n.value for n in node]):
        node.value = "decomposed"

        ax0, ax1 = len(node), len(node[0])
        if ax0 > 1:
            if ax1 > 1:
                node.dim = 3
            else:
                node.dim = 2
        else:
            if ax1 > 1:
                node.dim = 1
            else:
                node.dim = 0

        if node.parent["class"] in ("Assign", "Statement"):
            node.parent["backend"] = "matrix"
            return "{", ", ", "}"
        return str(node.auxiliary())

    elif dims == {0}:

        if len(node) > 1:
            if len(node[0]) > 1:
                node.dim = 3
            else:
                node.dim = 2
        else:
            if len(node[0]) > 1:
                node.dim = 1
            else:
                node.dim = 0

        if node.parent["class"] in ("Assign", "Statement"):
            node.parent["backend"] = "matrix"
            return ""
        return str(node.auxiliary())

    elif dims in ({0,1}, {1}):

        if len(node)>1:
            node.dim = 3
        else:
            node.dim = 1

        nodes = []
        for i in xrange(len(node)):

            if node[i].value or node[i].dim == 0: # value=decomposed
                nodei = node[i].auxiliary()
                nodes.append(str(nodei))

            else:
                nodes.append(str(node[i]))

    # Concatenate mats
    elif dims in ({2}, {3}, {2,3}):

        if dims == {2} and len(node)==1:
            node.dim = 2
        else:
            node.dim = 3

        nodes = []
        for i in xrange(len(node)):
            if node[i].value: # decomposed
                nodes.append(str(node[i].auxiliary()))
            else:
                nodes.append(str(node[i]))

    else:
        return "[", "; ", "]"

    return reduce(lambda a,b: ("arma::join_cols(%s, %s)" % (a,b)), nodes)



def Assign(node):

    lhs, rhs = node

    assert rhs.cls in ("Matrix", "Cell")
    assert rhs.cls in ("Matrix")

    if len(rhs[0]) == 0:
        return "%(0)s.reset() ;"

    if not lhs.num or not rhs.num:
        return "%(0)s = %(1)s ;"

    node.type = node["ctype"] = node[0].type
    dim = node.dim
    node.dim = 0

    if rhs.value: # decomposed

        if dim == 0:
            return "%(0)s = " + str(rhs[0][0]) + " ;"

        elif dim == 1: #vec
            node["rows"] = len(node[1][0])
            return "%(type)s _%(0)s [] = %(1)s ;\n"+\
                    "%(0)s = %(ctype)s(_%(0)s, %(rows)s, false) ;"

        elif dim == 2: #rowvec
            node["cols"] = len(node[1])
            return "%(type)s _%(0)s [] = %(1)s ;\n"+\
                    "%(0)s = %(ctype)s(_%(0)s, %(cols)s, false) ;"

        elif dim == 3: #mat
            node["rows"] = len(node[1][0])
            node["cols"] = len(node[1])
            return "%(type)s _%(0)s [] = %(1)s ;\n"+\
        "%(0)s = %(ctype)s(_%(0)s, %(rows)s, %(cols)s, false) ;"

        print rhs.type
        print [r.type for r in rhs]
        assert False

    return "%(0)s = %(1)s ;"

def Statement(node):
    return "// " + node.code[:-1]

Var = "%(name)s"

def Cell(node):

    if node.parent.cls not in ("Assign", "Assigns"):
        node.auxiliary()

    return "{", ", ", "}"
