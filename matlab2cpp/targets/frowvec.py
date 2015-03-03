from arma import *

Type = "frowvec"

def Get(node):

    type = node[0].type()
    if type in ("int", "float"):
        val = node[0]["str"]+"-1"
        type = node.type("float")
    else:
        val = node[0]["str"]
    val = "%(name)s.n_cols".join(val.split("&$"))

    if "&:" not in val:

        if "&=" == val:
            return "%(name)s"
        return "%(name)s("+val+")"

    val = val.split("&:")

    # without step
    if len(val) == 4:
        return "%(name)s.subvec("+\
                val[0]+val[1]+val[3]+", "+\
                val[0]+val[2]+val[3]+")"

    # with step
    if len(val) == 5:

        if type == "frowvec":
            # get custom method for this
            node.include("get_mr", source="frowvec", target="frowvec")
            return "get_mr(%(name)s, 0, " +\
                    val[0]+val[1]+val[4]+"-1, "+val[2]+", "+\
                    val[0]+val[3]+val[4]+"-1)"

    raise NotImplementedError


def Set(node):

    type = node[0][0].type()
    if type in ("int", "float"):
        val = node[0]["str"]+"-1"
        type = "float"

    else:
        val = node[0][0]["str"]
        type = "frowvec"

    val = "(%(name)s.n_cols-1)".join(val.split("&$"))

    if "&:" not in val:

        if "&=" == val:
            return "%(name)s = %(1)s ;"

        return "%(name)s("+val+") = %(1)s ;"

    val = val.split("&:")

    # without step
    if len(val) == 4:
        return "%(name)s.subvec("+\
                val[0]+val[1]+val[3]+"-1, "+\
                val[0]+val[2]+val[3]+"-1) = %(1)s ;"

    # with step
    if len(val) == 5:

        if type == "frowvec":
            # get custom method for this
            node.include("set_mr", source="frowvec", target="frowvec")
            return "set_mr(%(name)s, %(1)s, 0, " +\
                    val[0]+val[1]+val[4]+"-1, "+val[2]+", "+\
                    val[0]+val[3]+val[4]+"-1) ;"

    raise NotImplementedError

