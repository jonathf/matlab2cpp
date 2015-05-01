
Var = "%(name)s"
Fvar = "%(name)s.%(sname)s"

def Cvar(node):
#      node.typeerror()
    return "%(name)s{", "}{", "}"

def Set(node):
#      node.typeerror()
    return "%(name)s(", ", ", ")"

def Cset(node):
    n_fields = node["n_fields"]
    print n_fields, len(node)

    out = "%(name)s{%("
    out = out + ")s}{%(".join(map(str, range(n_fields)))
    out = out + ")s}(%("
    out = out + ")s, %(".join(map(str, range(n_fields, len(node))))
    out = out + ")s)"
    return out

def Fset(node):
#      node.typeerror()
    return "%(name)s.%(sname)s(", ", ", ")"

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
#      node.typeerror()
    return "%(name)s.%(sname)s(", ", ", ")"

def Nget(node):
#      node.typeerror()
    return "%(name)s.(", ", ", ")"

def Assign(node):
    return "%(0)s = %(1)s ;"


#  def error(node):
#  
#      text = "The variable type"

