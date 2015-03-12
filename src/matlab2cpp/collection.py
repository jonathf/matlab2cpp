"""
All the different kinds of nodes
"""

from node import Node

class Program(Node):
    """Root of the tree"""

    def __init__(self):
        self.program = self
        Node.__init__(self, self, "program")

class Block(Node):
    """Code block

Children
--------
line, [line, ...]
line : For, Func, Assign, Assigns, Set, Statement, Branch
    One or more codelines
    """

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


class Params(Node):
    """Parameter Values

Children
--------
[var, ...]

var : Var
    Zero or more parameter values
    """


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

class While(Node):
    """Whlie-llop

Children
--------
condtion : Expr
    Condition that is tested for each iteration
block : Block
    One or more codelines.
    """

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


class Otherwise(Node):
    """Otherwise Block

Children
--------
block : Block
    One or more codelines to run.
    """


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

class Else(Node):
    """Else Block

Children
--------
block : Block
    One or more codelines to run.
    """


class Cond(Node):
    """Conditional statement

Children
--------
expr : Expr
    Expression
    """

class Tryblock(Node):
    pass

class Try(Node):
    pass

class Catch(Node):
    def __init__(self, parent, name=""):
        Node.__init__(self, parent)
        if name:
            self["name"] = name


class Statement(Node):
    """Code statement

Children
--------
expr : Expr
    Expression to evaluation
    """


class Var(Node):
    """Variable"""
    def __init__(self, parent, name=""):
        if name and name[0] == "@":
            Node.__init__(self, parent, name[1:])
            self["lambda"] = True
        else:
            Node.__init__(self, parent, name)
            self["lambda"] = False


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

class Assigned(Node): pass

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
    def _backend(self):
        return self.line["backend"]

class Vector(Expr):
    """Vector

Children
--------
expr, [expr ...]

expr : Expr
    One or more vector element.
    """
    def _backend(self):
        return self.line["backend"]

class Paren(Expr):
    """Parenthesis

Children
--------
expr : Expr
    Grouped expression.
    """

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

class Neg(Expr):
    """Negative prefix

Children
--------
expr : Expr
    Grouped expression.
    """

class Not(Expr):
    """Negative prefix

Children
--------
expr : Expr
    Grouped expression.
    """

class Ctranspose(Expr):
    pass

class Transpose(Expr):
    pass

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


class Float(Expr):
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


class Ifloat(Expr):
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

class String(Expr):
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


class All(Expr):
    "Indicator for the full range in function/module calls."
    pass


class End(Expr):
    "Indicator for last element in iterable"
    pass

class Includes(Node):
    pass

class Include(Node):
    pass

class Declares(Node):
    pass

class Declare(Node):
    pass
