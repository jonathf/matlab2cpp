from assign import Assign
from variables import *

Declare = "TYPE %(name)s ;"

def Assigns(node):
    lhs = map(str, node[:-1])
    lhs = "[" + ", ".join(lhs) + "]"
    rhs = str(node[-1])
    return lhs + " = " + rhs + " ;"

def Matrix(node):
    return "", ", ", ""
