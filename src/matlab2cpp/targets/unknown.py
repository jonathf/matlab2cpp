
Var = "%(name)s"
Assignees = "", ", ", ""
Assigns = "%(0)s = %(1)s ;\n"
Declare = "TYPE %(name)s ;"

def Set(node):
    "arrays"
    return "%(name)s(%(0)s) = %(1)s ;"

def Set2(node):
    "tuple"
    return "%(name)s{%(0)s} = %(1)s ;"

def Set3(node):
    "fieldname"
    return "%(name)s.(%(0)s) = %(1)s ;"


def Get(node):

    names = node.program["names"]
    if node["name"] in names:
        func = node.program[names.index(node["name"])]
        if len(func[1]) == 1:
            node["backend"] = "func_return"
        else:
            node["backend"] = "func_returns"
    return "%(name)s(", ", ", ")"

def Get2(node):
    "tuple"
    return "%(name)s{%(0)s} ;"

def Get3(node):
    "fieldname"
    return "%(name)s.(%(0)s)"

def Assign(node):
    return "%(0)s = %(1)s ;"
