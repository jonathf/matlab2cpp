"""
Reserved translation rules

The module will always check if the specific "<class>_<name>" name
exists before finding the generic "<class>" name.
"""

# List of function names that should be handled by reserved.py:
reserved = {
"i", "and", "or", "not", "all", "any",
"false", "true", "pi", "inf", "Inf", "nan", "NaN",
"eye", "flipud", "length", "max", "min", "size",
"transpose", "ctranspose",
"abs", "nextpow2", "fft", "ifft", "hankel",
"zeros", "round", "return", "rand", "floor",
"clear", "close", "plot", "hold",
"_conv_to", "_reshape",
"interp1"
}

# Common attribute

Assign = "%(0)s = %(1)s ;"

def Declare(node):
    raise ValueError("Variable name '%s' is reserved."%node["name"]\
            +"\nPlease rename variable.")

def Var(node):
    return "%(name)s"


Var_pi = "datum::pi"
Var_true = "1"
Var_false = "0"
Var_inf = "datum::inf"
Var_Inf = "datum::inf"
Var_nan = "datum::nan"
Var_NaN = "datum::nan"

# Special handle of 'i'-variable

Var_i = "cx_complex(0, 1)"

def Get_abs(node):
    node.type = node[0].type
    return "abs(", ", ", ")"

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

    node.type = node[0].type

    if node[0].dim == 0:
        return "%(0)s"

    if node.dim == 2:
        node.dim = 0
    elif node.dim == 3:
        if len(node) == 2:
            val = node[1]["value"]
            if val == "0":
                node.dim = 2
            elif val == "1":
                node.dim = 1
            else:
                node.num = False

    else:
        node.dim = node[0].dim-1

    return "any(", ", ", ")"

def Get_all(node):
    if not node[0].num:
        return "all(", ", ", ")"

    node.type = node[0].type

    if node[0].dim == 0:
        return "%(0)s"

    if node.dim == 2:
        node.dim = 0
    elif node.dim == 3:
        if len(node) == 2:
            val = node[1]["value"]
            if val == "0":
                node.dim = 2
            elif val == "1":
                node.dim = 1
            else:
                node.num = False

    else:
        node.dim = node[0].dim-1

    return "all(", ", ", ")"

def Var_return(node):
    if node.func["backend"] == "func_returns":
        return "%(name)s"
    return "%(name)s " + str(node.func[0])

def Get_size(node):

    if node[0].type == "TYPE" or node.parent.cls == "Assigns":
        return "size(", ", ", ")"

    var = str(node[0])
    if len(node) > 1:

        node.type = "uword"
        arg2 = node[1]["value"]
        if arg2 == "1":
            return var+".n_rows"
        if arg2 == "2":
            return var+".n_cols"
        if arg2 == "3":
            return var+".n_slices"

    elif node[0].dim in (1,2):
        node.type = "uword"
        return var+".n_elem"

    elif node[0].dim == 3:
        node.type = "urowvec"
        if node.parent.cls not in ("Statement", "Assign"):
            return str(node.auxiliary())

        node.parent.backend = "reserved"
        node.parent.name = "size"
        return "{%(0)s.n_rows, %(0)s.n_cols}"

    elif node[0].dim == 4:
        node.type = "urowvec"
        if node.parent.cls not in ("Statement", "Assign"):
            return str(node.auxiliary())

        node.parent.backend = "reserved"
        node.parent.name = "size"
        return "{%(0)s.n_rows, %(0)s.n_cols, %(0)s.n_slices}"

    return "size(", ", ", ")"

def Assign_size(node):
    num = node[-1][0].dim == 3 and "2" or "3"
    return "uword _%(0)s [] = %(1)s ;\n"+\
            "%(0)s = urowvec(_%(0)s, " + num + ", false) ;"

def Assigns_size(node):

    val = node[-1][0]
    if val.cls != "Var":
        val = val.auxiliary()
    val = str(val)

    if len(node)==3:
        node[0].suggest = "int"
        node[1].suggest = "int"

        return "%(0)s = " +val+ ".n_rows ;\n%(1)s = " +val+ ".n_cols ;"

    if len(node)==4:

        node[0].suggest = "int"
        node[1].suggest = "int"
        node[2].suggest = "int"

        return  "%(0)s = "+val+".n_rows ;\n"+\
                "%(1)s = "+val+".n_cols ;\n"+\
                "%(2)s = "+val+".n_slices ;"

    raise NotImplementedError

def Get_length(node):
    node.type = "uword"
    node.include("length")
    if node.cls == "Var":
        return "%(0)s.n_elem"

    return "m2cpp::length(%(0)s)"


def Get_min(node):

    if not all([n.num for n in node]):
        return "min(", ", ", ")"

    if all([(not n.mem) for n in node]):
        return "std::min(", ", ", ")"

    node.type = node[0].type

    if len(node) == 1:

        if node.dim == 2:
            node.dim = 0
        else:
            node.dim = node.dim-1

        return "arma::min(%(0)s)"

    if len(node) == 2:
        return "arma::min(%(0)s, %(1)s)"

    if len(node) == 3:
        if node[2].dim == 0:

            val = node[2]["value"]
            if val == "1":
                node.dim = 2
                return "arma::min(%(0)s, 1)"
            elif val == "2":
                node.dim = 1
                return "arma::min(%(0)s, 0)"

            node.num = False
            return "arma::min(%(0)s, %(2)s-1)"

    assert False

def Assigns_min(node):
    assert len(node) == 3

    var = node[2][0]

    if not var.num:
        return "[", ", ", "] = max(", ") ;"

    node[0].suggest = (0, var.mem)
    node[1].suggest = "int"

    if var.cls != "Var":
        var = var.auxiliary()
    var = str(var)

    return "%(0)s = " + var + ".min(%(1)s) ;"

def Get_max(node):

    if not all([n.num for n in node]):
        return "max(", ", ", ")"

    if all([(not n.mem) for n in node]):
        return "std::max(", ", ", ")"

    node.type = node[0].type

    if len(node) == 1:

        if node.dim == 2:
            node.dim = 0
        else:
            node.dim = node.dim-1

        return "arma::max(%(0)s)"

    if len(node) == 2:
        return "arma::max(%(0)s, %(1)s)"

    if len(node) == 3:
        if node[2].dim == 0:

            val = node[2]["value"]
            if val == "1":
                node.dim = 2
                return "arma::max(%(0)s, 1)"
            elif val == "2":
                node.dim = 1
                return "arma::max(%(0)s, 0)"

            node.num = False
            return "arma::max(%(0)s, %(2)s-1)"

    assert False

def Assigns_max(node):
    assert len(node) == 3

    var = node[2][0]

    if not var.num:
        return "[", ", ", "] = max(", ") ;"

    node[0].suggest = (0, var.mem)
    node[1].suggest = "int"

    if var.cls != "Var":
        var = var.auxiliary()
    var = str(var)

    return "%(0)s = " + var + ".max(%(1)s) ;"


Var_eye = "1"
def Get_eye(node):

    node.type = "mat"
    if len(node) == 1:
        if node[0].dim == 0:
            return "arma::eye<mat>(%(0)s, %(0)s)"
        return "arma::eye<mat>(%(0)s(0), %(0)s(1))"

    if len(node) == 2:
        return "arma::eye<mat>(%(0)s, %(1)s)"

    raise NotImplementedError

def Get_transpose(node):
    if node[0].dim == 1:
        node.type = (2, node[0].mem)
    elif node[0].dim == 2:
        node.type = (1, node[0].mem)
    else:
        node.type = node[0].type
    return "arma::trans(%(0)s)"

def Get_ctranspose(node):
    if node[0].dim == 1:
        node.type = (2, node[0].mem)
    elif node[0].dim == 2:
        node.type = (1, node[0].mem)
    else:
        node.type = node[0].type
    return "arma::strans(%(0)s)"


def Get_flipud(node):
    return "arma::flipud(%(0)s)"


def Get_zeros(node):

    if node.parent.cls == "Assign" and node.parent[0].type != "TYPE":
        node.type = node.parent[0].type

    elif len(node) == 1:
        node.type = "vec"

    elif len(node) == 2:
        node.type = "mat"

    elif len(node) == 3:
        node.type = "cube"

    if node[0].num and node[0].dim in (1,2):

        if node[0].cls != "Var":
            node[0].auxiliary()

        if node.dim in (1,2):
            return "arma::zeros<%(type)s>(%(0)s(0))"
        if node.dim == 3:
            return "arma::zeros<%(type)s>(%(0)s(0), %(0)s(1))"
        if node.dim == 4:
            return "arma::zeros<%(type)s>(%(0)s(0), %(0)s(1), %(0)s(2))"

    return "arma::zeros<%(type)s>(", ", ", ")"

def Get_round(node):

    assert len(node)<3

    if len(node) == 2:
        decimals = str(node[1])
    else:
        decimals = "0"

    if node[0].mem < 2:
        return "%(0)s"

    if node[0].dim == 0:
        node.include("math")
        if decimals == "0":
            return "std::round(%(0)s)"
        return "std::round(%(0)s*std::pow(10, %(1)s))*std::pow(10, -%(1)s)"

    if decimals == "0":
        return "arma::round(%(0)s)"
    return "arma::round(%(0)s*std::pow(10, %(1)s))*std::pow(10, -%(1)s)"

def Var_rand(node):
    node.type = "float"
    return "arma::randu(1)"

def Get_rand(node):

    type = node[0].type
    if type == "TYPE":
        return "arma::randu<TYPE>(", ", ", ")"

    if len(node) == 1:
        node.type = "vec"
        return "arma::randu<vec>(%(0)s)"

    elif len(node) == 2:
        node.type = "mat"
        return "arma::randu<mat>(%(0)s, %(1)s)"

    elif len(node) == 3:
        node.type = "cube"
        return "arma::randu<cube>(%(0)s, %(1)s, %(2)s)"
    else:
        raise NotImplementedError

def Get_floor(node):

    if node[0].mem > 1:
        node.type = (node[0].dim, 1)

    if node.dim == 0:
        return "std::floor(%(0)s)"

    return "arma::floor(%(0)s)"

def Var_clear(node):
    return "// clear"

def Get_clear(node):
    return "// clear(", ", ", ")"

def Var_close(node):
    return "// close"

def Get_close(node):
    return "// close(", ", ", ")"

def Var_plot(node):
    return "// plot"

def Get_plot(node):
    return "// plot(", ", ", ")"

def Var_hold(node):
    return "// hold"

def Get_hold(node):
    return "// hold(", ", ", ")"

def Get__conv_to(node):
    return "conv_to<%(type)s>::from(%(0)s)"

def Get__reshape(node):
    return "%(value)s(", ", ", ")"

def Get_nextpow2(node):
    node.include("nextpow2")
    return "m2cpp::nextpow2(", ", ", ")"

def Get_fft(node):

    if len(node) == 1:
        return "arma::fft(%(0)s)"

    elif len(node) == 2:
        return "arma::fft(%(0)s, %(1)s)"

    elif len(node) == 3:

        if node[2].cls == "Int":

            if node[2].value == "1":

                if node[1].cls == "Matrix" and len(node[1][0])==0:
                    return "arma::fft(%(0)s)"

                else:
                    return "arma::fft(%(0)s, %(1)s)"

            elif node[2].value == "2":

                if node[1].cls == "Matrix" and len(node[1][0])==0:
                    return "arma::transpose(arma::fft(arma::transpose(%(0)s)))"

                else:
                    return "arma::transpose(arma::fft(arma::transpose(%(0)s), %(1)s))"

            else:
                node.error("Third argument in 'fft' should either be '1' or '2'")

        else:
            node.warning("Third argument in 'fft' is assumed to be '1'")

    else:
        node.error("Number of args in 'fft' should be between 1 and 3")

    return "arma::fft(", ", ", ")"

def Get_ifft(node):

    if len(node) == 1:
        return "arma::ifft(%(0)s)"

    elif len(node) == 2:
        return "arma::ifft(%(0)s, %(1)s)"

    elif len(node) == 3:

        if node[2].cls == "Int":

            if node[2].value == "1":

                if node[1].cls == "Matrix" and len(node[1][0])==0:
                    return "arma::ifft(%(0)s)"

                else:
                    return "arma::ifft(%(0)s, %(1)s)"

            elif node[2].value == "2":

                if node[1].cls == "Matrix" and len(node[1][0])==0:
                    return "arma::transpose(arma::ifft(arma::transpose(%(0)s)))"

                else:
                    return "arma::transpose(arma::ifft(arma::transpose(%(0)s), %(1)s))"

            else:
                node.error("Third argument in 'ifft' should either be '1' or '2'")

        else:
            node.warning("Third argument in 'ifft' is assumed to be '1'")

    else:
        node.error("Number of args in 'ifft' should be between 1 and 3")

    if node[0].mem != 4:
        node.warning("Argument datatype of 'ifft' should be complex")

    return "arma::ifft(", ", ", ")"

def Get_hankel(node):

    node.include("hankel")
    return "m2cpp::hankel(", ", ", ")"

def Get_interp1(node):
    node.include("interp1")
    node.error("'interp1' uses matlib library")
    if node[-1].cls == "String" and node[-1].value == "linear":
        return "matlib::interp1<matlib::row, double, double, double>"\
                "(%(0)s, %(1)s, %(2)s, matlib::linear)"

    return "interp1(", ", ", ")" 
