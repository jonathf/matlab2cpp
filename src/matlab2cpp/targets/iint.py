from variables import *

Declare = "cx_double"
def Iint(node):
    node.include("complex")
    return "%(value)s*sqrt(-1)"
