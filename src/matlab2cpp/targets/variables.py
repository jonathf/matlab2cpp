
Var = "%(name)s"
Fvar = "%(name)s.%(sname)s"

def Set(node):
    node.typeerror()
    return "%(name)s(", ", ", ")"

def Cset(node):
    node.typeerror()
    return "%(name)s{", "}{", "}"

def Fset(node):
    node.typeerror()
    return "%(name)s.%(sname)s(", ", ", ")"

def Nset(node):
    node.typeerror()
    return "%(name)s.(", ", ", ")"

def Get(node):
    node.typeerror()
    return "%(name)s(", ", ", ")"

def Cget(node):
    node.typeerror()
    return "%(name)s{", "}{", "}"

def Fget(node):
    node.typeerror()
    return "%(name)s.%(sname)s(", ", ", ")"

def Nget(node):
    node.typeerror()
    return "%(name)s.(", ", ", ")"
