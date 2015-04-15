Declare = "unsigned int %(name)s ;"
Uint = "%(value)s"
Var = "%(name)s"

def Assign(node):
    node[0].suggest("uint")
    return "%(0)s = %(1)s ;"
