from .variables import *

def Cell(node):

    # cells must stand on own line
    if node.parent.cls not in ("Assign", "Assigns"):
        node.auxiliary("cell")

    return "{", ",", "}"

def Assign(node):

    if node.name == 'varargin':
        out = "%(0)s = va_arg(varargin, " + node[0].type + ") ;"
    else:
        out = "%(0)s.clear() ;"

        # append to cell, one by one
        for elem in node[1]:
            out = out + "\n%(0)s.push_back(" + str(elem) + ") ;"

    return out
