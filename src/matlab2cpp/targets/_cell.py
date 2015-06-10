from _variables import *

def Cell(node):
    if node.parent.cls not in ("Assign", "Assigns"):
        node.auxiliary("cell")
    return "{", ",", "}"

def Assign(node):
    out = "%(0)s.clear() ;"
    for elem in node[1]:
        out = out + "\n%(0)s.push_back(" + str(elem) + ") ;"
    return out

def Cvar(node):
    "a{b}"
    return "%(name)s{", ", ", "}"

def Cset(node):
    "a{b}(c) = d"
    pass

def Cget(node):
    "a{b}(c)"
    pass
