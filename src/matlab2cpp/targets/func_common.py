from variables import *

def Returns(node):

    if node.backend == "func_return":
        return "%(0)s"

    if node.backend == "func_returns":
        out = ""
        for child in node[:]:
            out += ", " + child.type + " " + str(child)
        return out[2:]

    if node.backend == "func_lambda":
        return ""

    assert False


def Params(node):

    if node.backend in ("func_return", "func_returns"):

        out = ""
        for child in node[:]:
            out += ", " + child.type + " " + str(child)
        return out[2:]


    if node.backend == "func_lambda":
        return ", ".join(["%s %s" % (n.type, n.name) for n in node])


    assert False


def Declares(node):

    if node.backend in ("func_return", "func_returns"):
        declares = {}
        for child in node[:]:

            type = child.type

            if type == "func_lambda":
                type == "std::function"

            if type == "struct":
                type = child["name"].capitalize()

            if type not in declares:
                declares[type] = []
            declares[type].append(child)

        out = ""
        for key, val in declares.items():
            out = out + "\n" + key + " " + ", ".join([v["name"] for v in val]) + " ;"

        return out[1:]

    if node.backend == "func_lambda":
        return ", ".join(["%s %s" % (n.type, n["name"]) for n in node])


    assert False


def Func(node):

    if node.backend == "func_return":
        type = node[1][0].type
        return type + " %(name)s(%(2)s)\n{\n%(0)s\n%(3)s\nreturn %(1)s ;\n}"

    if node.backend == "func_returns":

        if len(node[1]) and len(node[2]):
            out = "void %(name)s(%(2)s, %(1)s)\n{\n"
        else:
            out = "void %(name)s(%(2)s%(1)s)\n{\n"
        out += "%(0)s\n%(3)s\n}"

        return out
    
    if node.backend == "func_lambda":

        return ""#// placeholder for %(name)s"


def Get(node):
    return "%(name)s(", ", ", ")"

def Var(node):
    return "@%(name)s"
