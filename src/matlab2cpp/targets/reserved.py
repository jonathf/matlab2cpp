"""
Reserved translation rules

The module will always check if the specific "<class>_<name>" name
exists before finding the generic "<class>" name.
"""

# List of function names that should be handled by reserved.py:
reserved = [
"eye", "flipud", "length", "max", "min", "size", "transpose",
"zeros", "round", "return", "rand", "floor", "pi", "conv_to",
]

# Common attribute

#  def Assignees(node):
#      node.parent["backend"] = "reserved"
#      return "", ", ", ""

def Declare(node):
    raise ValueError("Variable name '%s' is reserved."%node["name"]\
            +"\nPlease rename variable.")

def Var(node):
    raise ValueError("Variable name '%s' is reserved."%node["name"]\
            +"\nPlease rename variable.")


def Var_pi(node):
    return "datum::pi"

def Var_return(node):
    if node.func["backend"] == "func_returns":
        return "%(name)s"
    return "%(name)s " + str(node.func[0])

def Get_size(node):

    if node[0].type == "TYPE":
        return "size(%(0)s)"

    elif len(node) > 1:

        node.type = "int"
        arg2 = node[1]["value"]
        var = node[0]
        if arg2 == "1":
            return var+".n_rows"
        if arg2 == "2":
            return var+".n_cols"
        if arg2 == "3":
            return var+".n_slice"

    elif node[0].dim in (1,2):
        node.type = "int"
        return node[0]+".n_elem"

    elif node[0].dim == 3:
        node.type = "ivec"
        return "{%(0)s.n_rows, %(0)s.n_cols}"

    name = node[0]["name"]
    node.error(
            "'size(%s)'\t\t illigal type (%s)" \
                    % (name, type))

    return "<error:size(%(0)s)>"

def Assigns_size(node):

    if len(node[0])==2:

        node[0][0].suggest("int")
        node[0][1].suggest("int")
        if len(node[1]) == 0:
            val = str(node[1])
        else:
            val = str(node[1][0])

        return "%s = %s.n_rows ;\n%s = %s.n_cols ;" % \
                (node[0][0], val, node[0][1], val)

    if len(node[0])==3:

        node[0][0].suggest("int")
        node[0][1].suggest("int")
        node[0][2].suggest("int")
        if len(node[1]) == 0:
            val = str(node[1])
        else:
            val = str(node[1][0])
        rows, cols, slices = map(str, node[0])
        return  rows+" = "+val+".n_rows ;\n"+\
                cols+" = "+val+".n_cols ;\n"+\
                slices+" = "+val+".n_slice ;"

    raise NotImplementedError

def Get_length(node):
    node.type = "int"
    return "%(0)s.n_elem"


def Get_min(node):

    if len(node) == 1:

        if node[0].dim == 3:
            node.type = "ivec"
        elif node[0].dim in (1, 2):
            node.type = "int"

        return "arma::min(%(0)s)"

    if len(node) == 2:

        if node[0].dim == node[1].dim == 0:
            return "(%(0)s<%(1)s?%(0)s:%(1)s)"
        return "arma::min(%(0)s, %(1)s)"

    if len(node) == 3:

        if node[2].dim == 0:

            val = node[2]["value"]
            if val == "1":
                node.type = "irowvec"
            elif val == "2":
                node.type = "ivec"
            else:
                raise NotImplementedError

            return "arma::min(%(0)s, %(2)s-1)"

def Assigns_min(node):
    m_val = node[0][0]["name"]
    m_ind = node[0][1]["name"]
    return m_val + " = %(1)s.min("+m_ind+") ;\n"


def Get_max(node):

    if len(node) == 1:

        if node[0].dim == 3:
            node.type = "ivec"
        elif node[0].dim in (1,2):
            node.type = "int"

        return "arma::max(%(0)s)"

    if len(node) == 2:
        if node[0].dim == node[1].dim == 0:
            return "(%(0)s<%(1)s?%(1)s:%(0)s)"
        return "arma::max(%(0)s, %(1)s)"

    if len(node) == 3:

        if node[2].dim == 0:

            val = node[2]["value"]
            if val == "1":
                node.type = "irowvec"
            elif val == "2":
                node.type = "ivec"
            else:
                raise NotImplementedError

            return "arma::max(%(0)s, %(2)s-1)"

    raise NotImplementedError

def Assigns_max(node):
    m_val = node[0][0]["name"]
    m_ind = node[0][1]["name"]

    return m_val + " = %(1)s.min("+m_ind+") ;\n"

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
    else:
        raise NotImplementedError

def Get_floor(node):

    if node[0].mom > 1:
        node.type = (node[0].dim, 1)

    return "arma::floor(%(0)s)"


def Get_conv_to(node):
    return "conv_to<%(type)s>::from(%(0)s)"

