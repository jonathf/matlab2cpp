
Declare = "int %(name)s ;"
Type = "int"
Int = "%(value)s"
Var = "%(name)s"

def Assign(node):
    node[0].suggest("int")
    return "%(0)s = %(1)s ;"

def Get(node):
#      node.error("'%s'\t\trecast between int and callable" % node["name"])
    return "<error:%(name)s(%(0)s)>"
