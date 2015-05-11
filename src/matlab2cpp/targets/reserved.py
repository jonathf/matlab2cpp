"""
Reserved translation rules

The module will always check if the specific "<class>_<name>" name
exists before finding the generic "<class>" name.
"""
import vec_common, rowvec_common, mat_common, cube_common

# List of function names that should be handled by reserved.py:
reserved = {
"i", "and", "or", "not", "all", "any",
"false", "true", "pi", "inf", "Inf", "nan", "NaN",
"eye", "flipud", "length", "max", "min", "size",
"transpose", "ctranspose",
"abs",
"zeros", "round", "return", "rand", "floor",
"_conv_to", "_resize_", "_vectorise",
}

# Common attribute

Assign = "%(0)s = %(1)s ;"

def Declare(node):
    raise ValueError("Variable name '%s' is reserved."%node["name"]\
            +"\nPlease rename variable.")

def Var(node):
    raise ValueError("Variable name '%s' is reserved."%node["name"]\
            +"\nPlease rename variable.")


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

    if node[0].type == "TYPE":
        return "size(%(0)s)"

    var = node[0]
    if var.cls != "Var":
        var = var.auxiliary()
    var = str(var)

    if len(node) > 1:

        node.type = "int"
        arg2 = node[1]["value"]
        if arg2 == "1":
            return var+".n_rows"
        if arg2 == "2":
            return var+".n_cols"
        if arg2 == "3":
            return var+".n_slice"

    elif node[0].dim in (1,2):
        node.type = "int"
        return var+".n_elem"

    elif node[0].dim == 3:
        node.type = "ivec"
        return "{%(0)s.n_rows, %(0)s.n_cols}"

    name = node[0]["name"]
    node.error(
            "'size(%s)'\t\t illigal type (%s)" \
                    % (name, type))

    return "<error:size(%(0)s)>"

def Assigns_size(node):

    assert node[-1].cls == "Get"

    val = node[-1][0]
    if val.cls != "Var":
        val = val.auxiliary()
    val = str(val)

    if len(node)==3:
        node[0].suggest("int")
        node[1].suggest("int")

        return "%(0)s = " +val+ ".n_rows ;\n%(1)s = " +val+ ".n_cols ;"

    if len(node)==4:

        node[0].suggest("int")
        node[1].suggest("int")
        node[2].suggest("int")

        rows, cols, slices = map(str, node[0])
        return  "%(0)s = "+val+".n_rows ;\n"+\
                "%(1)s = "+val+".n_cols ;\n"+\
                "%(2)s = "+val+".n_slice ;"

    raise NotImplementedError

def Get_length(node):
    node.type = "int"
    return "length(%(0)s)"


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

    node[0].suggest((0, var.mem))
    node[1].suggest("int")

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

    node[0].suggest((0, var.mem))
    node[1].suggest("int")

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

    if len(node) == 1:
        node.type = "vec"
        return "arma::zeros<vec>(%(0)s)"
    if len(node) == 2:
        node.type = "mat"
        return "arma::zeros<mat>(%(0)s, %(1)s)"
    if len(node) == 3:
        node.type = "cube"
        return "arma::zeros<cube>(%(0)s, %(1)s, %(2)s)"

    raise NotImplementedError

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

    return "arma::floor(%(0)s)"


def Get__conv_to(node):
    return "conv_to<%(type)s>::from(%(0)s)"

def Get__resize(node):
    return "arma::resize(", ", ", ")"

def Get__vectorise(node):
    return "arma::vectorise(", ", ", ")"
