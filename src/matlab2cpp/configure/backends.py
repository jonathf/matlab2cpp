import matlab2cpp as mc

Project = "program"
Program = "program"
Includes = "program"
Funcs = "program"
Inlines = "program"
Structs = "program"
Struct = "program"
Headers = "program"
Log = "program"
Header = "program"
Main = "func_return"
Error = "program"
Warning = "program"
Counter = "structs"
Inline = "program"
Include = "program"
Block = "code_block"
Parfor = "code_block"
For = "code_block"
While = "code_block"
Switch = "code_block"
Case = "code_block"
Otherwise = "code_block"
Branch = "code_block"
If = "code_block"
Elif = "code_block"
Else = "code_block"
Tryblock = "code_block"
Try = "code_block"
Catch = "code_block"
Statement = "code_block"
def Assigns(node):
    backend = node[-1].backend
    if backend in ("func_returns",):
        node.backend = backend
    elif backend != "unknown":
        node.backend = "code_block"
Expr = "expression"
Exp = "expression"
Elexp = "expression"
Mul = "expression"
Minus = "expression"
Elmul = "expression"
Matrixdivision = "expression"
Elementdivision = "expression"
Leftmatrixdivision = "expression"
Leftelementdivision = "expression"
Plus = "expression"
Colon = "expression"
Gt = "expression"
Ge = "expression"
Lt = "expression"
Le = "expression"
Ne = "expression"
Eq = "expression"
Band = "expression"
Bor = "expression"
Land = "expression"
Lor = "expression"
Paren = "expression"
Neg = "expression"
Not = "expression"
Ctranspose = "expression"
Transpose = "expression"
All = "expression"
End = "expression"
Break = "expression"
Return = "expression"
def Matrix(node):
    # matrix surround struct converts it to array
    if len(node) == 1 and len(node[0]) == 1:
        elem = node[0][0]
        if elem.backend != "unknown":
            node.backend = elem.backend

        if elem.backend != "unknown" and elem.backend not in ("struct", "structs"):
            node.backend = "matrix"
    else:
        node.backend = "matrix"

Vector = "matrix"
Cell = "cell"
Int = "int"
Float = "double"
Imag = "cx_double"
String = "string"
Lambda = "func_lambda"
Pragma_for = "code_block"
Tbb_for = "code_block"
Lcomment = "code_block"
Bcomment = "code_block"
Ecomment = "code_block"
def Fvar(node):
    """
Example:
    >>> print(mc.qtree("a.b = 4.4; c = [a.b]", core=True, suggest=True)) #doctest: +NORMALIZE_WHITESPACE
    1   1Block      code_block   TYPE    
    1   1| Assign     double       double  
    1   1| | Fvar       struct       double  a
    1   7| | Float      double       double  
    1  12| Assign     struct       double  
    1  12| | Var        double       double  c
    1  16| | Matrix     struct       double  
    1  17| | | Vector     matrix       double  
    1  17| | | | Fvar       struct       double  a
    """
    declare = node.func[0][node.name]
    if declare.backend in ("struct", "structs"):
        node.backend = declare.backend

Cvar = "cell"
Cget = "cell"
Fget = "structs"
Sget = "structs"
Nget = "struct"
Cset = "cell"
Fset = "structs"
Sset = "structs"
Nset = "struct"
Resize = "cube_common"
Verbatim = "verbatim"

def Var(node):
    if node.type != "TYPE":
        node.backend = node.type
def Get(node):
    if node.type != "TYPE":
        node.backend = node.type
def Set(node):
    if node.type != "TYPE":
        node.backend = node.type

def Func(node):
    returns = node[1]
    if node.name[:1] == "_":
        node.backend = "func_lambda"
    elif len(returns) == 1:
        node.backend = "func_return"
    else:
        node.backend = "func_returns"
def Returns(node):
    if node.parent.name[:1] == "_":
        node.backend = "func_lambda"
    elif len(node) == 1 or node.parent.cls == "Main":
        node.backend = "func_return"
    else:
        node.backend = "func_returns"
def Params(node):
    returns = node.parent[1]
    if node.parent.name[:1] == "_":
        node.backend = "func_lambda"
    elif len(returns) == 1 or node.parent.cls == "Main":
        node.backend = "func_return"
    else:
        node.backend = "func_returns"
def Declares(node):
    returns = node.parent[1]
    if node.parent.name[:1] == "_":
        node.backend = "func_lambda"
    elif len(returns) == 1 or node.parent.cls == "Main":
        node.backend = "func_return"
    else:
        node.backend = "func_returns"

def Assign(node):
    node.backend = node[-1].backend


if __name__ == "__main__":
    import doctest
    doctest.testmod()
