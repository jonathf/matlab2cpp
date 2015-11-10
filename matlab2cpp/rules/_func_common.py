from _variables import *


def type_string(node):
    """
Determine string represnentation of type.

Outside scalars and armadillo, the datatype name and their declaration do not
match. This function converts simple datatype declaration and translate them to
equivalent C++ declarations.

Args:
    node (Node): location in tree
Returns:
    str: String representation of node type
    """

    # lambda-function
    if node.type == "func_lambda":

        # link to actual lambda-function
        if hasattr(node.declare, "reference"):
            func = node.declare.reference

            # no returns in lambda
            if len(func[1]) == 0:
                ret = "void"
                prm = ", ".join([p.type for p in func[2]])

            # single return
            elif len(func[1]) == 1:
                ret = func[1][0].type
                prm = ", ".join([p.type for p in func[2]])

            # multiple return
            else:
                ret = "void"
                prm = ", ".join([p.type for p in func[2][:]+func[1][:]])

            return "std::function<" + ret + "(" + prm + ")>"

        else:
            node.warning("lambda function content not found")
            return "std::function"

    # struct type
    elif node.type == "struct":
        return "_"+node.name.capitalize()

    # struct array type
    elif node.type == "structs":
        return "_" + node.name.capitalize()

    return node.type


def Returns(node):

    if node.backend == "func_return":
        return "", "" 

    # In multi-returns, place return values in parameters as references
    if node.backend == "func_returns":
        out = ""
        for child in node[:]:
            out += ", " + type_string(child) + "& " + str(child)
        return out[2:]

    # lambda functions are only printed in Lambda
    if node.backend == "func_lambda":
        return ""

    assert False


def Params(node):

    if node.backend in ("func_return", "func_returns"):

        # Create list of parameters
        out = ""
        for child in node[:]:
            out += ", " + type_string(child) + " " + str(child)
        return out[2:]

    # lambda functions are only printed in Lambda
    if node.backend == "func_lambda":
        return ", ".join(["%s %s" % (type_string(n), n.name) for n in node])


    assert False


def Declares(node):

    # normal functions
    if node.backend in ("func_return", "func_returns"):

        if not node:
            return ""

        returns = node.parent[1]

        declares = {}   # {"int" : ["a", "b"]} -> int a, b ;
        structs = {}    # {"_A" : "a"} -> _A a;

        # fill declares and structs
        for child in node[:]:

            # return values i multi-returns are declared as parameter
            if child.name in returns and node.backend == "func_returns":
                continue

            type = type_string(child)

            if type not in declares:
                declares[type] = []

            declares[type].append(child)

            if child.type == "structs":
                structs[child.name] = child

        # create output
        out = ""
        keys = declares.keys()
        keys.sort()
        for key in keys:
            val = declares[key]
            val.sort()

            # datatype
            out += "\n" + key + " "

            # all variables with that type
            for v in val:

                out += str(v)
                if v.name in structs:

                    structs_ = node.program[3]
                    struct = structs_[structs_.names.index(v.name)]
                    size = struct[struct.names.index("_size")].value
                    out += "[%s]" % size

                out += ", "

            out = out[:-2] + " ;"

        return out[1:]

    # lambda functions is just a comma separated list
    if node.backend == "func_lambda":
        return ", ".join(["%s %s" % (type_string(n), str(n)) for n in node])

    assert False


def Func(node):

    # single return function
    if node.backend == "func_return":

        node.type = node[1][0].type

        # function ends with a return statement
        if node[-1][-1] and node[-1][-1][-1].cls == "Return":
            return """%(type)s %(name)s(%(2)s)
{
%(0)s
%(3)s
}"""

        return """%(type)s %(name)s(%(2)s)
{
%(0)s
%(3)s
return %(1)s ;
}"""

    # zero or multiple returns
    if node.backend == "func_returns":

        # both returns and parameters present
        if len(node[1]) and len(node[2]):
            if len(node[0])>len(node[1]):
                return """void %(name)s(%(2)s, %(1)s)
{
%(0)s
%(3)s
}"""
            return """void %(name)s(%(2)s, %(1)s)
{
%(3)s
}"""

        # one of returns or params missing
        if len(node[0])>len(node[1]):
            return """void %(name)s(%(2)s%(1)s)
{
%(0)s
%(3)s
}"""
        return """void %(name)s(%(2)s%(1)s)
{
%(3)s
}"""
    
    if node.backend == "func_lambda":
        return ""


def Main(node):

    # has variables to declare
    if node[0]:
        return """int main(int argc, char** argv)
{
%(0)s
%(3)s
return 0 ;
}"""
    return """int main(int argc, char** argv)
{
%(3)s
return 0 ;
}"""

