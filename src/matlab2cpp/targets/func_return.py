"""
Functions with single return

Nodes
-----
Func : Function
    Contains: Returns, Params, Block
    Property: name

Returns : Function return variables
    Contains: Var, ...

Params : Function parameter variables
    Contains: Var, ...

Declares : Declarations in the beginning of function
    Contains: Var, ...
    Rule: func_return.py (if one variable return)
          func_returns.py (if multiple return)

Get : Function/Array retrieval
    Example: "y(4)"
    Contains: Gets
    Property: name
"""

def Returns(node):
    return "%(0)s"

def Get(node):

    name = node["name"]
    names = node.program["names"]
    func = node.program[names.index(name)+1]
    ret_val = func[1][0]
    node.type(ret_val.type())

    params = func[2]
    for i in xrange(len(node)):
        param = params[i]
        type = param.type()
        if type == "TYPE":
            type_ = node[i].type()
            if type_ != "TYPE":
                param.suggest(type_)

    return "%(name)s(", ", ", ")"


def Params(node):
    out = ""
    for child in node[:]:
        out += ", " + child.type() + "*"*child["pointers"] + " " + str(child)
    return out[2:]



def Func(node):
    type = node[1][0].type()
    return type + " %(name)s(%(2)s)\n{\n%(0)s\n%(3)s\nreturn %(1)s\n}"

def Declares(node):
    declares = {}
    for child in node[:]:
        type = child.type()
        if type not in declares:
            declares[type] = []
        declares[type].append(child)

    out = ""
    for key, val in declares.items():

        if key in ("int", "float", "ivec", "fvec", "irowvec",
                "frowvec", "imat", "fmat", "TYPE"):
            out = out + "\n" + key + " " + ", ".join([v["name"] for v in val]) + " ;"
        else:
            out = out + "\n" + "\n".join(map(str, val))

    return out[1:]

def Var(node):
    out = "@%(name)s"
    return out
