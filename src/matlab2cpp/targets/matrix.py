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


    types = list(set([n.type() for n in node]))
    types.sort()

    if len(node) == 1 or "TYPE" in types:

        node["decomposed"] = True
        return "", ", ", ""

    # Decomposed row
    if all([t in ("float", "int") for t in types]):

        node["decomposed"] = True
        if "float" in types:
            node.type("frowvec")
        else:
            node.type("irowvec")
        return "", "<<", ""

    # Concatenate rows
    elif all([t in ("float", "int", "irowvec", "frowvec")
            for t in types]):

        node["decomposed"] = False

        if "float" in types or "frowvec" in types:
            node.type("frowvec")
        else:
            node.type("irowvec")

        nodes = []
        for i in xrange(len(node)):
            child = node[i]
            type = child.type()
            if type == "float":
                child = child.auxillary("frowvec")
            elif type == "int":
                child = child.auxillary("irowvec")

            nodes.append(child)

    # Concatenate mats
    else:

        node["decomposed"] = False

        for t in ["float", "int", "frowvec", "irowvec"]:
            if t in types:
                print [str(n) for n in node]
                raise ValueError("illigal concatination of scalar and/or vector")

        if "fvec" in types or "fmat" in types:
            node.type("fmat")
        else:
            node.type("imat")

        nodes = node

    return reduce(lambda x,y: ("arma::join_cols(%s, %s)" % (x, y)), nodes)


def Matrix(node):

    types = set([n.type() for n in node])

    if "TYPE" in types:
        return "[", "; ", "]"

    if len(node) == 1:

        if len(node[0]) == 1:

            if node.parent["class"] in ("Assign", "Statement"):
                node.parent["backend"] = "matrix"
                return "%(0)s"

            return node.auxillary()

        if any([n.type() == "frowvec" for n in node]):
            node.type("frowvec")
        else:
            node.type("irowvec")

        if node[0]["decomposed"]:

            if node.parent["class"] in ("Assign", "Statement"):
                node.parent["backend"] = "matrix"
                return "%(0)s"

            return node.auxillary()

        return "%(0)s"

    if all([n["decomposed"] for n in node]):

        if len(node[0]) == 1:
            if any([n.type() == "float" for n in node]):
                type = node.type("fvec")
            else:
                type = node.type("ivec")
        else:
            if any([n.type() == "frowvec" for n in node]):
                type = node.type("fmat")
            else:
                type = node.type("imat")


        if node.parent["class"] in ("Assign", "Statement"):
            node.parent["backend"] = "matrix"
            return "", " <<arma::endr<< ", ""

        return node.auxillary(type)


    types = list(set([n.type() for n in node[:]]))
    types.sort()


    # Concatinate cols
    if all([t in ("float", "int", "ivec", "fvec")
            for t in types]):

        if "float" in types or "fvec" in types:
            node.type("fvec")
        else:
            node.type("ivec")

        nodes = []
        for child in node:
            type = child.type()
            if type == "float":
                child = child.auxillary("fvec")

            elif type == "int":
                child = child.auxillary("ivec")

            elif child["decomposed"]:
                if type == "fvec":
                    child.auxillary("fvec")
                else:
                    child.auxillary("ivec")

            nodes.append(child)

    # Concatenate mats
    else:

        for t in ["float", "int", "fvec", "ivec"]:
            if t in types:
                print [str(n) for n in node]
                raise ValueError("illigal concatination of scalar and/or vector")

        if "frowvec" in types or "fmat" in types:
            node.type("fmat")
        else:
            node.type("imat")

        nodes = []
        for child in node:
            if child["decomposed"]:
                if child.type() == "frowvec":
                    child = child.auxillary("frowvec")
                else:
                    child = child.auxillary("irowvec")
            node.append(child)

    return reduce(lambda a,b: ("arma::join_rows(%s, %s)" % (a,b)), nodes)



def Assign(node):
    if len(node[1][0]) == 0:
        return "%(0)s.reset() ;"
    node[0].suggest(node[1].type())
    return "%(0)s << %(1)s ;"


def Statement(node):
    name =  "_wasteful%03d" % node.program.next_index()
    node[0].declare(name)
    return name + " << %(0)s ;"
