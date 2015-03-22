"""
Target translation rules

Module content
==============

Each rule is identiefied by a handle file.
The basic nodes ara found in:

code_block.py   Loops, branches, statements, etc.
expression.py   Operators used in expression
func_return.py  Functions with single return
func_returns.py Functions with multiple returns
func_lambda.py  Lambda functions
matrix.py       Matrix/Vector declaration
program.py      Program as a whole. Includes and using namespace

There are also type dependent nodes which must be defined
from either context or suppliment file. These include:

float.py        Imaginary floats
fmat.py         Matrix of floats
frowvec.py      Row vector of floats
func_return.py  Functions with single return
func_returns.py Functions with multiple returns
func_lambda.py  Lambda functions
fvec.py         Column vector of floats
ifloat.py       Floats
iint.py         Imaginary integers
imat.py         Matrix of integers
int.py          Integers
irowvec.py      Row vector of integers
ivec.py         Column vector of integers
unknown.py      Unknown/Unassigned

In addtion, to be able to handle libary calls, there is also:

reserved.py     Library calls


Common properties
=================
Basic information
-----------------
backend         Name of current file which will handle this node
class           Name of current node type
func            Name of current function
%d              Access child number "%d"

Example
-------
>>> print node["name"]
y
>>> child0 = node[0]

Access to ancestry
------------------
parent          Parent node
func            Function (local function scope)
root            Tree root (static information)

Example
-------
>>> func = node.func

Node types
==========
Depending on context, each node has a type. It often defines
target backend is higly relevant for the handling of variable.

Example
-------
>>> type = node.type()      # Get type
>>> node.type("fmat")       # Set type (self or ancestry)
>>> node.suggest("irowvec") # Suggest type (children of class Var)

Building rules
==============
Rules come in two different types: strings and tuples.
The former give the most detailed control, while the latter has the
most flexibility for variable number of children.

Strings
-------
If a node is a string or a function returning a string, this will
be used inserted and used as code.

%(0)s, %(1)s, ...           replaced with the children
%(name)s, %(value)s, ...    replaced with properties

Example
-------
>>> Paren = "(%(0)s)"

Tuples
------
If node is a tuple or a function returning a tuple, each child will
be weaved in as follows (r-return value, c-child):
1 return        r[0] c[0] c[1] ... c[n]
2 return        r[0] c[0] c[1] ... c[n] r[1]
3 return        r[0] c[0] r[1] c[1] r[1] ... r[1] c[n] r[2]

%(name)s, %(value)s, ...    replaced with properties

Example
-------
>>> Plus = ("", "+", "")

Nodes
=====
The various node-types covered in the software is listed here.

Program : The root node
    Contains: Func, ...
    Rule: program.py

Includes : Elements included in preamble
    Contains: Include, ...
    Rule: program.py

Includes : Element in preamble
    Rule: program.py

Func : Function
    Contains: Returns, Params, Block
    Rule: func_return.py (if one variable return)
          func_returns.py (if multiple return)
    Property: name

Declares : Declarations in the beginning of function
    Contains: Var, ...
    Rule: func_return.py (if one variable return)
          func_returns.py (if multiple return)

Returns : Function return variables
    Contains: Var, ...
    Rule: func_return.py (if one variable return)
          func_returns.py (if multiple return)

Params : Function parameter variables
    Contains: Var, ...
    Rule: func_return.py (if one variable return)
          func_returns.py (if multiple return)

Block : Block of code
    Contains one or more of:
        Assign, Assigns, Branch, For, Func, Set, Set2, Set3,
        Statement, Switch, Tryblock, While
    Rule: code_block.py

For : For-loop
    Contains: Var, Expr, Block
    Rule: code_block.py

While : While-loop
    Contains: Expr, Block
    Rule: code_block.py

Switch : Root of switch/case
    Contains: Expr, Case, ..., (Otherwise)
    Rule: code_block.py
    Property: hasotherwise (True if Otherwise is included)

Case : Case in switch/case
    Contains: Expr, Block
    Rule: code_block.py

Otherwise : Alternative if all cases fails in switch/case
    Contains: Block
    Rule: code_block.py

Branch : Root of if/then/else
    Contains: If, Elif, ..., Else
    Rule: code_block.py
    Property: haselse (True if Else is included)

If : If in if/then/else
    Contains: Cond, Block
    Rule: code_block.py

Elif : Else-if in if/then/else
    Contains: Cond, Block
    Rule: code_block.py

Else : Else in if/then/else
    Contains: Block
    Rule: code_block.py

Cond : Conditional statement
    Contains: Expr
    Rule: code_block.py

Tryblock : Root of try/catch
    Contains: Try, Catch, ...
    Rule: code_block.py

Try : Try in try/catch
    Contains: Block
    Rule: code_block.py

Catch : Catch in try/catch
    Contains: Block
    Rule: code_block.py

Statement : Stand-alone codeline without assignment etc.
    Example: "y"
    Contains: Expr
    Rule: code_block.py

Set : Module/Array assignment
    Example: "y(2) = 4"
    Contains: Sets (lhs), Expr (rhs)
    Rule: <type specific>

Set2 : Tuple assignment
    Example: "y.(2) = 4"
    Contains: Sets (lhs), Expr (rhs)
    Rule: <type specific>

Set3 : Field assignment
    Example: "y.a = 4"
    Contains: Sets (lhs), Expr (rhs)
    Rule: <type specific>

Sets : Arguments of the Set-assignment
    Contains one or more of: All, Expr
    Rule: code_block

Assign : Single variable assignment
    Example: "y = 4"
    Contains: Var (lhs), Expr (rhs)
    Rule: <type specific>

Assigns : Multiple variable assignment
    Example: "[x, y] = f(4)"
    Example: "[x, y] = z"
    Contains: Assigned (lhs), Var (rhs)
    Rule: code_block.py
    Property: isvariable (True if Var is variable)

Assigned : Lhs in Assigns
    Contains one or more: Var
    Rule : code_block.py

Expr : General expression
    Take the following form:
        Band, Bor, Colon, Ctranspose, Div, Eldiv, Elexp, Elmul,
        Elrdiv, End, Eq, Exp, Float, Ge, Get, Get2, Get3, Gt,
        Ifloat, Iint, Int, Land, Lor, Lt, Matrix, Minus, Mul, Ne,
        Neg, Not, Paren, Plus, Rdiv, String, Transpose, Var
    Rule: expression.py

Band : Bit-vise And-operator
    Example: "x && y"
    Contains: Expr, Expr, ...
    Rule: expression.py

Bor : Bit-vise Or-operator
    Example: "x || y"
    Contains: Expr, Expr, ...
    Rule: expression.py

Colon : Colon
    Example: "x:y"
    Example: "x:y:z"
    Contains: Expr, Expr, (Expr)
    Rule: expression.py

Ctranspose : Ctranspose
    Example: "x'"
    Contains: Expr
    Rule: expression.py

Div : Division
    Example: "x / y"
    Contains: Expr, Expr, ...
    Rule: expression.py

Eldiv : Element-wise division
    Example: "x ./ y"
    Contains: Expr, Expr, ...
    Rule: expression.py

Elexp : Element-wise exponent
    Example: "x .^ y"
    Contains: Expr, Expr, ...
    Rule: expression.py

Elmul : Element-wise multiplication
    Example: "x .* y"
    Contains: Expr, Expr, ...
    Rule: expression.py

Elrdiv : Element-wise right division
    Example: "x .\ y"
    Contains: Expr, Expr, ...
    Rule: expression.py

End : Special charracter: last element in range/array
    Example: "y(end)"
    Rule: expression.py

Eq : Equate (Truth-value)
    Example: "x == y"
    Contains: Expr, Expr
    Rule: expression.py

Exp : Exponent
    Example: "x ^ y"
    Contains: Expr, Expr, ...
    Rule: expression.py

Float : Float
    Example: "4."
    Rule: float.py
    Property: value

Ge : Greater or equal
    Example: "x >= y"
    Contains: Expr
    Rule: expression.py

Get : Function/Array retrieval
    Example: "y(4)"
    Contains: Gets
    Rule: <type specific>
    Property: name

Get2 : Fieldname retrieval
    Example: "x.(y)"
    Contains: Gets
    Rule: <type specific>
    Property: name

Get3 : Tuple retrieval
    Example: "x.y"
    Contains: Gets
    Rule: <type specific>
    Property: name

Gt : Greater than
    Example: "x > y"
    Contains: Expr, Expr
    Rule: expression.py

Ifloat : Ifloat
    Example: "4.i"
    Rule: ifloat.py
    Property: value

Iint : Iint
    Example: "4i"
    Rule: iint.py
    Property: value

Int : Int
    Example: "4"
    Rule: int.py
    Property: value

Land : Logical And
    Example: "x and y"
    Contains: Expr
    Rule: expression.py

Lor : Logical Or
    Example: "x or y"
    Contains: Expr
    Rule: expression.py

Lt : Lt
    Example: "x < y"
    Contains: Expr, Expr
    Rule: expression.py

Matrix : Matrix container
    Example: "[x;y]"
    Contains: Vector, ...
    Rule: matrix.py

Vector : (Column)-Vector container
    Contains: Expr, ...
    Rule: matrix.py

Minus : Subtraction
    Example: "x - y"
    Contains: Expr, Expr, ...
    Rule: expression.py

Mul : Multiplication
    Example: "x * y"
    Contains: Expr, Expr, ...
    Rule: expression.py

Ne : Not equal
    Example: "x <> y"
    Contains: Expr, Expr
    Rule: expression.py

Neg : Negative
    Example: "-y"
    Contains: Expr
    Rule: expression.py

Not : Negation
    Example: "not y"
    Contains: Expr
    Rule: expression.py

Paren : Parenthesis
    Example: "(y)"
    Contains: Expr
    Rule: expression.py

Plus : Addition
    Example: "x + y"
    Contains: Expr, Expr, ...
    Rule: expression.py

Rdiv : Right devision
    Example: "x \ y"
    Contains: Expr
    Rule: expression.py

String : String
    Example: "'y'"
    Contains: Expr
    Rule: string.py
    Property: value

Transpose : Transpose
    Example: "y.'"
    Contains: Expr
    Rule: expression.py

Var : Var
    Example: "y"
    Rule: expression.py
    Property: name

All : All elements in array
    Example: "y(:)"
    Rule: expression.py
"""
import glob
import os
sep = os.path.sep

for name in glob.glob(os.path.dirname(__file__)+sep+"*.py"):

    name = name.split(sep)[-1]
    if name != "__init__":
        exec("import %s" % name[:-3])
