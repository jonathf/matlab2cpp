"""
Expressions

Nodes
-----
Expr : General expression
    Take the following form:
        Band, Bor, Colon, Ctranspose, Div, Eldiv, Elexp, Elmul,
        Elrdiv, End, Eq, Exp, Float, Ge, Get, Get2, Get3, Gt,
        Ifloat, Iint, Int, Land, Lor, Lt, Matrix, Minus, Mul, Ne,
        Neg, Not, Paren, Plus, Rdiv, String, Transpose, Var

Band : Bit-vise And-operator
    Example: "x && y"
    Contains: Expr, Expr, ...

Bor : Bit-vise Or-operator
    Example: "x || y"
    Contains: Expr, Expr, ...

Colon : Colon
    Example: "x:y"
    Example: "x:y:z"
    Contains: Expr, Expr, (Expr)

Ctranspose : Ctranspose
    Example: "x'"
    Contains: Expr

Div : Division
    Example: "x / y"
    Contains: Expr, Expr, ...

Eldiv : Element-wise division
    Example: "x ./ y"
    Contains: Expr, Expr, ...

Elexp : Element-wise exponent
    Example: "x .^ y"
    Contains: Expr, Expr, ...

Elmul : Element-wise multiplication
    Example: "x .* y"
    Contains: Expr, Expr, ...

Elrdiv : Element-wise right division
    Example: "x .\ y"
    Contains: Expr, Expr, ...

End : Special charracter: last element in range/array
    Example: "y(end)"

Eq : Equate (Truth-value)
    Example: "x == y"
    Contains: Expr, Expr

Exp : Exponent
    Example: "x ^ y"
    Contains: Expr, Expr, ...

Ge : Greater or equal
    Example: "x >= y"
    Contains: Expr

Gt : Greater than
    Example: "x > y"
    Contains: Expr, Expr

Land : Logical And
    Example: "x and y"
    Contains: Expr

Lor : Logical Or
    Example: "x or y"
    Contains: Expr

Lt : Lt
    Example: "x < y"
    Contains: Expr, Expr

Minus : Subtraction
    Example: "x - y"
    Contains: Expr, Expr, ...

Mul : Multiplication
    Example: "x * y"
    Contains: Expr, Expr, ...

Ne : Not equal
    Example: "x <> y"
    Contains: Expr, Expr

Neg : Negative
    Example: "-y"
    Contains: Expr

Not : Negation
    Example: "not y"
    Contains: Expr

Paren : Parenthesis
    Example: "(y)"
    Contains: Expr

Plus : Addition
    Example: "x + y"
    Contains: Expr, Expr, ...

Rdiv : Right devision
    Example: "x \ y"
    Contains: Expr

Transpose : Transpose
    Example: "y.'"
    Contains: Expr

Break : Break
    Example: "break"

Return : Return
    Example: "return"
"""

def operator_suggestions(node):
    if node.type() == "TYPE":
        type = node.propose()
        if type != "TYPE":
            for child in node:
                if child["class"] == "Var":
                    child.suggest(type)


Expr = "%(0)s"
Gets = "", ", ", ""
Paren = "(%(0)s)"

def End(node):

    pnode = node
    while pnode.parent["index"] != 0: pnode = pnode.parent

    if pnode.parent["class"] in ("Get", "Get2", "Get3", "Sets"):

        index = pnode.parent.children.index(pnode)

        if pnode.parent["class"] == "Sets":
            pnode = pnode.parent
        name = pnode = pnode.parent["name"]

        if index == 0:
            return name + ".n_rows"
        elif index == 1:
            return name + ".n_cols"
        elif index == 2:
            return name + ".n_slices"

    return "&$"

Break = "break"

def Return(node):
    func = node.func
    if func["backend"] == "func_returns":
        return "return"
    if func["backend"] == "func_lambda":
        return "return _retval"

    return "return " + func[1][0]["name"]



# simple operators
def Mul(node):
    operator_suggestions(node)
    return "", "*", ""

def Elmul(node):
    operator_suggestions(node)
    return "", ".*", ""

def Plus(node):
    operator_suggestions(node)
    return "", "+", ""

def Minus(node):
    operator_suggestions(node)
    return "", "-", ""

Gt      = "", ">", ""
Ge      = "", ">=", ""
Lt      = "", "<", ""
Le      = "", "<=", ""
Ne      = "", "~=", ""
Eq      = "", "==", ""
Band    = "", "&&", ""
Land    = "", "&", ""
Bor     = "", "||", ""
Lor     = "", "|", ""
Div     = "", "/", ""
Rdiv    = "", "\\", ""
Elrdiv = "", ".\\", ""
def Exp(node):
    out = str(node[0])
    for child in node[1:]:
        out = "pow(" + str(out) + "," + str(child) + ")"
    return out
def Elexp(node):
    out = str(node[0])
    for child in node[1:]:
        out = "pow(" + str(out) + "," + str(child) + ")"
    return out

All = "&="
Neg = "-(", "", ")"
Not = "not ", "", ""

Ctranspose = "arma::ctranspose(", "", ")"
Transpose = "arma::transpose(", "", ")"

def Eldiv(node):
    children = map(str, node[:])[::-1]
    return "/".join(children)

def Colon(node):

    for child in node:
        child.suggest("int")

    if node.group["class"] in ("Get", "Get2", "Get3") and\
            node.group.type(retd=True).numeric:
        node.type("uvec")
        name = "uspan"
    elif node.group["class"] == "Sets" and\
            node.group.parent.type(retd=True).numeric:
        node.type("uvec")
        name = "uspan"
    elif node.group["class"] == "Assign" and\
            node.group[0].type(retd=True).type == 0:
        node.type("uvec")
        name = "uspan"
    else:
        node.type("ivec")
        name = "span"

    if len(node) == 3:
        return name+"(%(0)s, %(1)s, %(2)s)"

    return name+"(%(0)s, 1, %(1)s)"
