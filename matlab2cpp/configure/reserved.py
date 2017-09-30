Var_false = "int"
Var_true = "int"
Var_pi = "double"
Get_linspace = "rowvec"

def Get_exp(node):
    node.type = node[0].type

def Get_log(node):
    node.type = node[0].type

def Get_log2(node):
    node.type = node[0].type

def Get_log10(node):
    node.type = node[0].type

def Get_power(node):
    node.type = node[0].type

def Get_floor(node):
    node.type = node[0].type

def Get_ceil(node):
    node.type = node[0].type

def Get_fix(node):
    node.type = node[0].type

def Get_round(node):
    if len(node) == 1:
        #int, float, double, uword
        if node[0].dim == 0 and node[0].mem != 4:
            node.type = "double"
        #arma types
        elif node[0].dim != 0:
            node.type = node[0].type

def Get_cos(node):
    node.type = node[0].type

def Get_acos(node):
    node.type = node[0].type

def Get_cosh(node):
    node.type = node[0].type

def Get_acosh(node):
    node.type = node[0].type

def Get_sin(node):
    node.type = node[0].type

def Get_asin(node):
    node.type = node[0].type

def Get_sinh(node):
    node.type = node[0].type

def Get_asinh(node):
    node.type = node[0].type

def Get_sqrt(node):
    #if len(node) > 0 ...
    if len(node) and node[0].cls == "Neg":
        node.type = "cx_double"
    elif len(node):
        node.type = node[0].type

def Get_mod(node):
    node.type = node[0].type

def Get_abs(node):
    if node[0].type in ("cx_double", "cx_mat"):
        node.type = "mat"
    else:
        node.type = node[0].type

def Get_tic(node):
    node.type = "double"

def Assign_tic(node):
    node[0].declare.type = "double"
    node[0].type = "double"

def Get_toc(node):
    node.type = "double"

def Assign_toc(node):
    node[0].declare.type = "double"
    node[0].type = "double"

def Get_any(node):
    if not node[0].num:
        return

    node.type = node[0].type

    # colvec or rowvec
    if node.dim in (1,2):
        node.dim = 0

    # matrix
    elif node.dim == 3:

        # axis input decides by second input
        if len(node) == 2:

            if  node[1].cls == "Int":
                val = node[1].value
                if val == "1":
                    node.dim = 2
                elif val == "2":
                    node.dim = 1

            # problem if arg not explicit
            else:
                node.num = False

    # cube
    else:
        node.dim = 3

Get_all = Get_any

Get_isequal = "int"

def Get_size(node):

    # unknown input
    if node[0].type == "TYPE" or node.parent.cls == "Assigns":
        return

    var = str(node[0])

    # multiple args
    if len(node) > 1:
        
        # determine ax from second arg
        node.type = "uword"

    # colvec or rowvec
    elif node[0].dim in (1,2):
        """
        if node.parent.backend == "reserved" and\
          node.parent.name in ("min", "max"):
            node.type = "uword"
            return
        if len(node) == 1:
            node.type = "urowvec"
            return
        node.type = "uword"
        """
        
        node.type = "urowvec"

        if node.parent.backend == "reserved" and\
          node.parent.name in ("min", "max"):
            node.type = "uword"
            return
        if len(node) == 1:
            node.type = "urowvec"
            return

        if node.parent.cls == "Get":
            return

        # inline calls moved to own line
        if node.parent.cls not in ("Statement", "Assign"):
            return

        node.parent.backend = "reserved"
        node.parent.name = "size"
        
    # matrix (returns two values)
    elif node[0].dim == 3:
        node.type = "urowvec"

        if node.parent.backend == "reserved" and\
          node.parent.name in ("min", "max"):
            node.type = "uword"
            return

        if node.parent.cls == "Get":
            return

        # inline calls moved to own line
        if node.parent.cls not in ("Statement", "Assign"):
            return

        node.parent.backend = "reserved"
        node.parent.name = "size"

    # cube (return three values)
    elif node[0].dim == 4:
        node.type = "urowvec"

        if node.parent.cls == "Get":
            return

        # inline calls moved to own line
        if node.parent.cls not in ("Statement", "Assign"):
            return

        node.parent.backend = "reserved"
        node.parent.name = "size"

def Assigns_size(node):

    # suggest some types for matrix
    if len(node)==3:
        node[0].suggest = "int"
        node[1].suggest = "int"

    # suggest some types for cube
    if len(node)==4:

        node[0].suggest = "int"
        node[1].suggest = "int"
        node[2].suggest = "int"

def Get_length(node):
    node.type = "uword"

def Get_min(node):

    # everything scalar
    if not all([n.num for n in node]) or  all([(n.dim < 1) for n in node]):
        if any([n.mem == 4 for n in node]):
            node.type = "cx_mat"
        return

    node.type = node[0].type

    # single arg
    if len(node) == 1:

        # determine node dimensions
        if node.dim == 2:
            node.dim = 0
        else:
            node.dim = node.dim-1

    # three args
    if len(node) == 3:
        if node[2].dim == 0:

            # assues third arg is int and sets axis
            val = node[2].value
            if val == "1":
                node.dim = 2
            elif val == "2":
                node.dim = 1
            else:
                node.num = False
            
def Assigns_min(node):
    assert len(node) == 3

    var = node[2][0]

    # non-numerical assignment
    if not var.num:
        pass
    else:
        node[0].suggest = (0, var.mem)
        node[1].suggest = "int"

Get_max = Get_min

def Assigns_max(node):
    assert len(node) == 3

    # right hand side of assignment
    var = node[-1]

    # non-numerical input
    if not var.num:
        pass
    else:
        node[0].suggest = (0, var.mem)
        node[1].suggest = "int"

def Get_fliplr(node):
    if len(node) > 0:
        node.type = node[0].type

def Get_flipud(node):
    if len(node) > 0:
        node.type = node[0].type

def Get_eye(node):
    #set eye type to cx_mat if LHS is complex type
    if node.group.cls == "Assign" and node.group[0].mem == 4:
        node.type = "cx_mat"
    else:
        node.type = "mat"
    
def Get_diag(node):
    if len(node) > 0:
        if node[0].dim == 3:
            node.type = (1, node[0].mem)
        elif node[0].dim in (1, 2):
            node.type = (3, node[0].mem)

def Get_tril(node):
    if node[0].mem:
        node.type = (3, node[0].mem)

def Get_triu(node):
    if node[0].mem:
        node.type = (3, node[0].mem)
        
Var_eye = Get_eye

def Get_trace(node):
    node.type = node[0].type

def Get_transpose(node):
    """Simple transpose
    """

    # colvec -> rowvec 
    if node[0].dim == 1:
        node.type = (2, node[0].mem)

    # rowvec -> colvec
    elif node[0].dim == 2:
        node.type = (1, node[0].mem)

    else:
        node.type = node[0].type
    
def Get_ctranspose(node):
    """Complex transpose
    """

    # colvec -> rowvec 
    if node[0].dim == 1:
        node.type = (2, node[0].mem)

    # rowvec -> colvec
    elif node[0].dim == 2:
        node.type = (1, node[0].mem)

    else:
        node.type = node[0].type

def Get_zeros(node):

    node.type = "uword"
    dim, mem = node.suggest_datatype()
    
    # set memory type
    if not (mem is None):
        node.mem = mem
    else:
        node.mem = 3

    #if node.group.cls == "Matrix" and node.group.group.cls == "Assign" and len(node.group.group) == 2:
    #    if node.group.group[0].mem == 4:
    #        node.mem = 4

    # reset to uword if arg of array-node
    if node.group.cls in ("Get", "Cget", "Fget", "Nget", "Sget", "Set", "Cset",
            "Fset", "Nset", "Sset") and node.group.num:
        node.mem = 0
        if len(node) == 2 and node[0].cls == "Int" and node[0].value == "1":
            node.dim = 1
            return
    
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
                node.dim = 3 # default

    # double argument creates colvec/rowvec/matrix depending on context
    elif len(node) == 2:

        # use matrix, if suggested
        if dim == 3:
            node.dim = 3

        # use colvec if first index is '1'
        elif node[0].cls == "Int" and node[0].value == "1":
            node.dim = 2

        # use rowvec if second index is '1'
        elif node[1].cls == "Int" and node[1].value == "1":
            node.dim = 1

        # default to matrix
        else:
            node.dim = 3

    # triple arg create cube
    elif len(node) == 3:
        node.dim = 4

Get_ones = Get_zeros

Var_rand = "vec"

def Get_rand(node):

    # Get type from left hand side of assignment
    if node.group.cls == "Assign":
        if node.group[0].type != "TYPE":
            node.type = node.group[0].type
            return

    # one arg
    if len(node) == 1:
        node.type = "vec"

    # two args
    elif len(node) == 2:
        node.type = "mat"

    # three args -> cube
    elif len(node) == 3:
        node.type = "cube"

def Get_reshape(node):
    if node[0].mem:
        node.type = (3, node[0].mem)

def Get_nextpow2(node):
    node.type = "int"
    
def Get_fft(node):

    node.type = node[0].type
    if node.type != 'TYPE':
        node.mem = 4
    #if node.mem == 4:
    #    node.mem = 4
    #elif node.mem == 3:
    #    node.mem = 4

def Get_ifft(node):

    #assert(node[0].mem == 4)
    node.type = node[0].type
    if node.type != 'TYPE':
        node.mem = 4

    #if node.mem == 4:
    #    node.mem = 3
    #elif node.mem == 3:
    #    node.mem = 3

    # unknown input
    #if not node.num:
    #    pass
    #else:
    #    node.mem = 4


def Get_interp1(node):
    if len(node):
        node.type = node[0].type

def Get_sum(node):

    arg = node[0]

    # unknown input
    if not arg.num or arg.dim == 0:
        return

    node.type = arg.type

    # determine output dimensions
    if arg.dim == 2:
        dim = 0
    elif arg.dim == 3:
        # sum along an axis
        if len(node) == 2 and node[1].cls == "Int" and node[1].value == "2":
            dim = 1
        else:
            dim = 2
    else:
        if arg.dim == 3:
            dim = 2
        elif arg.dim == 2:
            arg.dim == 0
        else:
            dim = arg.dim-1
    node.dim = dim

def Get_cumsum(node):
    node.type = node[0].type

def Get_conj(node):
    node.type = node[0].type

def Get_real(node):
    if node[0].dim:
        node.type = (node[0].dim, 3)
    #arg = node[0]
    #
    # output always real
    #if arg.mem:
    #    node.type = (3, arg.mem)

def Get_convmtx(node):
    node.type = node[0].type

def Get_conv2(node):
    node.type = [node[0].type, node[1].type]

def Get_logspace(node):
    node.type = "rowvec"

def Get_find(node):
    node.type = "uvec"

Get_tic = "string"

Get_toc = "string"
