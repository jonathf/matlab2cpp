from arma import *

Declare = "ivec %(name)s ;"

def Get(node):

    type = node[0].type()
    if type in ("int", "float"):
        val = node[0]["str"]+"-1"
        type = node.type("int")
    else:
        val = node[0]["str"]
    val = "%(name)s.n_rows".join(val.split("&$"))

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

        if type == "ivec":
            # get custom method for this
            node.include("get_mc", source="ivec", target="ivec")
            return "get_mc(%(name)s, " +\
                    val[0]+val[1]+val[4]+"-1, "+val[2]+", "+\
                    val[0]+val[3]+val[4]+"-1, 0)"

    raise NotImplementedError


def Set(node):

    type = node[0][0].type()
    if type in ("int", "float"):
        val = node[0]["str"]+"-1"
        type = "int"

    else:
        val = node[0][0]["str"]
        type = "ivec"

    val = "(%(name)s.n_rows-1)".join(val.split("&$"))

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

        if type == "ivec":
            # get custom method for this
            node.include("set_mc", source="ivec", target="ivec")
            return "set_mc(%(name)s, %(1)s" +\
                    val[0]+val[1]+val[4]+"-1, "+val[2]+", "+\
                    val[0]+val[3]+val[4]+"-1, 0) ;"

    raise NotImplementedError

