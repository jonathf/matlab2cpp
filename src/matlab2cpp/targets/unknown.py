
Var = "%(name)s"
Assignees = "", ", ", ""
Assigns = "%(0)s = %(1)s ;\n"
Declare = "TYPE %(name)s ;"

def Set(node):
    "arrays"
#      type = node[1].type()
#  
#      if type != "TYPE":
#          node.type(type)
#          node[0].suggest(type)

    return "%(name)s(%(0)s) = %(1)s ;"

def Set2(node):
    "tuple"
    n0 = node[0]
    t0 = n0.type()
    if t0 == "int":
        assign = "_"+str(n0)
    elif t0 == "float":
        assign = "_"+"_".join(str(n0).split("."))
    else:
        raise NotImplementedError

    return node["name"]+"::"+assign + "= %(1)s ;"

def Set3(node):
    "fieldname"
    return "%(name)s.(%(0)s) = %(1)s ;"


def Get(node):

    names = node.program["names"]
    if node["name"] in names:
        func = node.program[names.index(node["name"])+1]
        if len(func[1]) == 1:
            node["backend"] = "func_return"
        else:
            node["backend"] = "func_returns"
    return "%(name)s(", ", ", ")"

def Get2(node):
    "tuple"
    n0 = node[0]
    t0 = n0.type()
    if t0 == "int":
        assign = "_"+str(n0)
    elif t0 == "float":
        assign = "_"+"_".join(str(n0).split("."))
    else:
        assign = str(n0)

    return node["name"]+"::"+assign

def Get3(node):
    "fieldname"
    return "%(name)s.(%(0)s)"

def Assign(node):

    t0, t1 = node[0].type(), node[1].type()
    node.type(t1)

    return "%(0)s = %(1)s ;"
