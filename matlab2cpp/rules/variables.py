
def Var(node):
    if node.type == "TYPE":
        node.error("unknown data type")
    return "%(name)s"

def Fvar(node):

    if node.backend == "structs":
        if node.parent.cls == "Vector":
            if len(node.parent) == 1:
                size = node.declare.parent["_size"]
                return size.value
        return "%(name)s[0].%(value)s"
    return "%(name)s.%(value)s"

def Cvar(node):
    "a{b}"

    if node.type == "TYPE":
        node.declare.type = "cell"

    elif node.type != "cell":
        node.error("Behaves like cell, not %s" % node.type)

    return "%(name)s{", "}{", "}"

def Set(node):
    if node.type == "TYPE":
        node.error("unknown data type")
    elif node.num and node.mem == 0:
        node.error("scalar are not iterable")
    return "%(name)s(", ", ", ")"

def Cset(node):
    "a{b}(c) = d"

    if node.type == "TYPE":
        node.declare.type = "cell"

    elif node.type != "cell":
        node.error("Behaves like cell, not %s" % node.type)

    n_fields = node["n_fields"]

    out = "%(name)s{%("
    out = out + ")s}{%(".join(map(str, range(n_fields)))
    out = out + ")s}(%("
    out = out + ")s, %(".join(map(str, range(n_fields, len(node))))
    out = out + ")s)"
    return out

def Sset(node):
    node.pointer = 0
    if len(node) == 1 and node[0].cls == "Int":
        return "%(name)s[" + str(int(node[0].value)-1) + "].%(value)s"
    return "%(name)s[", ", ", "-1].%(value)s"

def Nset(node):
    return "%(name)s.(", ", ", ")"

def Get(node):
    return "%(name)s(", ", ", ")"

def Cget(node):
    "a{b}(c)"

    if node.type == "TYPE":
        node.declare.type = "cell"

    elif node.type != "cell":
        node.error("Behaves like cell, not %s" % node.type)

    n_fields = node["n_fields"]

    out = "%(name)s{%("
    out = out + ")s}{%(".join(map(str, range(n_fields)))
    out = out + ")s}(%("
    out = out + ")s, %(".join(map(str, range(n_fields, len(node))))
    out = out + ")s)"
    return out

def Fget(node):
    node.pointer = 0
    if len(node) == 1 and node[0].cls == "Int":
        return "%(name)s[" + str(int(node[0].value)-1) + "].%(value)s"
    return "%(name)s.%(value)s(", ", ", ")"

def Sget(node):
    return "%(name)s[", ", ", "-1].%(value)s"

def Nget(node):
    return "%(name)s.(", ", ", ")"
