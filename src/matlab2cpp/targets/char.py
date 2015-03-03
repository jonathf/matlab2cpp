
Var = "%(name)s"
Type = "char"

def Assign(node):
    node[0].suggest("char")
    return "%(0)s = %(1)s ;"
