"""
Functions with multiple returns

Nodes
-----
Func : Function
    Contains: Returns, Params, Block
    Property: name

Returns : Function return variables
    Contains: Var, ...

Params : Function parameter variables
    Contains: Var, ...

Get : Function/Array retrieval
    Example: "y(4)"
    Contains: Gets
    Property: name
"""

def Returns(node):
    out = ""
    for child in node[:]:
        if child["pointers"] == 0:
            poi = "&"
        else:
            poi = "*"*(child["pointers"]-1)
        out += ", " + child.type() + poi + " " + str(child)
    return out[2:]


#  def Get(node):
#      raise NotImplementedError(
#          "illigal multi-return call for %s" % node["name"])

def Get(node):
    return "", ", ", ""

def Params(node):
    out = ""
    for child in node[:]:
        out += ", " + child.type() + "*"*child["pointers"] + " " + str(child)
    return out[2:]


def Func(node):

    if len(node[1]):
        out = "void %(name)s(%(0)s, %(1)s)\n{\n"
    else:
        out = "void %(name)s(%(0)s)\n{\n"
    out += declares(node)
    out += "%(2)s\n}"

    return out


#  def declares(node):
#  
#      declared = node.declares.copy()
#  
#      params = node.get_property_all(
#          "func", node["name"])
#      params = set([p["name"] for p in params
#                    if p.parent["class"] in ("Params", "Returns")])
#  
#      out = ""
#      for key, val in declared.items():
#          if key not in params:
#              out += val
#  
#      return out

def Assignees(node):
    return "*", ", *", ""

def Assigns(node):

    assigness = str(node[0])
    name = node["name"]
    args = str(node[1])

    return name + "("+assigness+", "+args+") ;\n"
