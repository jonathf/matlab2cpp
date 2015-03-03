
Type = "std::complex<double>"
Int = "%(value)s"
Var = "%(name)s"

def Assign(node):
    node.suggest("complex")
    node[0].declare()
    return "%(0)s(0., %(1)s) ;"
