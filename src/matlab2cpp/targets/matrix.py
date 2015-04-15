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

    if [n for n in node if not n.num]:
        node["decomposed"] = False
        return "", ", ", ""

    if len(node) == 1 and dims == {0}:
        node.dim = 0
        node["decomposed"] = True
        return "", ", ", ""

    # Decomposed row
    if dims == {0}:
        node["decomposed"] = True
        node.dim = 2
        return "", "<<", ""

    # Concatenate rows
    elif dims == {2}:

        node["decomposed"] = False
        node.dim = 2
        nodes = [str(n) for n in node]

    elif dims == {0,2}:

        node["decomposed"] = False
        node.dim = 2

        nodes = []
        for i in xrange(len(node)):
            if node[i].dim == 0:
                nodes.append(str(node[i].auxillary((2, node.type))))
            else:
                nodes.append(str(node[i]))

    # Concatenate mats
    elif dims in ({1}, {3}, {1,3}):

        node["decomposed"] = False
        node.dim = 3
        nodes = [str(n) for n in node]

    else:
        return ""

    return reduce(lambda x,y: ("arma::join_cols(%s, %s)" % (x, y)), nodes)


def Matrix(node):

    dims = {n.dim for n in node}

    if len(node) == 1 and len(node[0]) == 0:
        if node.parent["class"] in ("Assign", "Statement"):
            node.parent["backend"] = "matrix"
        return ""

    elif [n for n in node if not n.num]:
        return "[", "; ", "]"

    elif all([n["decomposed"] for n in node]):

        if len(node) == 1:
            node.dim = 2
        elif dims == {0}:
            node.dim = 1
        else:
            node.dim = 3

        if node.parent["class"] in ("Assign", "Statement"):
            node.parent["backend"] = "matrix"
            return "", " <<endr<< ", " <<endr"
        return str(node.auxillary())

    elif dims == {0}:

        if node.parent["class"] in ("Assign", "Statement"):
            node.parent["backend"] = "matrix"
            return ""
        return str(node.auxillary())

    elif dims == {0,1}:
        node.dim = 1

        nodes = []
        for i in xrange(len(node)):

            if node[i]["decomposed"] or node[i].dim == 0:
                nodei = node[i].auxillary()
                nodes.append(str(nodei))
#                  if nodei.parent["class"] in ("Assign", "Statement"):
#                      nodei.parent["backend"] = "matrix"

            else:
                nodes.append(str(node[i]))

    # Concatenate mats
    elif dims in ({2}, {3}, {2,3}):

        node.dim = 3

        nodes = []
        for i in xrange(len(node)):
            if node[i]["decomposed"]:
                nodes.append(str(node[i].auxillary()))
            else:
                nodes.append(str(node[i]))


    return reduce(lambda a,b: ("arma::join_rows(%s, %s)" % (a,b)), nodes)



def Assign(node):
    if len(node[1][0]) == 0:
        return "%(0)s.reset() ;"
    return "%(0)s << %(1)s ;"


def Statement(node):
    name =  "_nullpointer"
    node[0].declare(name)
    return name + " << %(0)s ;"

