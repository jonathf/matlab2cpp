
String = '%(value)s'
Var = "%(name)s"

def Assign(node):
    node[0].suggest("string")
    return '%(0)s[] = %(1)s ;'
