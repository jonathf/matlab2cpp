from variables import *

Declare = "cx_double %(name)s ;"
def Ifloat(node):
    node.include("complex")
    return "%(value)s*sqrt(-1)"
