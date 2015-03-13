
Type = "std::complex<double>"
Ifloat = "%(value)s"
Var = "%(name)s"

def Assign(node):
    node.suggest("complex")
    return "%(0)s(0., %(1)s) ;"
