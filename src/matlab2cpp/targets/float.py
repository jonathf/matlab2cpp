Declare = "float %(name)s ;"
Float = "%(value)s"
Var = "%(name)s"

def Assign(node):
    node[0].suggest("float")
    return "%(0)s = %(1)s ;"
