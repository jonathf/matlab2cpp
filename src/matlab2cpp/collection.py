"""
All the different kinds of nodes
"""

from node import Node

class Program(Node):
    """Root of the tree"""

    def __init__(self):
        self.program = self
        Node.__init__(self, self, "program")

        self["backend"] = "program"

class Includes(Node):

    def __init__(self, parent, name=""):
        Node.__init__(self, parent, name)
        self["backend"] = "program"

class Include(Node):

    def __init__(self, parent, name=""):
        Node.__init__(self, parent, name)
        self["backend"] = "program"

class Block(Node):
    """Code block

Children
--------
line, [line, ...]
line : For, Func, Assign, Assigns, Set, Statement, Branch
    One or more codelines
    """

    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "code_block"

class Func(Node):
    """Function

Children
--------
retvals, params, block

retvals : Returns
    Return variables
params : Rarams
    Function parameters
block : Block
    One or more codelines
    """
    def __init__(self, parent, name):
        Node.__init__(self, parent, name)

class Returns(Node):
    """Return Values

Children
--------
[var, ...]

var : Var
    Zero or more return values
    """
    def __init__(self, parent):
        Node.__init__(self, parent)


class Params(Node):
    """Parameter Values

Children
--------
[var, ...]

var : Var
    Zero or more parameter values
    """
    def __init__(self, parent):
        Node.__init__(self, parent)


class Declares(Node):
    def __init__(self, parent):
        Node.__init__(self, parent)

class Declare(Node):
    pass


class For(Node):
    """For-loop

Children
--------
index, condition, block

index : Var
    Variable traversing the for loop.
condition : Expr
    How runner changes.
block : Block
    One or more codelines.
    """
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "code_block"

class While(Node):
    """Whlie-llop

Children
--------
condtion : Expr
    Condition that is tested for each iteration
block : Block
    One or more codelines.
    """
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "code_block"

class Switch(Node):
    """Switch branch

Children
--------
case [case, ...], [otherwise]

case : Case
    One or more Case blocks
otherwise : Otherwise
    Optional "Else" block
    """
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "code_block"


class Case(Node):
    """Case Block

Children
--------
condition, block

condition : Cond
    Conditional value for entering block
block : Block
    One or more codelines to run if condition is met.
    """
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "code_block"


class Otherwise(Node):
    """Otherwise Block

Children
--------
block : Block
    One or more codelines to run.
    """
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "code_block"


class Branch(Node):
    """If branch

Children
--------
if, [elif, ...], [else]

if : If
    If block.
elif : Elif
    One or more optional "Else if" blocks
else : Else
    Optional "Else" block
    """
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "code_block"


class If(Node):
    """If Block

Children
--------
condition, block

condition : Cond
    Conditional value for entering block
block : Block
    One or more codelines to run if condition is met.
    """
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "code_block"

class Elif(Node):
    """Elif Block

Children
--------
condition, block

condition : Cond
    Conditional value for entering block
block : Block
    One or more codelines to run if condition is met.
    """
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "code_block"

class Else(Node):
    """Else Block

Children
--------
block : Block
    One or more codelines to run.
    """
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "code_block"


class Cond(Node):
    """Conditional statement

Children
--------
expr : Expr
    Expression
    """
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "code_block"

class Tryblock(Node):

    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "code_block"

class Try(Node):
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "code_block"

class Catch(Node):
    def __init__(self, parent, name=""):
        Node.__init__(self, parent)
        if name:
            self["name"] = name
        self["backend"] = "code_block"


class Statement(Node):
    """Code statement

Children
--------
expr : Expr
    Expression to evaluation
    """
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "code_block"


class Var(Node):
    """Variable"""
    def __init__(self, parent, name):
        if name[:1] == "@":
            name = name[1:]
        Node.__init__(self, parent, name)


class Set(Node):
    """Set a module/array value

Children
--------
rhs, lhs
arg : Expr, All
    One or more arguments.
rhs : Expr
    Right hand side expression.
    """

class Set2(Node):
    """Set a tuple element"""

class Set3(Node):
    """Set a field element"""

class Sets(Node):
    """Values argument for the Set methods"""
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "code_block"


class Assign(Node):
    """Assigment of variable

Children
--------
lhs, rhs

lhs : Var
    Left hand side/Assigned value.
rhs : Expr
    Right hand side expression.
    """

class Assigns(Node):
    """Assigment of multiple variables

Children
--------
lhs, rhs

lhs : Assigns_return
    Two or more variable returned
rhs : Assigns_args
    Argument in call.
    """
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "code_block"

class Assigned(Node):

    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "code_block"

class Assignees(Node): pass

class Expr(Node):
    """Expression

Children
    """

class Opr(Expr):
    """Operator

Children
--------
arg, arg, [arg ...]

arg : Expr
    Two or more argument for the operator.
"""
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "expression"

class Exp(Opr): pass
class Elexp(Opr): pass
class Mul(Opr): pass
class Minus(Opr): pass
class Elmul(Opr): pass
class Div(Opr): pass
class Eldiv(Opr): pass
class Rdiv(Opr): pass
class Elrdiv(Opr): pass
class Plus(Opr): pass
class Colon(Opr): pass
class Gt(Opr): pass
class Ge(Opr): pass
class Lt(Opr): pass
class Le(Opr): pass
class Ne(Opr): pass
class Eq(Opr): pass
class Band(Opr): pass
class Bor(Opr): pass
class Land(Opr): pass
class Lor(Opr): pass

class Matrix(Node):
    """Matrix

Children
--------
vector, [vector ...]

vector : Vector
    One or more row vector.
    """
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "matrix"

class Vector(Node):
    """Vector

Children
--------
expr, [expr ...]

expr : Expr
    One or more vector element.
    """
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "matrix"

class Paren(Node):
    """Parenthesis

Children
--------
expr : Expr
    Grouped expression.
    """
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "expression"

class Get(Var):
    """Function/Module call

func(arg1, arg2, ..)

Children
--------
arg, [arg ...]

arg : Expr
    One or more argument in the function/module call.
    """

class Get2(Var):
    "Fieldname retrival"

class Get3(Var):
    "Tuple retrival"

class Gets(Node): pass

class Neg(Node):
    """Negative prefix

Children
--------
expr : Expr
    Grouped expression.
    """
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "expression"

class Not(Node):
    """Negative prefix

Children
--------
expr : Expr
    Grouped expression.
    """
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "expression"

class Ctranspose(Node):
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "expression"

class Transpose(Node):
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "expression"

class Int(Node):
    """Integer """
    def __init__(self, parent, value):
        """
Parameters
----------
parent : Node
    Parent node
value : str
    Text representation of the int value.
        """
        Node.__init__(self, parent)
        self["value"] = value
        self["backend"] = "int"
        self.type("int")


class Float(Node):
    """Float """
    def __init__(self, parent, value):
        """
Parameters
----------
parent : Node
    Parent node
value : str
    Text representation of the float value.
        """
        Node.__init__(self, parent)
        self["value"] = value
        self["backend"] = "float"
        self.type("float")


class Iint(Node):
    """Imaginary integer """
    def __init__(self, parent, value):
        """
Parameters
----------
parent : Node
    Parent node
value : str
    Text representation of the int value.
        """
        Node.__init__(self, parent)
        self["value"] = value
        self["backend"] = "iint"
        self.type("iint")


class Ifloat(Node):
    """Imaginary float """
    def __init__(self, parent, value):
        """
Parameters
----------
parent : Node
    Parent node
value : str
    Text representation of the float value.
        """
        Node.__init__(self, parent)
        self["value"] = value
        self["backend"] = "ifloat"
        self.type("ifloat")

class String(Node):
    """String"""
    def __init__(self, parent, value):
        """
Parameters
----------
parent : Node
    Parent node
value : str
    Text representation of the string value.
        """
        Node.__init__(self, parent)
        self["value"] = value
        self["backend"] = "string"


class All(Node):
    "Indicator for the full range in function/module calls."
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "expression"


class End(Node):
    "Indicator for last element in iterable"
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "expression"

class Break(Node):
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "expression"

class Return(Node):
    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "expression"

class Lambda(Node):
    def __init__(self, parent, name=""):
        Node.__init__(self, parent, name)
        self["backend"] = "func_lambda"




class Assign_alt(Node):
    def __init__(self, parent, name=""):
        Node.__init__(self, parent, name)
        self["backend"] = "sandbox"

class Var_alt(Node):
    def __init__(self, parent, name=""):
        Node.__init__(self, parent, name)
        self["backend"] = "sandbox"

class Call_alt(Node):
    def __init__(self, parent, name=""):
        Node.__init__(self, parent, name)
        self["backend"] = "sandbox"

class Field1_alt(Node):
    def __init__(self, parent, name=""):
        Node.__init__(self, parent, name)
        self["backend"] = "sandbox"

class Field2_alt(Node):
    def __init__(self, parent, name=""):
        Node.__init__(self, parent, name)
        self["backend"] = "sandbox"

class Field3_alt(Node):
    def __init__(self, parent, name=""):
        Node.__init__(self, parent, name)
        self["backend"] = "sandbox"

class Assigned_alt(Node):

    def __init__(self, parent):
        Node.__init__(self, parent)
        self["backend"] = "sandbox"

class Assignees_alt(Node):

    def __init__(self, parent, name=""):
        Node.__init__(self, parent, name)
        self["backend"] = "sandbox"

class Get_alt(Node):
    def __init__(self, parent, name=""):
        Node.__init__(self, parent, name)
        self["backend"] = "sandbox"

class Cell_alt(Node):
    def __init__(self, parent, name=""):
        Node.__init__(self, parent, name)
        self["backend"] = "sandbox"
