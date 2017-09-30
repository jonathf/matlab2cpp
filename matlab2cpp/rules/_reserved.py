"""
Reserved translation rules

See :py:attr:`rules.reserved <matlab2cpp.rules.reserved>` for a collection of
set of the various reserved words implemented into matlab2cpp.
"""

import matlab2cpp as mc

# List of function names that should be handled by reserved.py:
reserved = {
    "and", "or", "not", "all", "any", "isequal",
    "false", "true", "pi", "inf", "Inf", "nan", "NaN",
    "eps", "exp", "log", "log2", "log10", "power", "floor", "ceil", "fix",
    "cos", "acos", "cosh", "acosh",
    "sin", "asin", "sinh", "asinh", "mod",
    "eye", "fliplr", "flipud", "length", "max", "min", "size", "chol",
    "trace", "transpose", "ctranspose",
    "abs", "sqrt", "nextpow2", "fft", "ifft", "fft2", "ifft2", "hankel",
    "zeros", "ones", "round", "return", "rand",
    "qr",
    "clear", "close", "clc", "clf", "more", "format",
    "_conv_to", "_reshape", "reshape",
    "interp1", "linspace", "varargin",
    "sum", "cumsum", "conj", "real", "imag",
    "tic", "toc", "diag", "tril", "triu",
    "disp", "fprintf", "error", "convmtx", "conv2",
    "figure", "clf", "cla", "show", "xlabel", "ylabel", "hold", "load",
    "title", "plot", "imshow", "imagesc", "wigb", "colorbar",
    "xlim", "ylim", "caxis", "axis", "grid", "subplot", "colormap",
    "_splot", "logspace", "find", "unique", "intersect", "isempty", "sortrows",
}

# Common attribute

from .assign import Assign
#Assign = "%(0)s = %(1)s ;"

def Var(node):
    return "%(name)s"

Var_pi = "datum::pi"
Var_true = "1"
Var_false = "0"
Var_inf = "datum::inf"
Var_Inf = "datum::inf"
Var_nan = "datum::nan"
Var_NaN = "datum::nan"
Var_eps = "datum::eps"

def Get_NaN(node):
    return "arma::zeros(", ", ", ") * datum::nan"

def conv_to(str, type):
    return "arma::conv_to<" + type +  ">::from(" + str + ")"

def Assign_elemwise_(node):

    if node[0].type != node[1].type:

        if node[0].dim == 0 and node[1].dim == 0:
            return "%(0)s = " + node[0].type + "(%(1)s) ;"

        if node[0].dim == 0 and node[1].dim > 0:
            if node[0].mem != node[1].mem:
                return "%(0)s = " + node[0].type + "(arma::as_scalar(%(1)s)) ;"
            return "%(0)s = arma::as_scalar(%(1)s) ;"

        if node[0].mem != node[1].mem:
            return "%(0)s = arma::conv_to<" + node[0].type + ">::from(%(1)s) ;"

    return "%(0)s = %(1)s ;"

def Get_exp(node):
    node.type = node[0].type
    # scalar done through std
    if node[0].dim == 0 and node[0].mem != 4:
        node.include("cmath")
        return "std::exp(", ", ", ")"

    return "arma::exp(", ", ", ")"

def Get_log(node):
    node.type = node[0].type
    # scalar done through std
    if node[0].dim == 0 and node[0].mem != 4:
        node.include("cmath")
        return "std::log(", ", ", ")"
    return "arma::log(", ", ", ")"

def Get_log2(node):
    node.type = node[0].type
    if node[0].dim == 0 and node[0].mem != 4:
        node.include("cmath")
        return "std::log(%(0)s)/std::log(2)"
        #seems like it is a C++11 feature
        #return "std::log2(", ", ", ")"
    return "arma::log2(", ", ", ")"

def Get_log10(node) :
    node.type = node[0].type
    if node[0].dim == 0 and node[0].mem != 4:
        node.include("cmath")
        return "std::log10(", ", ", ")"
    return "arma::log10(", ", ", ")"

def Get_power(node):
    node.type = node[0].type
    if node[0].dim == 0 and node[0].mem != 4:
        node.include("cmath")
        return "std::pow(", ", ", ")"
    return "arma::pow(", ", ", ")"

def Get_floor(node):
    # unknown input
    #if node[0].type == "TYPE":
    #    return "floor(", ", ", ")"
    node.type = node[0].type

    # scalar done through std
    if node[0].dim == 0 and node[0].mem != 4:
        node.include("cmath")
        return "std::floor(", ", ", ")"

    return "arma::floor(", ", ", ")"

def Get_ceil(node):
    node.type = node[0].type
    # scalar done through std
    if node[0].dim == 0 and node[0].mem != 4:
        node.include("cmath")
        return "std::ceil(%(0)s)"

    return "arma::ceil(%(0)s)"

def Get_round(node):
    node.type = node[0].type
    assert len(node)<3

    # number of decimals to retain
    if len(node) == 2:
        decimals = str(node[1])
    else:
        decimals = "0"

    # int and uword do not have decimals
    if node[0].mem < 2:
        return "%(0)s"

    # hack to cut-off for scalars
    if node[0].dim == 0:
        node.include("cmath")
        if decimals == "0":
            return "std::round(%(0)s)"
        return "std::round(%(0)s*std::pow(10, %(1)s))*std::pow(10, -%(1)s)"

    # hack for cut-off for array-type
    if decimals == "0":
        return "arma::round(%(0)s)"
    return "arma::round(%(0)s*std::pow(10, %(1)s))*std::pow(10, -%(1)s)"

def Get_fix(node):
    node.type = node[0].type

    if node[0].mem < 2:
        return "%(0)s"

    if node[0].dim == 0 and node[0].mem != 4:
        node.include("mconvert")
        return "m2cpp::fix(%(0)s)"

    return "arma::trunc(%(0)s)"

def Assign_fix(node):
    return Assign_elemwise_(node)

def Get_cos(node):
    node.type = node[0].type
    if node[0].dim == 0 and node[0].mem != 4:
        node.include("cmath")
        return "std::cos(", ", ", ")"
    return "arma::cos(", ", ", ")"

def Get_acos(node):
    node.type = node[0].type
    if node[0].dim == 0 and node[0].mem != 4:
        node.include("cmath")
        return "std::acos(", ", ", ")"
    return "arma::acos(", ", ", ")"

def Get_cosh(node):
    node.type = node[0].type
    if node[0].dim == 0 and node[0].mem != 4:
        node.include("cmath")
        return "std::cosh(", ", ", ")"
    return "arma::cosh(", ", ", ")"

def Get_acosh(node):
    node.type = node[0].type
    if node[0].dim == 0 and node[0].mem != 4:
        node.include("cmath")
        #is a C++11 feature
        return "std::acosh(", ", ", ")"
    return "arma::acosh(", ", ", ")"

def Get_sin(node):
    node.type = node[0].type
    if node[0].dim == 0 and node[0].mem != 4:
        node.include("cmath")
        return "std::sin(", ", ", ")"
    return "arma::sin(", ", ", ")"

def Get_asin(node):
    node.type = node[0].type
    if node[0].dim == 0 and node[0].mem != 4:
        node.include("cmath")
        return "std::asin", ", ", ")"
    return "arma::asin(", ", ", ")"

def Get_sinh(node):
    node.type = node[0].type
    if node[0].dim == 0 and node[0].mem != 4:
        node.include("cmath")
        return "std::sinh", ", ", ")"
    return "arma::sinh(", ", ", ")"

def Get_asinh(node):
    node.type = node[0].type
    if node[0].dim == 0 and node[0].mem != 4:
        node.include("cmath")
        return "std::asinh", ", ", ")"
    return "arma::asinh(", ", ", ")"

# Special handle of 'i'-variable
""" removed from reserved: "i",
def Var_i(node):
    return "cx_double(0, 1)"
"""

def Get_mod(node):
    node.type = node[0].type
    if node[0].dim == 0 and node[0].mem != 4:
        return "", " __percent__ ", ""
    return "mod(", ", ", ")"

def Get_abs(node):
    node.type = node[0].type
    if len(node) and node[0].dim == 0:
        if node[0].mem == 4: #cx_double
            node.include("m2cpp")
            return "abs(m2cpp::smat(%(0)s))"
        node.include("cmath")
        return "std::abs(", ", ", ")"
    return "abs(", ", ", ")"

def Get_sqrt(node):
    node.type = node[0].type
    #if len(node) > 0 ...
    if len(node) and node[0].cls == "Neg" and len(node[0]) == 1:
        return "cx_double(0, " + node[0][0].str + ")"
    return "sqrt(", ", ", ")"

def Get_and(node):
    return "(", "*", ")"

def Get_or(node):
    return "("+"+".join(["%(" + i +")s*%(" + i + ")s" \
            for i in xrange(len(node))])+")"

def Get_not(node):
    assert len(node) == 1
    if not node[0].num:
        return "not(%(0)s)"
    return "(%(0)s == 0)"

def Get_any(node):
    if not node[0].num:
        return "any(", ", ", ")"

    # unknown datatype
    if node[0].dim == 0:
        return "%(0)s"

    return "any(", ", ", ")"

def Get_all(node):

    # unkonwn datatype
    if not node[0].num:
        return "all(", ", ", ")"

    # scalar value
    if node[0].dim == 0:
        return "%(0)s"

    return "all(", ", ", ")"

def Get_isequal(node):
    return "%(0)s == %(1)s"

def Var_return(node):

    # multi-return does not return a value
    if node.func.backend == "func_returns":
        return "return"
    return "return " + str(node.func[0])


def Get_size(node):

    # unknown input
    if node[0].type == "TYPE" or node.parent.cls == "Assigns":
        return "size(", ", ", ")"

    var = str(node[0])

    # multiple args
    if len(node) > 1:

        # determine ax from second arg
        arg2 = node[1].value
        if arg2 == "1":
            return var+".n_rows"
        if arg2 == "2":
            return var+".n_cols"
        if arg2 == "3":
            return var+".n_slices"

    # colvec or rowvec
    elif node[0].dim in (1,2):
        #if node.parent.backend == "reserved" and\
        #  node.parent.name in ("min", "max"):
        #    return var+".n_elem"

        #if node[0].dim == 1:
        #    return "%(0)s.n_elem, 1"
        #elif node[0].dim == 2:
        #    return "1, %(0)s.n_elem"
        #return var+".n_elem"

        if node.parent.cls == "Get":
            if node.parent.backend in ("reserved", "func_return",
                "func_returns", "func_lambda", "unknown"):
                return "%(0)s.n_rows, %(0)s.n_cols"

        # inline calls moved to own line
        if node.parent.cls not in ("Statement", "Assign"):
            return str(node.auxiliary())

        return "{%(0)s.n_rows, %(0)s.n_cols}"

    # matrix (returns two values)
    elif node[0].dim == 3:

        if node.parent.cls == "Get":
            if node.parent.backend in ("reserved", "func_return",
                    "func_returns", "func_lambda", "unknown"):
                return "%(0)s.n_rows, %(0)s.n_cols"
            return "%(0)s.n_rows-1, %(0)s.n_cols"

        # inline calls moved to own line
        if node.parent.cls not in ("Statement", "Assign"):
            return str(node.auxiliary())

        return "{%(0)s.n_rows, %(0)s.n_cols}"

    # cube (return three values)
    elif node[0].dim == 4:

        if node.parent.cls == "Get":
            if node.parent.backend in ("reserved", "func_return",
                    "func_returns", "func_lambda", "unknown"):
                return "%(0)s.n_rows, %(0)s.n_cols, %(0)s.n_slices"
            return "%(0)s.n_rows-1, %(0)s.n_cols-1, %(0)s.n_slices"

        # inline calls moved to own line
        if node.parent.cls not in ("Statement", "Assign"):
            return str(node.auxiliary())

        return "{%(0)s.n_rows, %(0)s.n_cols, %(0)s.n_slices}"

    return "size(", ", ", ")"

def Assign_size(node):
    num = node[-1][0].dim == 3 and "2" or "2"
    if len(node[-1]) == 2 and (node[-1][1].str == "1" or node[-1][1].str == "2"):
        return "%(0)s = %(1)s ;"
    else:
        return "uword _%(0)s [] = %(1)s ;\n"+\
            "%(0)s = urowvec(_%(0)s, " + num + ", false) ;"

def Assigns_size(node):

    val = node[-1][0]
    # multi-assigned size to own line
    if val.cls != "Var":
        val = val.auxiliary()
    val = str(val)

    # suggest some types for matrix

    out = ""

    if node[0].str != '~':
        out += "%(0)s = " + val + ".n_rows;\n"
    if node[1].str != '~':
        out += "%(1)s = " + val + ".n_cols;\n"
    if len(node) == 4 and node[2] != '~':
        out += "%(2)s = " + val + ".n_slices;\n"
    #if len(node)==3:
    #    return 
    #    return "%(0)s = " +val+ ".n_rows ;\n%(1)s = " +val+ ".n_cols ;"

    if not (len(node) == 3 or len(node) == 4):
        raise NotImplementedError

    return out


    # suggest some types for cube
    #if len(node)==4:

    #    return  "%(0)s = "+val+".n_rows ;\n"+\
    #            "%(1)s = "+val+".n_cols ;\n"+\
    #            "%(2)s = "+val+".n_slices ;"



def Get_chol(node):
    return "", ", ", ""


def Assign_chol(node):
    lhs, rhs = node
    my_list = []
    for n in rhs:
        my_list.append(n.str)
    my_string = ", ".join(my_list)

    return "%(0)s = chol(" + my_string + ") ;"

def Assigns_chol(node):
    lhs = node[:-1]
    rhs = node[-1]

    if len(lhs) == 2:
        rhs_string = lhs[0].str + ", " + rhs.str
        # flip p bool value, to get same value as matlab
        ret_bool = lhs[1].str + " = !" + lhs[1].str + " ;"
        return lhs[1].str + " = chol(" + rhs_string + ") ;\n" + ret_bool

    # Default out. If more lhs values, then write new if statement
    lhs_list = [n.str for n in lhs]
    rhs_list = [n.str for n in rhs]
    lhs_string = ", ".join(lhs_list)
    rhs_string = ", ".join(rhs_list)
    return "[" + lhs_string + "]" + " = chol(" + rhs_string + ") ;"


def Get_unique(node):
    node.include("m2cpp")
    return "", ", ", ""

def Assign_unique(node):
    node.include("m2cpp")
    args = ", ".join([n.str for n in node])
    return "m2cpp::unique(" + args + ");"

def Assigns_unique(node):
    node.include("m2cpp")
    args = ", ".join([n.str for n in node])
    return "m2cpp::unique(" + args + ");"

def Get_sortrows(node):
    node.include("m2cpp")
    args = ", ".join([n.str for n in node])
    return "m2cpp::sortrows(" + args + ");"

def Get_intersect(node):
    node.include("m2cpp")
    return "", ", ", ""


def Assign_intersect(node):
    node.include("m2cpp")
    lhs, rhs = node
    my_list = []
    for n in rhs:
        my_list.append(n.str)
    my_string = ", ".join(my_list)

    return "%(0)s = m2cpp::intersect(" + my_string + ") ;"

def Assigns_intersect(node):
    node.include("m2cpp")
    rhs = ", ".join([n.str for n in node])
    return "m2cpp::intersect(" + rhs + ");"

def Get_length(node):
    # array-type uses n_elem
    if node.cls == "Var":
        return "%(0)s.n_elem"

    node.include("m2cpp")
    return "m2cpp::length(%(0)s)"

def Get_isempty(node):
    node.include("m2cpp")
    return "m2cpp::isempty(%(0)s)"

def Get_min(node):

    # non.numerical input
    if not all([n.num for n in node]):
        return "min(", ", ", ")"

    # everything scalar
    if all([(n.dim < 1) for n in node]):

        if any([n.mem == 4 for n in node]):
            node.include("m2cpp")
            nodes = map(str, node)
            nodes = ["m2cpp::smat<cx_double>(" + name + ")" for name in nodes]
            arg = ", ".join(nodes)
            return "arma::min(" + arg + ")"

        node.include("algorithm")
        return "std::min(", ", ", ")"

    # single arg
    if len(node) == 1:
        return "arma::min(%(0)s)"

    # two args
    if len(node) == 2:
        if node[0].dim and node[1].dim:
            return "arma::min(%(0)s, %(1)s)"

        if node[0].dim==0:
            return "arma::clamp(%(1)s, %(1)s.min(), %(0)s)"

        if node[1].dim==0:
            return "arma::clamp(%(0)s, %(0)s.min(), %(1)s)"


    # three args
    if len(node) == 3:
        if node[2].dim == 0:

            # assues third arg is int and sets axis
            val = node[2].value
            if val == "1":
                return "arma::min(%(0)s, 1)"
            elif val == "2":
                return "arma::min(%(0)s, 0)"

            return "arma::min(%(0)s, %(2)s-1)"

    assert False

def Assigns_min(node):
    assert len(node) == 3

    var = node[2][0]

    # non-numerical assignment
    if not var.num:
        return "[", ", ", "] = min(", ") ;"

    # multi-assignmens on own line
    if var.cls != "Var":
        var = var.auxiliary()
    var = str(var)
    if node[0].str != '~':
        return "%(0)s = " + var + ".min(%(1)s) ;"
    else:
        return var + ".min(%(1)s);"

def Get_max(node):

    # non.numerical input
    if not all([n.num for n in node]):
        return "max(", ", ", ")"

    # everything scalar
    if all([(n.dim<1) for n in node]):

        if any([n.mem == 4 for n in node]):
            node.include("m2cpp")
            nodes = map(str, node)
            nodes = ["m2cpp::smat<cx_double>(" + name + ")" for name in nodes]
            arg = ", ".join(nodes)
            return "arma::max(" + arg + ")"

        # single element, uword (returned from size(a))
        #if len(node) == 1 and node[0].dim == 0:
        #    return "%(0)s"

        node.include("algorithm")
        return "std::max(", ", ", ")"

    # number of args is ...
    if len(node) == 1:
        return "arma::max(%(0)s)"

    if len(node) == 2:
        if node[0].dim and node[1].dim:
            return "arma::max(%(0)s, %(1)s)"

        if node[0].dim==0:
            return "arma::clamp(%(1)s, %(0)s, %(1)s.max())"

        if node[1].dim==0:
            return "arma::clamp(%(0)s, %(1)s, %(0)s.max())"

    if len(node) == 3:
        if node[2].dim == 0:

            # thrid argument sets axis to take max over
            val = node[2]["value"]
            if val == "1":
                return "arma::max(%(0)s, 1)"
            elif val == "2":
                return "arma::max(%(0)s, 0)"

            return "arma::max(%(0)s, %(2)s-1)"

    assert False

def Assigns_max(node):
    assert len(node) == 3

    # right hand side of assignment
    var = node[-1]

    # non-numerical input
    if not var.num:
        return "[", ", ", "] = max(", ") ;"

    # multi-assign max on own line
    if var.cls != "Var":
        var = var.auxiliary()
    var = str(var)

    if node[0].str != '~':
        return "%(0)s = " + var + ".max(%(1)s);"
    else:
        var + ".max(%(1)s);"

Var_eye = "1"

def Get_eye(node):

    # not numerical input
    if not node[0].num:
        return "eye(", ", ", ")"

    # single argument constructor
    if len(node) == 1:
        if node[0].dim == 0:
            return "arma::eye<%(type)s>(%(0)s, %(0)s)"
        return "arma::eye<%(type)s>(%(0)s(0), %(0)s(1))"

    # double arguments
    if len(node) == 2:
        return "arma::eye<%(type)s>(%(0)s, %(1)s)"

    raise NotImplementedError

def Get_trace(node):
    return "arma::trace(", ", ", ")"

def Get_transpose(node):
    """Simple transpose
    """

    return "arma::strans(%(0)s)"

def Get_ctranspose(node):
    """Complex transpose
    """

    return "arma::trans(%(0)s)"

def Get_fliplr(node):
    return "arma::fliplr(%(0)s)"

def Get_flipud(node):
    return "arma::flipud(%(0)s)"


def Get_ones(node):

    # one argument
    if len(node) == 1:
        #size as argument: zeros(size(A))
        if node[0].backend == "reserved" and node[0].name == "size":
            #Take the type of the LHS, normally it is the other way around
            if node.parent.cls == "Assign" and node.parent[0] != node:
                out = "arma::ones<" + node.parent[0].type + ">("
                return out, ", ", ")"
            #return "arma::ones<%(type)s>(", ", ", ")"

        #arg input is a scalar
        if node[0].num and node[0].dim == 0:
            #dim is matrix
            if node.dim == 3:
                return "arma::ones<%(type)s>(%(0)s, %(0)s)"

        # arg input is vector
        if node[0].num and node[0].dim in (1,2):

            # non-trivial variables moved out to own line
            if node[0].cls != "Var":
                node[0].auxiliary()

            # indexing arg as input
            if node.dim in (1,2):
                return "arma::ones<%(type)s>(%(0)s(0))"
            if node.dim == 3:
                return "arma::ones<%(type)s>(%(0)s(0), %(0)s(1))"
            if node.dim == 4:
                return "arma::ones<%(type)s>(%(0)s(0), %(0)s(1), %(0)s(2))"

    # two args where one vector and other "1" handled specially
    elif len(node) == 2:

        if node.dim == 3:
            return "arma::ones<%(type)s>(%(0)s, %(1)s)"

        if node.dim in (1,2):
            if node[0].cls == "Int" and node[0].value == "1":
                return "arma::ones<%(type)s>(%(1)s)"
            if node[1].cls == "Int" and node[1].value == "1":
                return "arma::ones<%(type)s>(%(0)s)"

    return "arma::ones<%(type)s>(", ", ", ")"


def Get_zeros(node):

    # one argument
    if len(node) == 1:

        #size as argument: zeros(size(A))
        if node[0].backend == "reserved" and node[0].name == "size":
            #Take the type of the LHS, normally it is the other way around
            if node.parent.cls == "Assign" and node.parent[0] != node:
                out = "arma::zeros<" + node.parent[0].type + ">("
                return out, ", ", ")"
            #return "arma::zeros<%(type)s>(", ", ", ")"

        #arg input is a scalar
        if node[0].num and node[0].dim == 0:
            #dim is matrix
            if node.dim == 3:
                return "arma::zeros<%(type)s>(%(0)s, %(0)s)"

        # arg input is vector
        if node[0].num and node[0].dim in (1,2):

            # non-trivial variables moved out to own line
            if node[0].cls != "Var":
                node[0].auxiliary()

            # indexing arg as input if vector
            if node.dim in (1,2):
                return "arma::zeros<%(type)s>(%(0)s(0))"
            if node.dim == 3:
                return "arma::zeros<%(type)s>(%(0)s(0), %(0)s(1))"
            if node.dim == 4:
                return "arma::zeros<%(type)s>(%(0)s(0), %(0)s(1), %(0)s(2))"

    # double argument creates colvec/rowvec/matrix depending on context
    elif len(node) == 2:

        if node.dim == 3:
            return "arma::zeros<%(type)s>(%(0)s, %(1)s)"

        if node.dim in (1,2):
            # use colvec if first index is '1'
            if node[0].cls == "Int" and node[0].value == "1":
                return "arma::zeros<%(type)s>(%(1)s)"

            # use rowvec if second index is '1'
            elif node[1].cls == "Int" and node[1].value == "1":
                return "arma::zeros<%(type)s>(%(0)s)"

    return "arma::zeros<%(type)s>(", ", ", ")"

def Get_qr(node):
    return "", ", ", ""

def Assign_qr(node):
    return "arma::qr(", ", ", ")"

def Assigns_qr(node):
    return "arma::qr(", ", ", ")"

def Var_rand(node):
    return "arma::randu<" + node.type + ">(1)"


def Get_rand(node):
    return "arma::randu<" + node.type + ">(", ", ", ")"

def Var_clear(node):
    #index = node.parent.children.index(node)
    #print(node.parent.parent.names)
    #del node.parent.parent.children[0]
    #print(node.parent.summary())
    #return ""
    return "// clear"

def Get_clear(node):
    return "// clear(", ", ", ")"

def Var_close(node):
    return "// close"

def Get_close(node):
    return "// close(", ", ", ")"

def Var_clc(node):
    return "// clc"

def Get_clc(node):
    return "// clc"

def Var_clf(node):
    return "// clf"

def Get_clf(node):
    return "// clf"

def Var_more(node):
    return "// more"

def Get_more(node):
    return "// more"

def Var_format(node):
    return "// format"

def Get_format(node):
    return "// format"

def Get__conv_to(node):
    return "conv_to<%(type)s>::from(%(0)s)"

def Get__reshape(node):
    return "%(value)s(", ", ", ")"

def Get_reshape(node):
    return "reshape(", ", ", ")"

def Get_nextpow2(node):
    node.include("m2cpp")
    return "m2cpp::nextpow2(", ", ", ")"


def Assign_fft(node):

    #conv = node[0].type == "mat"
    #conv = conv or node[0].type == "fmat"
    #conv = conv or node[0].type == "vec"
    #conv = conv or node[0].type == "fvec"
    #conv = conv or node[0].type == "rowvec"
    #conv = conv or node[0].type == "frowvec"

    if node[0].mem == 3:
        return "%(0)s = arma::conv_to<" + node[0].type + ">::from(%(1)s) ;"

    return "%(0)s = %(1)s ;"

def Assign_ifft(node):
    return Assign_fft(node)

def Get_fft(node):

    if node[0].mem != None:
        node.type = node[0].type

    # arma & matlab fft same for n_args in (1,2)
    if len(node) in (1,2):
        return "arma::fft(", ", ", ")"

    elif len(node) == 3:

        if node[0].dim in (1,2):
            return "arma::fft(%(0)s, %(1)s)"

        if node[1].cls == "Matrix":
            node.include("m2cpp")
            return "m2cpp::fft<" + node[0].type + ">(%(0)s, %(2)s)"
        else:
            node.include("m2cpp")
            return "m2cpp::fft<" + node[0].type + ">(", ", ", ")"

    else:
        node.error("Number of args in 'fft' should be between 1 and 3")



    return "arma::fft(", ", ", ")"

def Get_ifft(node):

    if node[0].mem != None:
        node.type = node[0].type

    # unknown input
    if not node.num:
        return "arma::ifft(", ", ", ")"

    if len(node) == 1:
        return "arma::ifft(%(0)s)"


    elif len(node) == 2:
        return "arma::ifft(%(0)s, %(1)s)"


    elif len(node) == 3:

        if node[0].dim in (1,2):
            return "arma::ifft(%(0)s, %(1)s)"

        if node[1].cls == "Matrix":
            node.include("m2cpp")
            return "m2cpp::ifft(%(0)s, %(2)s)"
        else:
            node.include("m2cpp")
            return "m2cpp::ifft(", ", ", ")"

    else:
        node.error("Number of args in 'ifft' should be between 1 and 3")

    if node[0].mem != 4:
        node.warning("Argument datatype of 'ifft' should be complex")

    return "arma::ifft(", ", ", ")"

def Get_fft2(node):

    if node[0].mem != None:
        node.type = node[0].type

    return "arma::fft2(", ", ", ")"

def Get_ifft2(node):

    if node[0].mem != None:
        node.type = node[0].type

    return "arma::ifft2(", ", ", ")"

def Assign_fft2(node):
    return Assign_fft(node)

def Assign_ifft2(node):
    return Assign_fft(node)


def Get_hankel(node):
    node.include("m2cpp")
    return "m2cpp::hankel(", ", ", ")"

def Get_interp1(node):

    if node.parent.cls == "Assign":
        out = "arma::interp1(%(0)s, %(1)s, %(2)s, " + node.parent[0].str

        if node[-1].type == "string":
            out = out + ", %(3)s)"
        else:
            out = out + ")"
    else:
        out = "arma::interp1(", ", ", ")"

    return out

def Assign_interp1(node):
    return "%(1)s ;"

def Get_linspace(node):
    return "arma::linspace<%(type)s>(", ", ", ")"


def Get_sum(node):

    arg = node[0]

    # unknown input
    if not arg.num or arg.dim == 0:
        node.error("sum over non-array")
        return "arma::sum(", ", ", ")"

    # second argument should be dim, matlab uses dim 1/2, and armadillo 0/1
    if len(node) == 2:
        return "arma::sum(", ", ", "-1)"
    elif len(node) == 1 and node[0].dim == 2:
        return "arma::as_scalar(arma::sum(%(0)s))"
    elif len(node) == 1 and node[0].dim == 1:
        return "arma::as_scalar(arma::sum(", ", ", "))"
    return "arma::sum(", ", ", ")"

def Get_cumsum(node):
    if len(node) < 2:
        return "cumsum(", ", ", ")"
    elif len(node) == 2:
        return "cumsum(%(0)s, %(1)s-1)"
    else:
        return "cumsum(", ", ", ")"

def Get_conj(node):
    if node.dim == 0:
        if node.mem == 4:
            node.include("complex")
            return "std::conj(", ", ", ")"
        else:
            return "%(0)s"

    return "arma::conj(", ", ", ")"

def Get_imag(node):
    return "arma::imag(", ", ", ")"

def Get_real(node):
    # output always real
    return "arma::real(", ", ", ")"

def Var_tic(node):
    return Get_tic(node)

def Get_tic(node):
    node.wall_clock()
    node.type = 'double'
    return "m2cpp::tic()"

def Assign_tic(node):
    node.wall_clock()
    node[0].type = 'double'
    return "%(0)s = m2cpp::tic();"

def Var_toc(node):
    return Get_toc(node)

def Get_toc(node):
    node.wall_clock()

    arg = ", ".join([n.str for n in node])

    if node.parent.cls != "Statement":
        return "m2cpp::toc(" + arg + ")"

    node.include("iostream")
    return 'std::cout << "Elapsed time = " << m2cpp::toc(' + arg + ') << std::endl'

def Get_diag(node):
    if node.dim == 3:
        return "diagmat(", ", ", ")"
    return "diagvec(", ", ", ")"

def Get_tril(node):
    return "trimatl(", ", ", ")"

def Get_triu(node):
    return "trimatu(", ", ", ")"

def Var_disp(node):
    return "// disp"

def Get_disp(node):
    node.include("iostream")

    if len(node) == 1:
        arg = node[0]
        if not arg.num or arg.dim == 0:
            return "std::cout << %(0)s << std::endl"
        else:
            return "%(0)s.print()"
    else:
        node.error("disp should take one argument")
    return "std::cout << ", "<< ", " << std::endl"

def Get_fprintf(node):
    """ Matlab's fprintf can write to file and screen... this is translated to printf (so only printing to screen)
    will give error if trying to write to file.
    """
    node.include("cstdio")
    return "std::printf(", ", ", ")"


def Get_error(node):
    node.include("iostream")

    return "std::cerr << ", "<< ", " << std::endl"

def Get_convmtx(node):
    node.include("m2cpp")
    return "m2cpp::convmtx(", ", ", ")"

def Get_conv2(node):
    node.include("m2cpp")
    return "m2cpp::conv2<%(type)s>(", ", ", ")"
    #return "m2cpp::conv2<" + node[0].type + "," + node[1].type + ">(", ", ", ")"

#SPlot reserved words
def Get_figure(node):
    node.plotting()
    return "_plot.figure(", ", ", ")"

def Var_hold(node):
    return Get_hold(node)

def Get_hold(node):
    node.plotting()
    if node and node[0].cls == "String":

        if node[0].value == "on":
            return "_plot.hold(1)"

        if node[0].value == "off":
            return "_plot.hold(0)"

        node.error('argument must either be "on" or "off"')

        return "_plot.hold(", ", ", ")"

    node.error("hold toggle not supported")
    return "_plot.hold(", ", ", ")"

def Var_load(node):
    return Get_load(node)

def Get_load(node):

    out = "load " + node.code
    if len(node) == 1:
        if node[0].cls == "String":
            name = str(node[0].value).split(".")[0]
            out = name + ".load(%(0)s)"
        else:
            out = "%(0)s.load(\"" + node.value + "\")"

    return out

def Var_clf(node):
    return Get_clf(node)

def Get_clf(node):
    node.plotting()
    return "_plot.clf(", ", ", ")"

def Var_cla(node):
    return Get_cla(node)

def Get_cla(node):
    node.plotting()
    return "_plot.cla(", ", ", ")"

def Get_show(node):
    node.plotting()
    return "_plot.show(", ", ", ")"

def Get_xlabel(node):
    node.plotting()
    return "_plot.xlabel(", ", ", ")"

def Get_ylabel(node):
    node.plotting()
    return "_plot.ylabel(", ", ", ")"

def Get_title(node):
    node.plotting()
    return "_plot.title(", ", ", ")"

def Get_plot(node):
    node.plotting()

    if len(node) > 2:
        state = True

        num_children = len(node)
        cur_child = 0

        out = ""
        while state:
            #if cur_child > 0 and cur_child < num_children:
            #    out += "\n"
            #elif cur_child >= num_children:
            #    break

            out += "_plot.plot("

            #add next two childen
            if (cur_child+2) <= num_children:
                out += "%(" + str(cur_child) + ")s, "
                cur_child += 1
                out += "%(" + str(cur_child) + ")s"
                cur_child += 1

            #test if linespec
            if cur_child < num_children and node[cur_child].type == "string":
                out += ", %(" + str(cur_child) + ")s"
                cur_child += 1
            elif cur_child < num_children and node[cur_child].type != "string":
                out += ""
            elif cur_child >= num_children:
                out += ""

            #add next two children
            if (cur_child+2) <= num_children:
                out += ", %(" + str(cur_child) + ")s, "
                cur_child += 1
                out += "%(" + str(cur_child) + ")s"
                cur_child += 1

            #test if linespec
            if cur_child < num_children and node[cur_child].type == "string":
                out += ", %(" + str(cur_child) + ")s"
                cur_child += 1
            elif cur_child < num_children and node[cur_child].type != "string":
                out += ""
            elif cur_child >= num_children:
                out += ""


            if (cur_child+1) <= num_children:
                out += ") ;\n"
            else:
                out += ")"
                state = False

        return out

    return "_plot.plot(", ", ", ")"

def Get_imshow(node):
    node.plotting()
    return "_plot.imshow(", ", ", ")"

def Get_imagesc(node):
    node.plotting()
    return "_plot.imagesc(", ", ", ")"

def Get_wigb(node):
    node.plotting()
    return "_plot.wigb(", ", ", ")"

def Var_colorbar(node):
    return Get_colorbar(node)

def Get_colorbar(node):
    node.plotting()
    return "_plot.colorbar(", ", ", ")"

def Get_xlim(node):
    """
Examples:
    >>> print(mc.qscript("xlim(0.0, 3.14)"))
    _plot.xlim(0.0, 3.14) ;
    _plot.show() ;
    >>> print(mc.qscript("xlim([0.0, 3.14])"))
    _plot.xlim(0.0, 3.14) ;
    _plot.show() ;
    """

    node.plotting()

    if len(node) == 1:
        arg = node[0]

        if arg.cls == "Matrix" and len(arg[0]) == 2:

            a,b = arg[0]
            return "_plot.xlim(" + str(a) + ", " + str(b) + ")"

        elif arg.cls != "Matrix" and arg.num and arg.dim>0:

            name1 = arg.name + "(0)"
            name2 = arg.name + "(1)"
            if arg.mem not in (2,3):
                name1 = "static_cast<double>(" + name1 + ")"
                name2 = "static_cast<double>(" + name2 + ")"

            return "_plot.xlim(" + name1 + ", " + name2 + ")"

    node.error("argument array type")
    return "_plot.xlim(", ", ", ")"

def Get_ylim(node):
    """
Examples:
    >>> print(mc.qscript("ylim(0.5,.7)"))
    _plot.ylim(0.5, 0.7) ;
    _plot.show() ;
    >>> print(mc.qscript("ylim([0.5,.7])"))
    _plot.ylim(0.5, 0.7) ;
    _plot.show() ;
    """

    node.plotting()

    if len(node) == 1:
        arg = node[0]

        if arg.cls == "Matrix" and len(arg[0]) == 2:
                a,b = arg[0]
                return "_plot.ylim(" + str(a) + ", " + str(b) + ")"

        elif arg.cls != "Matrix" and arg.num and arg.dim>0:

            name1 = arg.name + "(0)"
            name2 = arg.name + "(1)"
            if arg.mem not in (2,3):
                name1 = "static_cast<double>(" + name1 + ")"
                name2 = "static_cast<double>(" + name2 + ")"

            return "_plot.ylim(" + name1 + ", " + name2 + ")"

    node.error("argument array type")
    return "_plot.ylim(", ", ", ")"

def Get_caxis(node):
    """
    >>> print(mc.qscript("caxis(0, 3)"))
    _plot.caxis(0, 3) ;
    _plot.show() ;
    >>> print(mc.qscript("caxis([0, 3])"))
    _plot.caxis(0, 3) ;
    _plot.show() ;
    """

    node.plotting()

    if len(node) == 1:
        arg = node[0]

        if arg.cls == "Matrix" and len(arg[0]) == 2:
                a,b = arg[0]
                return "_plot.caxis(" + str(a) + ", " + str(b) + ")"

        elif arg.cls != "Matrix" and arg.num and arg.dim>0:

            name1 = arg.name + "(0)"
            name2 = arg.name + "(1)"
            if arg.mem not in (2,3):
                name1 = "static_cast<double>(" + name1 + ")"
                name2 = "static_cast<double>(" + name2 + ")"

            return "_plot.caxis(" + name1 + ", " + name2 + ")"

    node.error("argument array type")
    return "_plot.caxis(", ", ", ")"

def Get_axis(node):
    """
    >>> print(mc.qscript("axis(0, 3, -2, 4)"))
    _plot.axis(0, 3, -2, 4) ;
    _plot.show() ;
    >>> print(mc.qscript("axis([0, 3, -2, 4])"))
    _plot.axis(0, 3, -2, 4) ;
    _plot.show() ;
    """

    node.plotting()

    if len(node) == 1:
        arg = node[0]

        if arg.cls == "Matrix" and len(arg[0]) == 4:
                a,b,c,d = arg[0]
                return "_plot.axis(" + str(a) + ", " + str(b) + ", " + str(c) + ", " + str(d) + ")"

        elif arg.cls != "Matrix" and arg.num and arg.dim>0:

            name1 = arg.name + "(0)";
            name2 = arg.name + "(1)"
            name3 = arg.name + "(2)";
            name4 = arg.name + "(3)"
            if arg.mem not in (2,3):
                name1 = "static_cast<double>(" + name1 + ")"
                name2 = "static_cast<double>(" + name2 + ")"
                name3 = "static_cast<double>(" + name3 + ")"
                name4 = "static_cast<double>(" + name4 + ")"

            return "_plot.axis(" + name1 + ", " + name2 + ", " + name3 + ", " + name4 + ")"

    node.error("argument array type")
    return "_plot.axis(", ", ", ")"

def Var_grid(node):
    return Get_grid(node)

def Get_grid(node):
    node.plotting()

    if node and node[0].cls == "String":

        if node[0].value == "on":
            return "_plot.grid({{\"b\", \"on\"}})"

        if node[0].value == "off":
            return "_plot.grid({{\"b\", \"off\"}})"

        node.error('argument must either be "on" or "off"')

        return "_plot.grid(", ", ", ")"

    return "_plot.grid(", ", ", ")"

def Get_subplot(node):
    node.plotting()
    return "_plot.subplot(", ", ", ")"

def Get_colormap(node):
    node.plotting()

    if len(node) == 1:
        arg = node[0]

        if len(arg) == 0:
            name = str(arg)[:-2] + "(1)"
            return "_plot.colormap(" + name + ")"

    return "_plot.colormap(", ", ", ")"

def Get__splot(node):
    return "_plot.show()"

def Get_logspace(node):
    if len(node) == 2:
        return "logspace<%(type)s>(%(0)s, %(1)s, 50)"

    if len(node) == 3:
        return "logspace<%(type)s>(%(0)s, %(1)s, %(2)s)"

    return "logspace<%(type)s>(", ", ", ")"

def Get_find(node):
    return "find(", ", ", ") + 1"

if __name__ == "__main__":
    import doctest
    doctest.testmod()
