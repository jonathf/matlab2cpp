Declare = "double %(name)s ;"
Float = "%(value)s"
Var = "%(name)s"

def Assign(node):
    node[0].suggest("double")
    return "%(0)s = %(1)s ;"
