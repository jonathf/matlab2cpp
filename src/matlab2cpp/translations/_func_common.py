from _variables import *


def type_string(node):

    if node.type == "func_lambda":

        if hasattr(node.declare, "reference"):
            func = node.declare.reference

            if len(func[1]) == 0:
                ret = "void"
                prm = ", ".join([p.type for p in func[2]])

            elif len(func[1]) == 1:
                ret = func[1][0].type
                prm = ", ".join([p.type for p in func[2]])

            else:
                ret = "void"
                prm = ", ".join([p.type for p in func[2][:]+func[1][:]])

            return "std::function<" + ret + "(" + prm + ")>"

        else:
            node.warning("lambda function content not found")
            return "std::function"

    elif node.type == "struct":
        return "_"+node.name.capitalize()

    elif node.type == "structs":

        return "_" + node.name.capitalize()

    return node.type


def Returns(node):

    if node.backend == "func_return":
        return "", "" 

    if node.backend == "func_returns":
        out = ""
        for child in node[:]:
            out += ", " + type_string(child) + "& " + str(child)
        return out[2:]

    if node.backend == "func_lambda":
        return ""

    assert False


def Params(node):

    if node.backend in ("func_return", "func_returns"):

        out = ""
        for child in node[:]:
            out += ", " + type_string(child) + " " + str(child)
        return out[2:]


    if node.backend == "func_lambda":
        return ", ".join(["%s %s" % (type_string(n), n.name) for n in node])


    assert False


def Declares(node):

    if node.backend in ("func_return", "func_returns"):

        declares = {}
        structs = {}

        for child in node[:]:

            type = type_string(child)

            if type not in declares:
                declares[type] = []

            declares[type].append(child)

            if child.backend == "structs":
                structs[child.name] = child

        out = ""
        for key, val in declares.items():

            out += "\n" + key + " "
            for v in val:

                out += str(v)
                if v.name in structs:
                    var = structs[v.name].declare
                    size = var.parent[var.parent.names.index("_size")]
                    out += "[" + str(size.value) + "]"
                out += ", "

            out = out[:-2] + " ;"

        return out[1:]

    if node.backend == "func_lambda":
        return ", ".join(["%s %s" % (type_string(n), str(n)) for n in node])

    assert False


def Func(node):

    if node.backend == "func_return":
        node.type = node[1][0].type
        if node[-1][-1] and node[-1][-1][-1].cls == "Return":
            return "%(type)s %(name)s(%(2)s)\n{\n%(0)s\n%(3)s\n}"
        return "%(type)s %(name)s(%(2)s)\n{\n%(0)s\n%(3)s\nreturn %(1)s ;\n}"

    if node.backend == "func_returns":

        if len(node[1]) and len(node[2]):
            out = "void %(name)s(%(2)s, %(1)s)\n{\n"
        else:
            out = "void %(name)s(%(2)s%(1)s)\n{\n"
        if node[0]:
            out += "%(0)s\n"
        out += "%(3)s\n}"

        return out
    
    if node.backend == "func_lambda":

        return ""#// placeholder for %(name)s"

def Main(node):
    if node[0]:
        return """int main(int argc, char* argv[])
{
%(0)s
%(3)s
return 0 ;
}"""
    return """int main(int argc, char* argv[])
{
%(3)s
return 0 ;
}"""

