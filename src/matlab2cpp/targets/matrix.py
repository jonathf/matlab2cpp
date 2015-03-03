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

def Matrix(node):
    types = list(set([n.type() for n in node[:]]))
    types.sort()

    if "TYPE" in types:
        return "[", "; ", "]"

    node["decomposed"] = False

    # Still  col
    if all([t in ("float", "int") for t in types]):

        if len(node)>1:
            types += ["ivec"]
        node.type(types)

    if all([t in ("float", "int", "ivec", "fvec")
            for t in types]):
        if len(node)>1 or types[0] not in ("int", "float"):
            types += ["ivec"]
        node.type(types)

    # concatenate rows
    else:
        if len(node)>1 or types[0] not in ("irowvec", "frowvec"):
            types += ["imat"]
        node.type(types)

    if all(n["decomposed"] for n in node[:]):

        node["decomposed"] = True
        node.type(types)
        if node.parent["class"] in ("Assign", "Statement"):
            return "", "<< arma::endr <<", ""
        return node.auxillary()

    out = []
    for vec in node[:]:
        type = vec.type()
        if type in ("float", "int"):
            vec.type([type, "ivec"])
            out.append(vec.auxillary())

        elif vec["decomposed"]:
            out.append(vec.auxillary())
        else:
            out.append(vec["str"])
    return reduce(lambda a,b: ("arma::join_rows(%s, %s)" % (a,b)), out)



def Vector(node):
    types = list(set([n.type() for n in node[:]]))
    types.sort()

    if "TYPE" in types:
        return "", ", ", ""

    node["decomposed"] = False

    # Decomposed row
    if all([t in ("float", "int") for t in types]):

        node["decomposed"] = True
        if len(node)>1:
            types += ["irowvec"]
        node.type(types)

        return "", "<<", ""

    # Concatenated row
    elif all([t in ("float", "int", "irowvec", "frowvec")
            for t in types]):

        node.type(types)

    # Concatenate cols
    else:
        if len(node)>1 or types[0] not in ("ivec", "fvec"):
            types += ["imat"]
        node.type(types)


    out = []
    for n in node[:]:
        type = n.type()
        if type in ("float", "int"):
            n.type([type, "irowvec"])
            out.append(n.auxillary())
        else:
            out.append(str(n["str"]))

    return reduce(lambda a,b: ("arma::join_cols(%s, %s)" % (a,b)), out)

