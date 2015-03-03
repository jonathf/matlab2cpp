
Var = "%(name)s"

def Assign(node):

    if node[1]["decomposed"]:
        return "%(0)s << %(1)s ;"
    return "%(0)s = %(1)s ;"

def Set(node):

    return "%(name)s(%(0)s) = %(1)s ;"

