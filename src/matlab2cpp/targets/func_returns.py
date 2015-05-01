"""
Functions with multiple returns

Nodes
-----
Func : Function
    Contains: Returns, Params, Block
    Property: name

Returns : Function return variables
    Contains: Var, ...

Params : Function parameter variables
    Contains: Var, ...

Get : Function/Array retrieval
    Example: "y(4)"
    Contains: Gets
    Property: name
"""
from variables import *

def Returns(node):
    out = ""
    for child in node[:]:
        child.prop["pointer"] -= 1
        out += ", " + child.type + child.pointer() + " " + str(child)
    return out[2:]


def Get(node):
    return "", ", ", ""

def Params(node):
    out = ""
    for child in node[:]:
        out += ", " + child.type + child.pointer() + " " + str(child)
    return out[2:]


def Func(node):

    if len(node[1]):
        out = "void %(name)s(%(1)s, %(2)s)\n{\n"
    else:
        out = "void %(name)s(%(2)s)\n{\n"
    out += "%(0)s\n%(3)s\n}"

    return out



def Assignees(node):
    return "*", ", *", ""

def Assigns(node):

    assigness = str(node[0])
    name = node["name"]
    args = str(node[1])

    return name + "("+assigness+", "+args+") ;\n"


def Declares(node):
    declares = {}
    for child in node[:]:
        type = child.type
        if type not in declares:
            declares[type] = []
        declares[type].append(child)

    out = ""
    for key, val in declares.items():
        out = out + "\n" + key + " " + ", ".join([v["name"] for v in val]) + " ;"

    return out[1:]


def Var(node):
    out = "@%(name)s"
    return out
