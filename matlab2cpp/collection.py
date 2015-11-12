"""
All the various different kinds of nodes


"""

from node import Node

__all__ = [
"All", "Assign", "Assigns", "Band", "Bcomment", "Block", "Bor", "Branch",
"Break", "Case", "Catch", "Cell", "Cget", "Colon", "Cond", "Condline",
"Counter", "Cset", "Ctranspose", "Cvar", "Declare", "Declares", "Ecomment",
"Elementdivision", "Elexp", "Elif", "Elmul", "Else", "End", "Eq", "Error",
"Exp", "Expr", "Fget", "Float", "For", "Fset", "Func", "Funcs", "Fvar", "Ge",
"Get", "Gt", "Header", "Headers", "If", "Imag", "Include", "Includes", "Inline",
"Inlines", "Int", "Lambda", "Land", "Lcomment", "Le", "Leftelementdivision",
"Leftmatrixdivision", "Log", "Lor", "Lt", "Main", "Matrix", "Matrixdivision",
"Minus", "Mul", "Ne", "Neg", "Nget", "Not", "Nset", "Opr", "Otherwise",
"Params", "Paren", "Plus", "Program", "Project", "Resize", "Return", "Returns",
"Set", "Sget", "Sset", "Statement", "String", "Struct", "Structs", "Switch",
"Transpose", "Try", "Tryblock", "Var", "Vector", "Warning", "While"
]

class Project(Node):
    def __init__(self, backend="program", name="project", cur=0, line=0, code="", file="unnamed", **kws):
        """
Root of the node tree. Every other node should inherant from this one.

This node should not recieve `parent` argument node during construction.

Children:
    `Program+`

All keyword arguments are passed to `mc.Node.__init__`.
    """
        assert "parent" not in kws
        self.parent = self
        self._program = self
        Node.__init__(self, self, name=name, backend=backend, cur=cur,
                line=line, code=code, file=file, **kws)

class Program(Node):
    def __init__(self, parent, name, backend="program", **kws):
        """
Represents one stand-alone script or program. Each child represents the various
aspects of script/program.

Children:
    `Includes Funcs Inlines Structs Headers Log`

All keyword arguments are passed to `mc.Node.__init__`.
    """
        self._program = self
        Node.__init__(self, parent, name=name, backend=backend, file=name, **kws)

class Includes(Node):
    def __init__(self, parent, backend="program", **kws):
        """

Children:
    `Includes Funcs Inlines Structs Headers Log`

All keyword arguments are passed to `mc.Node.__init__`.
    """
        Node.__init__(self, parent, backend=backend, **kws)

class Funcs(Node):
    def __init__(self, parent, backend="program", line=1, **kws):
        Node.__init__(self, parent, line=line, backend=backend, **kws)

class Inlines(Node):
    def __init__(self, parent, backend="program", **kws):
        Node.__init__(self, parent, backend=backend, **kws)

class Structs(Node):
    def __init__(self, parent, backend="program", **kws):
        Node.__init__(self, parent, backend=backend,**kws)

class Headers(Node):
    def __init__(self, parent, backend="program", **kws):
        Node.__init__(self, parent, backend=backend, **kws)

class Log(Node):
    def __init__(self, parent, backend="program", **kws):
        Node.__init__(self, parent, backend=backend, **kws)

class Header(Node):
    def __init__(self, parent, name, backend="program", **kws):
        Node.__init__(self, parent, name=name, backend=backend, **kws)

class Main(Node):
    def __init__(self, parent, name="main", backend="func_return", **kws):
        Node.__init__(self, parent, name=name, backend=backend, **kws)

class Error(Node):
    def __init__(self, parent, name, value, backend="program", **kws):
        Node.__init__(self, parent, name, value=value, backend=backend, **kws)
        self.prop["cls"] = name[10:]
class Warning(Node):
    def __init__(self, parent, name, value, backend="program", **kws):
        Node.__init__(self, parent, name, value=value, backend=backend, **kws)
        self.prop["cls"] = name[10:]

class Counter(Node):
    def __init__(self, parent, name, value,
            backend="structs", type="structs", **kws):
        Node.__init__(self, parent, name,
                value=value, backend=backend, type=type, **kws)

class Inline(Node):
    def __init__(self, parent, name, backend="program", **kws):
        Node.__init__(self, parent, name, backend=backend, **kws)

class Include(Includes):
    def __init__(self, parent, name, backend="program", **kws):
        Node.__init__(self, parent, name=name, backend=backend, **kws)

class Struct(Structs):          pass

class Func(Node):           pass
class Returns(Node):        pass
class Params(Node):         pass
class Declares(Node):       pass
class Declare(Node):        pass

class Block(Node):
    def __init__(self, parent, backend="code_block", **kws):
        Node.__init__(self, parent, backend=backend, **kws)
class Condline(Block):      pass
class For(Block):           pass
class While(Block):         pass
class Switch(Block):        pass
class Case(Block):          pass
class Otherwise(Block):     pass
class Branch(Block):        pass
class If(Block):            pass
class Elif(Block):          pass
class Else(Block):          pass
class Cond(Block):          pass
class Tryblock(Block):      pass
class Try(Block):           pass
class Catch(Block):         pass
class Statement(Block):     pass

class Assign(Node):         pass
class Assigns(Node):
    def __init__(self, parent, backend="code_block", **kws):
        Node.__init__(self, parent, backend=backend, **kws)

class Expr(Node):
    def __init__(self, parent, backend="expression", **kws):
        Node.__init__(self, parent, backend=backend, **kws)
class Opr(Expr):            pass
class Exp(Opr):             pass
class Elexp(Opr):           pass
class Mul(Opr):             pass
class Minus(Opr):           pass
class Elmul(Opr):           pass
class Matrixdivision(Opr):      pass
class Elementdivision(Opr):     pass
class Leftmatrixdivision(Opr):  pass
class Leftelementdivision(Opr): pass
class Plus(Opr):            pass
class Colon(Opr):           pass
class Gt(Opr):              pass
class Ge(Opr):              pass
class Lt(Opr):              pass
class Le(Opr):              pass
class Ne(Opr):              pass
class Eq(Opr):              pass
class Band(Opr):            pass
class Bor(Opr):             pass
class Land(Opr):            pass
class Lor(Opr):             pass

class Matrix(Node):
    def __init__(self, parent, backend="matrix", **kws):
        Node.__init__(self, parent, backend=backend, **kws)
class Vector(Matrix):       pass

class Cell(Node):
    def __init__(self, parent, backend="cell", **kws):
        Node.__init__(self, parent, backend=backend, **kws)

class Paren(Expr):          pass
class Neg(Expr):            pass
class Not(Expr):            pass
class Ctranspose(Expr):     pass
class Transpose(Expr):      pass
class All(Expr):            pass
class End(Expr):            pass
class Break(Expr):          pass
class Return(Expr):         pass

class Int(Node):
    def __init__(self, parent, value, backend="int", type="int", **kws):
        Node.__init__(self, parent, value=value, backend=backend, type=type, **kws)

class Float(Node):
    def __init__(self, parent, value, backend="double", type="double", **kws):
        if value[0] == ".": value = "0" + value
        Node.__init__(self, parent, value=value, backend=backend, type=type, **kws)

class Imag(Node):
    def __init__(self, parent, value, backend="cx_double", type="cx_double", **kws):
        Node.__init__(self, parent, backend=backend, type=type, **kws)

class String(Node):
    def __init__(self, parent, value, backend="string", type="string", **kws):
        value = value.replace("%", "__percent__")
        Node.__init__(self, parent, value=value, backend=backend, type=type, **kws)

class Lambda(Node):
    def __init__(self, parent, name="", backend="func_lambda", **kws):
        Node.__init__(self, parent, name=name, backend=backend, **kws)

class Lcomment(Node):
    def __init__(self, parent, value, backend="code_block", **kws):
        value = value.replace("%", "__percent__")
        Node.__init__(self, parent, value=value, backend=backend, **kws)

class Bcomment(Node):
    def __init__(self, parent, value, backend="code_block", **kws):
        value = value.replace("%", "__percent__")
        Node.__init__(self, parent, value=value, backend=backend, **kws)

class Ecomment(Node):
    def __init__(self, parent, value, backend="code_block", **kws):
        value = value.replace("%", "__percent__")
        Node.__init__(self, parent, value=value, backend=backend, **kws)

class Var(Node):
    def __init__(self, parent, name, **kws):
        Node.__init__(self, parent, name=name, **kws)
class Get(Var):         pass
class Set(Var):         pass

class Fvar(Node):
    def __init__(self, parent, name, value, backend="struct", **kws):
        Node.__init__(self, parent, name=name, value=value, backend=backend, **kws)

class Cvar(Node):
    def __init__(self, parent, name, backend="cell", **kws):
        Node.__init__(self, parent, name, backend=backend, **kws)

class Cget(Node):
    def __init__(self, parent, name, backend="cell", **kws):
        Node.__init__(self, parent, name=name, backend=backend, **kws)

class Fget(Node):
    def __init__(self, parent, name, value, backend="struct", **kws):
        Node.__init__(self, parent, name=name, value=value, backend=backend, **kws)

class Sget(Node):
    def __init__(self, parent, name, value, backend="structs", **kws):
        Node.__init__(self, parent, name=name, value=value, backend=backend, **kws)

class Nget(Node):
    def __init__(self, parent, name, backend="struct", **kws):
        Node.__init__(self, parent, backend=backend, name=name, **kws)

class Cset(Node):
    def __init__(self, parent, name, backend="cell", **kws):
        Node.__init__(self, parent, name=name, backend=backend, **kws)

class Fset(Node):
    def __init__(self, parent, name, value, backend="struct", **kws):
        Node.__init__(self, parent, name=name, value=value, backend=backend, **kws)

class Sset(Node):
    def __init__(self, parent, name, value, backend="structs", **kws):
        Node.__init__(self, parent, name=name, value=value, backend=backend, **kws)

class Nset(Node):
    def __init__(self, parent, name, backend="struct", **kws):
        Node.__init__(self, parent, name=name, backend=backend, **kws)

class Resize(Node):
    def __init__(self, parent, backend="cube_common", **kws):
        Node.__init__(self, parent, backend=backend, **kws)

class Verbatim(Node):
    def __init__(self, parent, name, value, backend="verbatim", **kws):
        Node.__init__(self, parent, name=name, value=value, backend=backend, **kws)
