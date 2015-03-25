
Var = "%(name)s"

def Assign(node):

    t0 = node[0].type()
    t1 = node[1].type()

    if t0 == "TYPE" and t1 != "TYPE":
        node[0].suggest(t1)

    if node[1]["decomposed"]:
        return "%(0)s << %(1)s ;"

    return "%(0)s = %(1)s ;"

def Set(node):

    return "%(name)s(%(0)s) = %(1)s ;"

