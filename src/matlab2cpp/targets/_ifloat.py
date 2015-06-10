from _variables import *

Declare = "cx_double %(name)s ;"
def Ifloat(node):
    return "cx_double(0, %(value)s)"
