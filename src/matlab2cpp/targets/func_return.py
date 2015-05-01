"""
Functions with single return

Nodes
-----
Func : Function
    Contains: Declares, Returns, Params, Block
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
from variables import *

def Returns(node):
    return "%(0)s"

def Get(node):
    return "%(name)s(", ", ", ")"


def Params(node):
    out = ""
    for child in node[:]:
        out += ", " + child.type + child.pointer() + " " + str(child)
    return out[2:]



def Func(node):
    type = node[1][0].type
    return type + " %(name)s(%(2)s)\n{\n%(0)s\n%(3)s\nreturn %(1)s ;\n}"

adjusts = {"func_lambda": "std::function",
        "uint": "unsigned int"}

def Declares(node):
    declares = {}
    for child in node[:]:
        type = child.type
        if type not in declares:
            declares[type] = []
        declares[type].append(child)

    for key,val in adjusts.items():
        if key in declares:
            declares[val] = declares.pop(key)

    out = ""
    for key, val in declares.items():
        out = out + "\n" + key + " " + ", ".join([v["name"] for v in val]) + " ;"

    return out[1:]

def Var(node):
    out = "@%(name)s"
    return out
