"""
All the different kinds of nodes
"""

from node import Node

class Project(Node):
    def __init__(self, backend="program", name="project", line=0,
            cur=0, **kws):
        self.parent = self
        self._program = self
        Node.__init__(self, self, cur=cur, line=line, name=name,
                backend=backend, **kws)

class Resize(Node):
    def __init__(self, parent, backend="cube_common", **kws):
        Node.__init__(self, parent, backend=backend, **kws)

class Errors(Node):
    def __init__(self, parent, backend="error_log", **kws):
        Node.__init__(self, parent, backend=backend, **kws)

class Error(Node):
    def __init__(self, parent, name, value, backend="error_log", **kws):
        Node.__init__(self, parent, name, value=value, backend=backend, **kws)
        self.prop["cls"] = name[10:]

class Warning(Node):
    def __init__(self, parent, name, value, backend="error_log", **kws):
        Node.__init__(self, parent, name, value=value, backend=backend, **kws)
        self.prop["cls"] = name[10:]

class Counter(Node):
    def __init__(self, parent, name, value,
            backend="structs", type="structs", **kws):
        Node.__init__(self, parent, name,
                value=value, backend=backend, type=type, **kws)

class Library(Node):
    def __init__(self, parent, backend="program", **kws):
        Node.__init__(self, parent, backend=backend, **kws)

class Snippet(Node):
    def __init__(self, parent, name, value, backend="program", **kws):
        Node.__init__(self, parent, name, value=value, backend=backend, **kws)

class Program(Node):
    def __init__(self, parent, name="program", backend="program", **kws):
        self._program = self
        Node.__init__(self, parent, name=name, backend=backend, **kws)

class Includes(Node):
    def __init__(self, parent, backend="program", **kws):
        Node.__init__(self, parent, backend=backend, **kws)
class Include(Includes):
    def __init__(self, parent, name, value, backend="program", **kws):
        Node.__init__(self, parent, name=name, value=value, backend=backend, **kws)

class Structs(Node):
    def __init__(self, parent, backend="struct", **kws):
        Node.__init__(self, parent, backend=backend,**kws)
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
class Div(Opr):             pass
class Eldiv(Opr):           pass
class Rdiv(Opr):            pass
class Elrdiv(Opr):          pass
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
