Var_i = "cx_double"
Get_linspace = "rowvec"

def Get_abs(node):
    node.type = node[0].type

def Get_zeros(node):

    node.type = "uword"
    dim, mem = node.suggest_datatype()

    # set memory type
    if not (mem is None):
        node.mem = mem
    else:
        node.mem = 3

    # reset to uword if arg of array-node
    if node.group.cls in ("Get", "Cget", "Fget", "Nget", "Sget", "Set", "Cset",
            "Fset", "Nset", "Sset") and node.group.num:
        node.mem = 0

    # one argument
    if len(node) == 1:

        # arg input is vector
        if node[0].num and node[0].dim in (1,2):
            pass

        else:

            # use suggestions or defualts
            if dim in (1,2,3):
                node.dim = dim
            else:
                node.dim = 1 # default

    # double argument creates colvec/rowvec/matrix depending on context
    elif len(node) == 2:

        # use matrix, if suggested
        if dim == 3:
            node.dim = 3

        # use colvec if first index is '1'
        elif node[0].cls == "Int" and node[0].value == "1":
            node.dim = 1

        # use rowvec if second index is '1'
        elif node[1].cls == "Int" and node[1].value == "1":
            node.dim = 2

        # default to matrix
        else:
            node.dim = 3

    # triple arg create cube
    elif len(node) == 3:
        node.dim = 4

Get_ones = Get_zeros

Get_eye = "mat"
