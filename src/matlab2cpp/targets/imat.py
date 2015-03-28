from mat_common import *

Declare = "imat %(name)s ;"

#  
#  from arma import *
#  
#  def Get(node):
#  
#      # Single argument
#      if len(node)==1:
#  
#          type = node[0].type()
#          # normal indexing
#          if type in ("int", "float"):
#              val = node[0]["str"]+"-1"
#              type = node.type("ivec")
#  
#          # slice of sorts
#          else:
#              val = node[0]["str"]
#              type = node.type("imat")
#          val = "(%(name)s.n_rows-1)".join(val.split("&$"))
#  
#          # not of range
#          if "&:" not in val:
#  
#              # full range
#              if "&=" == val:
#                  return "%(name)s"
#  
#              return "%(name)s.row("+val+")"
#  
#          val = val.split("&:")
#  
#          # without step
#          if len(val) == 4:
#              return "%(name)s.cols("+\
#                      val[0]+val[1]+val[3]+", "+\
#                      val[0]+val[2]+val[3]+")"
#  
#          # with step
#          if len(val) == 5:
#  
#              if type == "imat":
#                  # get custom method for this
#                  node.include("get_mm", source="imat", target="imat")
#                  return "get_mm(%(name)s, " +\
#                          val[0]+val[1]+val[4]+"-1, "+val[2]+", "+\
#                          val[0]+val[3]+val[4]+"-1, 0, 1, %(name)s.ncols-1)"
#  
#          raise NotImplementedError
#  
#  
#      # double argument
#      elif len(node) == 2:
#  
#          # define types
#          type0 = node[0].type()
#          type1 = node[1].type()
#  
#          if type0 in ("int", "float"):
#              if type1 in ("int", "float"):
#                  val0 = node[0]["str"]+"-1"
#                  val1 = node[1]["str"]+"-1"
#                  type = node.type("int")
#              else:
#                  val0 = node[0]["str"]+"-1"
#                  val1 = node[1]["str"]
#                  type = node.type("irowvec")
#          else:
#              if type1 in ("int", "float"):
#                  val0 = node[0]["str"]
#                  val1 = node[1]["str"]+"-1"
#                  type = node.type("ivec")
#              else:
#                  val0 = node[0]["str"]
#                  val1 = node[1]["str"]
#                  type = node.type("imat")
#  
#  
#          val0 = "%(name)s.n_rows-1".join(val0.split("&$"))
#          val1 = "%(name)s.n_cols-1".join(val1.split("&$"))
#  
#          if type == "int":
#              return "%(name)s("+val0+", "+val1+")"
#  
#          elif type == "irowvec":
#  
#              if "&=" == val1:
#                  return "%(name)s.row("+val0+")"
#  
#              val1 = val1.split("&:")
#              if len(val1) == 4:
#                  return "%(name)s.submat("+val0+", "+\
#                          val1[0]+val1[1]+val1[3]+"-1, "+\
#                          val0+", "+\
#                          val1[0]+val1[2]+val1[3]+"-1)"
#  
#              if len(val1) == 5:
#                  node.include("get_mr", source="imat", target="irowvec")
#                  return "get_mr(%(name)s, " +val0[2]+", "+\
#                          val1[0]+val1[1]+val1[4]+"-1, "+\
#                          val1[0]+val1[3]+val1[4]+"-1)"
#  
#              raise NotImplementedError
#  
#          elif type == "ivec":
#  
#              if "&=" == val0:
#                  return "%(name)s.col("+val1+")"
#  
#              val0 = val0.split("&:")
#              if len(val1) == 4:
#                  return "%(name)s.col("+val1+").rows("+\
#                          val0[0]+val0[1]+val0[3]+"-1, "+\
#                          val0[0]+val0[2]+val0[3]+"-1)"
#  
#              if len(val1) == 5:
#                  node.include("get_mc", source="imat", target="ivec")
#                  return "get_mc(%(name)s, "+\
#                          val0[0]+val0[1]+val0[4]+"-1, "+\
#                          val0[0]+val0[3]+val0[4]+"-1, "+val1[2]+")"
#  
#              raise NotImplementedError
#  
#          elif type == "imat":
#  
#              val0 = val0.split("&:")
#              val1 = val1.split("&:")
#  
#              if len(val0) == 1:
#                  if len(val1) == 1:
#                      return "%(name)s"
#  
#                  elif len(val1) == 4:
#  
#                      return "%(name)s.cols("+\
#                          val1[0]+val1[1]+val1[3]+"-1, "+\
#                          val1[0]+val1[2]+val1[3]+"-1)"
#  
#                  elif len(val1) == 5:
#                      node.include("get_mm", source="imat", target="imat")
#                      return "get_mm(%(name)s, 0, 1, %(name)s.nrows-1, "+\
#                          val1[0]+val1[1]+val1[4]+"-1, "+val1[2]+", "+\
#                          val1[0]+val1[3]+val1[4]+"-1)"
#  
#              elif len(val0) == 4:
#                  if len(val1) == 1:
#                      return "%(name)s.rows("+\
#                          val0[0]+val0[1]+val0[3]+"-1, "+\
#                          val0[0]+val0[2]+val0[3]+"-1)"
#  
#                  elif len(val1) == 4:
#                      return "%(name)s.submat("+\
#                          val0[0]+val0[1]+val0[3]+"-1, "+\
#                          val1[0]+val1[1]+val1[3]+"-1, "+\
#                          val0[0]+val0[2]+val0[3]+"-1, "+\
#                          val1[0]+val1[2]+val1[3]+"-1)"
#  
#                  elif len(val1) == 5:
#                      node.include("get_mm", source="imat", target="imat")
#                      return "get_mm(%(name)s,"+\
#                          val0[0]+val0[1]+val0[3]+"-1, 1, "+\
#                          val0[0]+val0[3]+val0[3]+"-1, "+\
#                          val1[0]+val1[1]+val1[4]+"-1, "+val1[2]+", "+\
#                          val1[0]+val1[3]+val1[4]+"-1)"
#  
#  
#              elif len(val0) == 5:
#                  if len(val1) == 1:
#                      node.include("get_mm", source="imat", target="imat")
#                      return "get_mm(%(name)s, "+\
#                          val1[0]+val1[1]+val1[4]+"-1, "+val1[2]+", "+\
#                          val1[0]+val1[3]+val1[4]+"-1, "+\
#                          "0, 1, %(name)s.nrows-1)"
#  
#                  elif len(val1) == 4:
#                      node.include("get_mm", source="imat", target="imat")
#                      return "get_mm(%(name)s,"+\
#                          val0[0]+val0[1]+val0[4]+"-1, "+val0[2]+", "+\
#                          val0[0]+val0[3]+val0[4]+"-1, "+\
#                          val1[0]+val1[1]+val1[3]+"-1, 1, "+\
#                          val1[0]+val1[2]+val1[3]+"-1)"
#  
#                  elif len(val1) == 5:
#                      node.include("get_mm", source="imat", target="imat")
#                      return "get_mm(%(name)s,"+\
#                          val0[0]+val0[1]+val0[4]+"-1, "+val0[2]+", "+\
#                          val0[0]+val0[3]+val0[4]+"-1, "+\
#                          val1[0]+val1[1]+val1[4]+"-1, "+val1[2]+", "+\
#                          val1[0]+val1[3]+val1[4]+"-1)"
#  
#      raise NotImplementedError
#  
#  
#  
#  def Set(node):
#  
#      if len(node[0]) == 1:
#  
#          type = node[0][0].type()
#          if type in ("int", "float"):
#              val = node[0]["str"]+"-1"
#              type = "ivec"
#  
#          else:
#              val = node[0][0]["str"]
#              type = "imat"
#  
#          val = "(%(name)s.n_rows-1)".join(val.split("&$"))
#  
#          if "&:" not in val:
#  
#              if "&=" == val:
#                  return "%(name)s = %(1)s ;"
#  
#              return "%(name)s.row("+val+") = %(1)s ;"
#  
#          val = val.split("&:")
#  
#          # without step
#          if len(val) == 4:
#              return "%(name)s.cols("+\
#                      val[0]+val[1]+val[3]+"-1, "+\
#                      val[0]+val[2]+val[3]+"-1) = %(1)s ;"
#  
#          # with step
#          if len(val) == 5:
#  
#              if type == "fmat":
#                  # get custom method for this
#                  node.include("set_mm", source="imat", target="imat")
#                  return "set_mm(%(name)s, %(1)s" +\
#                          val[0]+val[1]+val[4]+"-1, "+val[2]+", "+\
#                          val[0]+val[3]+val[4]+"-1, 0, 1, %(name)s.ncols-1) ;"
#  
#          raise NotImplementedError
#  
#  
#      # double argument
#      elif len(node[0]) == 2:
#  
#          # define types
#          type0 = node[0][0].type()
#          type1 = node[0][1].type()
#  
#          if type0 in ("int", "float"):
#              if type1 in ("int", "float"):
#                  val0 = node[0][0]["str"]+"-1"
#                  val1 = node[0][1]["str"]+"-1"
#                  type = "int"
#              else:
#                  val0 = node[0][0]["str"]+"-1"
#                  val1 = node[0][1]["str"]
#                  type = "irowvec"
#          else:
#              if type1 in ("int", "float"):
#                  val0 = node[0][0]["str"]
#                  val1 = node[0][1]["str"]+"-1"
#                  type = "ivec"
#              else:
#                  val0 = node[0]["str"]
#                  val1 = node[1]["str"]
#                  type = "imat"
#  
#          val0 = "%(name)s.n_rows-1".join(val0.split("&$"))
#          val1 = "%(name)s.n_cols-1".join(val1.split("&$"))
#  
#          if type == "int":
#              return "%(name)s("+val0+", "+val1+") = %(1)s ;"
#  
#          elif type == "irowvec":
#  
#              if "&=" == val1:
#                  return "%(name)s.row("+val0+") = %(1)s ;"
#  
#              val1 = val1.split("&:")
#              if len(val1) == 4:
#                  return "%(name)s.submat("+val0+", "+\
#                          val1[0]+val1[1]+val1[3]+"-1, "+\
#                          val0+", "+\
#                          val1[0]+val1[2]+val1[3]+"-1) = %(1)s ;"
#  
#              if len(val1) == 5:
#                  node.include("set_mr", source="imat", target="irowvec")
#                  return "set_mr(%(name)s, %(1)s, " +val0[2]+", "+\
#                          val1[0]+val1[1]+val1[4]+"-1, "+\
#                          val1[0]+val1[3]+val1[4]+"-1) ;"
#  
#              raise NotImplementedError
#  
#          elif type == "ivec":
#  
#              if "&=" == val0:
#                  return "%(name)s.col("+val1+") = %(1)s ;"
#  
#              val0 = val0.split("&:")
#              if len(val1) == 4:
#                  return "%(name)s.submat("+\
#                          val0[0]+val0[1]+val0[3]+"-1, "+\
#                          val1+", "+\
#                          val0[0]+val0[2]+val0[3]+"-1, "+\
#                          val1+") = %(1)s ;"
#  
#              if len(val1) == 5:
#                  node.include("set_mc", source="imat", target="ivec")
#                  return "get_mc(%(name)s, %(1)s, "+\
#                          val0[0]+val0[1]+val0[4]+"-1, "+\
#                          val0[0]+val0[3]+val0[4]+"-1, "+val1[2]+") ;"
#  
#              raise NotImplementedError
#  
#          elif type == "imat":
#  
#              val0 = val0.split("&:")
#              val1 = val1.split("&:")
#  
#              if len(val0) == 1:
#                  if len(val1) == 1:
#                      return "%(name)s"
#  
#                  elif len(val1) == 4:
#  
#                      return "%(name)s.cols("+\
#                          val1[0]+val1[1]+val1[3]+"-1, "+\
#                          val1[0]+val1[2]+val1[3]+"-1) = %(1)s ;"
#  
#                  elif len(val1) == 5:
#                      node.include("set_mm", source="imat", target="imat")
#                      return "set_mm(%(name)s, %(1)s, "+\
#                          "0, 1, %(name)s.nrows-1, "+\
#                          val1[0]+val1[1]+val1[4]+"-1, "+val1[2]+", "+\
#                          val1[0]+val1[3]+val1[4]+"-1) ;"
#  
#              elif len(val0) == 4:
#                  if len(val1) == 1:
#                      return "%(name)s.rows("+\
#                          val0[0]+val0[1]+val0[3]+"-1, "+\
#                          val0[0]+val0[2]+val0[3]+"-1) = %(1)s ;"
#  
#                  elif len(val1) == 4:
#                      return "%(name)s.submat("+\
#                          val0[0]+val0[1]+val0[3]+"-1, "+\
#                          val1[0]+val1[1]+val1[3]+"-1, "+\
#                          val0[0]+val0[2]+val0[3]+"-1, "+\
#                          val1[0]+val1[2]+val1[3]+"-1) = %(1)s ;"
#  
#                  elif len(val1) == 5:
#                      node.include("set_mm", source="imat", target="imat")
#                      return "set_mm(%(name)s, %(1)s, "+\
#                          val0[0]+val0[1]+val0[3]+"-1, 1, "+\
#                          val0[0]+val0[3]+val0[3]+"-1, "+\
#                          val1[0]+val1[1]+val1[4]+"-1, "+val1[2]+", "+\
#                          val1[0]+val1[3]+val1[4]+"-1) ;"
#  
#  
#              elif len(val0) == 5:
#                  if len(val1) == 1:
#                      node.include("set_mm", source="imat", target="imat")
#                      return "set_mm(%(name)s, %(1)s, "+\
#                          val1[0]+val1[1]+val1[4]+"-1, "+val1[2]+", "+\
#                          val1[0]+val1[3]+val1[4]+"-1, "+\
#                          "0, 1, %(name)s.nrows-1) ;"
#  
#                  elif len(val1) == 4:
#                      node.include("set_mm", source="imat", target="imat")
#                      return "set_mm(%(name)s, %(1)s, "+\
#                          val0[0]+val0[1]+val0[4]+"-1, "+val0[2]+", "+\
#                          val0[0]+val0[3]+val0[4]+"-1, "+\
#                          val1[0]+val1[1]+val1[3]+"-1, 1, "+\
#                          val1[0]+val1[2]+val1[3]+"-1) ;"
#  
#                  elif len(val1) == 5:
#                      node.include("set_mm", source="imat", target="imat")
#                      return "set_mm(%(name)s, %(1)s, "+\
#                          val0[0]+val0[1]+val0[4]+", "+val0[2]+", "+\
#                          val0[0]+val0[3]+val0[4]+", "+\
#                          val1[0]+val1[1]+val1[4]+", "+val1[2]+", "+\
#                          val1[0]+val1[3]+val1[4]+") ;"
#  
#      raise NotImplementedError
#  
