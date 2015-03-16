
Type = "std::complex<double>"
Iint = "%(value)s"
Var = "%(name)s"

def Assign(node):
#      node.include("complex")
    node[0].suggest("iint")
    return "%(0)s(0., %(1)s) ;"
