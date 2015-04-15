Declare = "double complex %(name)s ;"
Imag = "%(value)s*I"
Var = "%(name)s"

def Assign(node):
#      node[0].suggest("complex")
    return "%(0)s = %(1)s ;"
