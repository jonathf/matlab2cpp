from assign_common import Assign

Var = "%(name)s"
Fvar = "%(name)s.%(value)s"

def Cvar(node):
#      node.typeerror()
    return "%(name)s{", "}{", "}"

def Set(node):
#      node.typeerror()
    return "%(name)s(", ", ", ")"

def Cset(node):
    n_fields = node["n_fields"]

    out = "%(name)s{%("
    out = out + ")s}{%(".join(map(str, range(n_fields)))
    out = out + ")s}(%("
    out = out + ")s, %(".join(map(str, range(n_fields, len(node))))
    out = out + ")s)"
    return out

def Fset(node):
#      node.typeerror()
    return "%(name)s.%(value)s(", ", ", ")"

def Sset(node):
    return "%(name)s(", ", ", ").%(value)s"

def Nset(node):
#      node.typeerror()
    return "%(name)s.(", ", ", ")"

def Get(node):
#      node.typeerror()
    return "%(name)s(", ", ", ")"

def Cget(node):
    n_fields = node["n_fields"]

    out = "%(name)s{%("
    out = out + ")s}{%(".join(map(str, range(n_fields)))
    out = out + ")s}(%("
    out = out + ")s, %(".join(map(str, range(n_fields, len(node))))
    out = out + ")s)"
    return out

def Fget(node):
    return "%(name)s.%(value)s(", ", ", ")"

def Sget(node):
    return "%(name)s(", ", ", ").%(value)s"

def Nget(node):
    return "%(name)s.(", ", ", ")"
