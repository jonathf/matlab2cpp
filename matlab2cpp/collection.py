# encoding: utf-8

r"""
A full summary of all nodes.

+---------------------+--------------------+----------------+------------------------------+
| Name                | Children           | Example        | Description                  |
+=====================+====================+================+==============================+
| All                 |                    | `:`            | Colon operator w/o range     |
+---------------------+--------------------+----------------+------------------------------+
| Assign              | `Expr Expr`        | `a=b`          | Assignment one var           |
+---------------------+--------------------+----------------+------------------------------+
| Assigns             | `Expr Expr+`       | `[a,b]=c`      | Assignment multi vars        |
+---------------------+--------------------+----------------+------------------------------+
| Band                | `Expr Expr+`       | `a&b`          | Binary AND operator          |
+---------------------+--------------------+----------------+------------------------------+
| Bcomment            |                    | `%{ . %}`      | Block comment                |
+---------------------+--------------------+----------------+------------------------------+
| Block               | `Line*`            | `a`            | Code block                   |
+---------------------+--------------------+----------------+------------------------------+
| Bor                 | `Expr Expr+`       | `a|b`          | Binary OR operator           |
+---------------------+--------------------+----------------+------------------------------+
| Branch              | `If Ifse* Else?`   | `if a; end`    | If chain container           |
+---------------------+--------------------+----------------+------------------------------+
| Break               |                    | `break`        | Break statement              |
+---------------------+--------------------+----------------+------------------------------+
| Case                | `Var Block`        | `case a`       | Case part of Switch          |
+---------------------+--------------------+----------------+------------------------------+
| Catch               | `Block`            | `catch a`      | Catch part of Tryblock       |
+---------------------+--------------------+----------------+------------------------------+
| Cell                | `Expr*`            | `{a}`          | Cell array                   |
+---------------------+--------------------+----------------+------------------------------+
| Cget                | `Expr+`            | `a{b}(c)`      | Cell retrival                |
+---------------------+--------------------+----------------+------------------------------+
| Colon               | `Expr Expr Expr?`  | `a:b`          | Colon operator w range       |
+---------------------+--------------------+----------------+------------------------------+
| Counter             |                    |                | Struct array size            |
+---------------------+--------------------+----------------+------------------------------+
| Cset                | `Expr+`            | `a{b}(c)=d`    | Cell array assignment        |
+---------------------+--------------------+----------------+------------------------------+
| Ctranspose          | `Expr`             | `a'`           | Complex transform            |
+---------------------+--------------------+----------------+------------------------------+
| Cvar                | `Expr+`            | `a{b}`         | Cell variable                |
+---------------------+--------------------+----------------+------------------------------+
| Declares            | `Var*`             |                | Declared variable list       |
+---------------------+--------------------+----------------+------------------------------+
| Ecomment            |                    | `a%b`          | End-of-line comment          |
+---------------------+--------------------+----------------+------------------------------+
| Elementdivision     | `Expr Expr+`       | `a./b`         | Sclars division              |
+---------------------+--------------------+----------------+------------------------------+
| Elexp               | `Expr Expr+`       | `a.^b`         | Element-wise exponent        |
+---------------------+--------------------+----------------+------------------------------+
| Elif                | `Expr Block`       | `elseif a`     | Else-if part of Branch       |
+---------------------+--------------------+----------------+------------------------------+
| Elmul               | `Expr Expr+`       | `a.*b`         | Element-wise multiplication  |
+---------------------+--------------------+----------------+------------------------------+
| Else                | `Block`            | `else`         | Else part of Branch          |
+---------------------+--------------------+----------------+------------------------------+
| End                 |                    | `end`          | End-expression               |
+---------------------+--------------------+----------------+------------------------------+
| Eq                  | `Expr Expr`        | `a==b`         | Equallity sign               |
+---------------------+--------------------+----------------+------------------------------+
| Error               |                    |                | Error node                   |
+---------------------+--------------------+----------------+------------------------------+
| Exp                 | `Expr Expr+`       | `a^b`          | Exponential operator         |
+---------------------+--------------------+----------------+------------------------------+
| Fget                | `Expr*`            | `a.b(c)`       | Fieldarray retrival          |
+---------------------+--------------------+----------------+------------------------------+
| Float               |                    | `4.`           | Float-point number           |
+---------------------+--------------------+----------------+------------------------------+
| For                 | `Var Expr Block`   | `for a=b;end`  | For-loop container           |
+---------------------+--------------------+----------------+------------------------------+
| Fset                | `Expr Expr+`       | `a.b(c)=d`     | Fieldname assignment         |
+---------------------+--------------------+----------------+------------------------------+
| Func                | `Declares Returns` | `function f()` | Function container           |
|                     | `Params Block`     | `end`          |                              |
+---------------------+--------------------+----------------+------------------------------+
| Funcs               | `[Main Func+]`     |                | Root of all functions        |
+---------------------+--------------------+----------------+------------------------------+
| Fvar                |                    | `a.b`          | Fieldname variable           |
+---------------------+--------------------+----------------+------------------------------+
| Ge                  | `Expr Expr`        | `a>=b`         | Greater-or-equal operator    |
+---------------------+--------------------+----------------+------------------------------+
| Get                 | `Expr*`            | `a(b)`         | Function or retrival         |
+---------------------+--------------------+----------------+------------------------------+
| Gt                  | `Expr Expr`        | `a>b`          | Greater operator             |
+---------------------+--------------------+----------------+------------------------------+
| Header              |                    |                | File header element          |
+---------------------+--------------------+----------------+------------------------------+
| Headers             |                    |                | Collection header lines      |
+---------------------+--------------------+----------------+------------------------------+
| If                  | `Expr Block`       | `if a`         | If part of Branch            |
+---------------------+--------------------+----------------+------------------------------+
| Imag                |                    | `i`            | Imaginary unit               |
+---------------------+--------------------+----------------+------------------------------+
| Include             |                    |                | Include statement            |
+---------------------+--------------------+----------------+------------------------------+
| Includes            |                    |                | Collection of includes       |
+---------------------+--------------------+----------------+------------------------------+
| Int                 |                    | `1`            | Integer value                |
+---------------------+--------------------+----------------+------------------------------+
| Lambda              |                    | `f=@()1`       | Lambda function expression   |
+---------------------+--------------------+----------------+------------------------------+
| Land                | `Expr Expr+`       | `a&&b`         | Logical AND operator         |
+---------------------+--------------------+----------------+------------------------------+
| Lcomment            |                    | `%a`           | Line-comment                 |
+---------------------+--------------------+----------------+------------------------------+
| Le                  | `Expr Expr`        | `a<=b`         | Less-or-equal operator       |
+---------------------+--------------------+----------------+------------------------------+
| Leftelementdivision | `Expr Expr+`       | `a.\b`         | Left sclar division          |
+---------------------+--------------------+----------------+------------------------------+
| Leftmatrixdivision  | `Expr Expr+`       | `a\b`          | Left matrix division         |
+---------------------+--------------------+----------------+------------------------------+
| Log                 | `[Error Warning]+` |                | Collection of Errors         |
+---------------------+--------------------+----------------+------------------------------+
| Lor                 | `Expr Expr`        | `a||b`         | Logical OR operator          |
+---------------------+--------------------+----------------+------------------------------+
| Lt                  | `Expr Expr`        | `a<b`          | Less-then operator           |
+---------------------+--------------------+----------------+------------------------------+
| Main                | `Declares Returns` | `function f()` | Container for                |
|                     | `Params Block`     | `end`          | main function                |
+---------------------+--------------------+----------------+------------------------------+
| Matrix              | `Vector*`          | `[a]`          | Matrix container             |
+---------------------+--------------------+----------------+------------------------------+
| Matrixdivision      | `Expr Expr+`       | `a/b`          | Matrix division              |
+---------------------+--------------------+----------------+------------------------------+
| Minus               | `Expr Expr+`       | `a-b`          | Minus operator               |
+---------------------+--------------------+----------------+------------------------------+
| Mul                 | `Expr Expr+`       | `a*b`          | Multiplication operator      |
+---------------------+--------------------+----------------+------------------------------+
| Ne                  | `Expr Expr`        | `a~=b`         | Not-equal operator           |
+---------------------+--------------------+----------------+------------------------------+
| Neg                 | `Expr`             | `-a`           | Unary negative sign          |
+---------------------+--------------------+----------------+------------------------------+
| Nget                | `Expr`             | `a.(b)`        | Namefield retrival           |
+---------------------+--------------------+----------------+------------------------------+
| Not                 | `Expr`             | `~a`           | Not operator                 |
+---------------------+--------------------+----------------+------------------------------+
| Nset                | `Expr`             | `a.(b)=c`      | Namefield assignment         |
+---------------------+--------------------+----------------+------------------------------+
| Otherwise           | `Block`            | `otherwise`    | Otherwise part of Switch     |
+---------------------+--------------------+----------------+------------------------------+
| Params              | `Var*`             |                | Function parameter container |
+---------------------+--------------------+----------------+------------------------------+
| Parfor              | `Var Expr Block`   | `parfor a=b;end`| Parallel for-loop container |
+---------------------+--------------------+----------------+------------------------------+
| Plus                | `Expr Expr+`       | `a+b`          | Addition operator            |
+---------------------+--------------------+----------------+------------------------------+
| Pragma_for          |                    | `%%PARFOR str` | For-loop pragma              |
+---------------------+--------------------+----------------+------------------------------+
| Program             | `Includes Funcs`   |                | Program root                 |
|                     | `Inlines Structs`  |                |                              |
|                     | `Headers Log`      |                |                              |
+---------------------+--------------------+----------------+------------------------------+
| Project             | `Program+`         |                | Root of all programs         |
+---------------------+--------------------+----------------+------------------------------+
| Return              |                    | `return`       | Return statement             |
+---------------------+--------------------+----------------+------------------------------+
| Returns             | `Var*`             |                | Return value collection      |
+---------------------+--------------------+----------------+------------------------------+
| Set                 | `Expr*`            | `a(b)=c`       | Array value assignment       |
+---------------------+--------------------+----------------+------------------------------+
| Sget                | `Expr+`            | `a.b(c)`       | Submodule function/retrival  |
+---------------------+--------------------+----------------+------------------------------+
| Sset                | `Expr+`            | `a.b(c)=d`     | Submodule assignment         |
+---------------------+--------------------+----------------+------------------------------+
| Statement           | `Expr`             | `a`            | Stand alone statement        |
+---------------------+--------------------+----------------+------------------------------+
| String              |                    | `'a'`          | String representation        |
+---------------------+--------------------+----------------+------------------------------+
| Struct              |                    |                | Struct container             |
+---------------------+--------------------+----------------+------------------------------+
| Structs             |                    |                | Container for structs        |
+---------------------+--------------------+----------------+------------------------------+
| Switch              | `Var Case+ Other`  | `case a; end`  | Container for Switch branch  |
+---------------------+--------------------+----------------+------------------------------+
| Transpose           | `Expr`             | `a'`           | Transpose operator           |
+---------------------+--------------------+----------------+------------------------------+
| Try                 | `Block`            | `try`          | Try part of Tryblock         |
+---------------------+--------------------+----------------+------------------------------+
| Tryblock            | `Try Catch`        | `try; end`     | Container for try-blocks     |
+---------------------+--------------------+----------------+------------------------------+
| Var                 |                    | `a`            | Variable                     |
+---------------------+--------------------+----------------+------------------------------+
| Vector              | `Expr*`            | `[a]`          | Row-vector part of Matrix    |
+---------------------+--------------------+----------------+------------------------------+
| Warning             |                    |                | Element in Log               |
+---------------------+--------------------+----------------+------------------------------+
| While               | `Expr Block`       | `while a;end`  | While-loop container         |
+---------------------+--------------------+----------------+------------------------------+
"""

from .node import Node

__all__ = [
    "All", "Assign", "Assigns", "Band", "Bcomment", "Block", "Bor", "Branch",
    "Break", "Case", "Catch", "Cell", "Cget", "Colon",
    "Counter", "Cset", "Ctranspose", "Cvar", 
    "Declares", "Ecomment",
    "Elementdivision", "Elexp", "Elif", "Elmul", "Else", "End", "Eq", "Error",
    "Exp", "Expr", "Fget", "Float", "Parfor", "Pragma_for", "For", "Fset", "Func", "Funcs", "Fvar", "Ge",
    "Get", "Gt", "Header", "Headers", "If", "Imag", "Include", "Includes", "Inline",
    "Inlines", "Int", "Lambda", "Land", "Lcomment", "Le", "Leftelementdivision",
    "Leftmatrixdivision", "Log", "Lor", "Lt", "Main", "Matrix", "Matrixdivision",
    "Minus", "Mul", "Ne", "Neg", "Nget", "Not", "Nset", "Opr", "Otherwise",
    "Params", "Paren", "Plus", "Program", "Project", "Resize", "Return", "Returns",
    "Set", "Sget", "Sset", "Statement", "String", "Struct", "Structs", "Switch",
    "Transpose", "Try", "Tryblock", "Var", "Vector", "Warning", "While"
]

class Project(Node):
    def __init__(self, name="", cur=0, line=0, code="", **kws):
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
        Node.__init__(self, self, name=name, cur=cur,
                line=line, code=code, **kws)

class Program(Node):
    def __init__(self, parent, name, **kws):
        """
Represents one stand-alone script or program. Each child represents the various
aspects of script/program.

Children:
    `Includes Funcs Inlines Structs Headers Log`

All keyword arguments are passed to `mc.Node.__init__`.
    """
        self._program = self
        Node.__init__(self, parent, name=name, **kws)

class Includes(Node):
    def __init__(self, parent, **kws):
        Node.__init__(self, parent, **kws)

class Funcs(Node):
    def __init__(self, parent, line=1, **kws):
        Node.__init__(self, parent, line=line, **kws)

class Inlines(Node):
    def __init__(self, parent, **kws):
        Node.__init__(self, parent, **kws)

class Structs(Node):
    def __init__(self, parent, **kws):
        Node.__init__(self, parent, **kws)

class Headers(Node):
    def __init__(self, parent, **kws):
        Node.__init__(self, parent, **kws)

class Log(Node):
    def __init__(self, parent, **kws):
        Node.__init__(self, parent, **kws)

class Header(Node):
    def __init__(self, parent, name, **kws):
        Node.__init__(self, parent, name=name, **kws)

class Main(Node):
    def __init__(self, parent, name="main", **kws):
        Node.__init__(self, parent, name=name, **kws)

class Error(Node):
    def __init__(self, parent, name, value, **kws):
        Node.__init__(self, parent, name, value=value, **kws)
        self.prop["cls"] = name[10:]
class Warning(Node):
    def __init__(self, parent, name, value, **kws):
        Node.__init__(self, parent, name, value=value, **kws)
        self.prop["cls"] = name[10:]

class Counter(Node):
    def __init__(self, parent, name, value, **kws):
        Node.__init__(self, parent, name,
                value=value, **kws)

class Inline(Node):
    def __init__(self, parent, name, **kws):
        Node.__init__(self, parent, name, **kws)

class Include(Includes):
    def __init__(self, parent, name, **kws):
        Node.__init__(self, parent, name=name, **kws)

class Struct(Structs):          pass

class Func(Node):           pass
class Returns(Node):        pass
class Params(Node):         pass
class Declares(Node):       pass

class Block(Node):
    def __init__(self, parent, **kws):
        Node.__init__(self, parent, **kws)
class Parfor(Block):        pass
class For(Block):           pass
class While(Block):         pass
class Switch(Block):        pass
class Case(Block):          pass
class Otherwise(Block):     pass
class Branch(Block):        pass
class If(Block):            pass
class Elif(Block):          pass
class Else(Block):          pass
class Tryblock(Block):      pass
class Try(Block):           pass
class Catch(Block):         pass
class Statement(Block):     pass

class Assign(Node):         pass
class Assigns(Node):
    def __init__(self, parent, **kws):
        Node.__init__(self, parent, **kws)

class Expr(Node):
    def __init__(self, parent, **kws):
        Node.__init__(self, parent, **kws)
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
    def __init__(self, parent, **kws):
        Node.__init__(self, parent, **kws)
class Vector(Matrix):       pass

class Cell(Node):
    def __init__(self, parent, **kws):
        Node.__init__(self, parent, **kws)

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
    def __init__(self, parent, value, **kws):
        Node.__init__(self, parent, value=value, **kws)

class Float(Node):
    def __init__(self, parent, value, **kws):
        if value[0] == ".": value = "0" + value
        Node.__init__(self, parent, value=value, **kws)

class Imag(Node):
    def __init__(self, parent, value, **kws):
        Node.__init__(self, parent, value=value, **kws)

class String(Node):
    def __init__(self, parent, value, **kws):
        value = value.replace("%", "__percent__")
        Node.__init__(self, parent, value=value, **kws)

class Lambda(Node):
    def __init__(self, parent, name="", **kws):
        Node.__init__(self, parent, name=name, **kws)

class Pragma_for(Node):
    def __init__(self, parent, value, **kws):
        Node.__init__(self, parent, value=value, **kws)

class Lcomment(Node):
    def __init__(self, parent, value, **kws):
        value = value.replace("%", "__percent__")
        Node.__init__(self, parent, value=value, **kws)

class Bcomment(Node):
    def __init__(self, parent, value, **kws):
        value = value.replace("%", "__percent__")
        Node.__init__(self, parent, value=value, **kws)

class Ecomment(Node):
    def __init__(self, parent, value, **kws):
        value = value.replace("%", "__percent__")
        Node.__init__(self, parent, value=value, **kws)

class Var(Node):
    def __init__(self, parent, name, **kws):
        Node.__init__(self, parent, name=name, **kws)
class Get(Var):         pass
class Set(Var):         pass

class Fvar(Node):
    def __init__(self, parent, name, value, **kws):
        Node.__init__(self, parent, name=name, value=value, **kws)

class Cvar(Node):
    def __init__(self, parent, name, **kws):
        Node.__init__(self, parent, name, **kws)

class Cget(Node):
    def __init__(self, parent, name, **kws):
        Node.__init__(self, parent, name=name, **kws)

class Fget(Node):
    def __init__(self, parent, name, value, **kws):
        Node.__init__(self, parent, name=name, value=value, **kws)

class Sget(Node):
    def __init__(self, parent, name, value, **kws):
        Node.__init__(self, parent, name=name, value=value, **kws)

class Nget(Node):
    def __init__(self, parent, name, **kws):
        Node.__init__(self, parent, name=name, **kws)

class Cset(Node):
    def __init__(self, parent, name, **kws):
        Node.__init__(self, parent, name=name, **kws)

class Fset(Node):
    def __init__(self, parent, name, value, **kws):
        Node.__init__(self, parent, name=name, value=value, **kws)

class Sset(Node):
    def __init__(self, parent, name, value, **kws):
        Node.__init__(self, parent, name=name, value=value, **kws)

class Nset(Node):
    def __init__(self, parent, name, **kws):
        Node.__init__(self, parent, name=name, **kws)

class Resize(Node):
    def __init__(self, parent, **kws):
        Node.__init__(self, parent, **kws)

class Verbatim(Node):
    def __init__(self, parent, name, value, **kws):
        Node.__init__(self, parent, name=name, value=value, **kws)
