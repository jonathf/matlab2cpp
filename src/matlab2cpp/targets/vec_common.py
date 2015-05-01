from variables import *

Var = "%(name)s"

def Get(node):

    assert len(node) == 1
    node.type = "uvec"
    arg = node[0]

    if arg["class"] == "All":
        return "%(name)s"

    elif not arg.num:
        return "%(name)s(%(0)s)"

    elif arg.dim == 0:
        node.dim = 0
        out = str(arg)+"-1"

    elif arg.mem != 0:
        out = str(arg.auxillary((arg.dim, 0), convert=True))

    else:
        out = str(arg)

    if arg.dim == 2:
        out = out + ".t()"
    elif arg.dim > 2:
        out = "vectorise(" + out + ")"

    out = "%(name)s(" + out + ")"

    return out

#  def Assign(node):
#  
#      if node[1]["decomposed"]:
#          return "%(0)s << %(1)s ;"
#  
#      if node[0].cls == "Var":
#          return "%(0)s = %(1)s ;"
#  
#      sets, expr = node
#  
#      assert len(sets) == 1
#      assert sets["class"] in "Set"
#  
#      node.type = "uvec"
#      arg = sets[0]
#  
#      if expr.dim == 2:
#          rhs = "(" + str(expr) + ").t()"
#      else:
#          rhs = str(expr)
#  
#      if arg.dim == 0: # constant
#          out = str(arg)+"-1"
#  
#      elif arg["class"] == "All":
#          if expr.dim == 0:
#              return "%(name)s.fill(" + rhs + ") ;"
#          return "%(name)s = " + rhs + " ;"
#  
#      elif not arg.num:
#          return "%(name)s(%(0)s) = " + rhs + " ;"
#  
#      elif arg.mem != 0:
#          out = str(arg.auxillary((arg.dim, 0), convert=True))
#  
#      else:
#          out = str(arg)
#  
#      if arg.dim == 2:
#          out = out + ".t()"
#      elif arg.dim > 2:
#          out = "vectorise(" + out + ")"
#  
#      out = "%(name)s(" + out + ") = " + rhs + " ;"
#  
#      return out

def Assign(node):

    if node[1]["decomposed"]:
        return "%(0)s << %(1)s ;"

    if node[0].cls == "Var":
        return "%(0)s = %(1)s ;"

    sets, expr = node

    if expr.dim == 2:
        rhs = "(%(1)s).t()"
    else:
        rhs = "%(1)s"


    out = "%(0)s = " + rhs + " ;"

    return out


def Set(node):

    assert len(node) == 1

    arg = node[0]

    if arg["class"] == "All":
        return "%(name)s"

    elif arg.dim == 0: # constant
        out = "%(0)s-1"
        node.dim = 0

    elif not arg.num:
        return "%(name)s(%(0)s)"

    elif arg.mem != 0:
        arg.auxillary((arg.dim, 0), convert=True)
        out = "%(0)s"

    else:
        out = "%(0)s"

    if arg.dim == 2:
        out = "(" + out + ").t()"
    elif arg.dim > 2:
        out = "vectorise(" + out + ")"

    return "%(name)s(" + out + ")"
