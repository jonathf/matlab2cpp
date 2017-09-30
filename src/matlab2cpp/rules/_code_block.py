"""
This module contains all the codeblock related nodes.
Each node can then here be nested on top of each other.
They are static in the sense that there only exists one copy, unaffected by type
and have the backend fixd to `code_block`.
"""
import os

import matlab2cpp as mc
from . import parallel


def Statement(node):
    """
Stand-alone codeline without assignment etc.

Args:
    node (Statement): Current position in node-tree

Return:
    str : Translation of current node.

Children:
    Expression

    Expression:
        Right hand side of expression

Examples:
    >>> print(mc.qscript("'text'"))
    "text" ;
    >>> print(mc.qscript("123"))
    123 ;
    >>> print(mc.qscript("[1,2]"))
    {1, 2} ;
    >>> print(mc.qscript("a"))
    a ;
    >>> print(mc.qscript("f()"))
    f() ;
    """
    return "%(0)s ;"


def While(node):
    """
While-loop

Args:
    node (While): Current position in node-tree

Return:
    str : Translation of current node.

Children:
    Expression Block

    Expression:
        Loop condition
    Block:
        Loop content

Examples:
    >>> print(mc.qscript("while 1, f()"))
    while (1)
    {
      f() ;
    }
    """
    node.error("While-loops are currently not supported.")
    return "while (%(0)s)\n{\n%(1)s\n}"

def Branch(node):
    """
Root of if/then/else branch

Args:
    node (Branch): Current position in node-tree

Return:
    str : Translation of current node.

Children:
    If Elif* Else?

    If:
        If block
    Elif:
        Elseif block
    Else:
        Else block

Examples:
    >>> print(mc.qscript("if a, b; elseif c, d; else e"))
    if (a)
    {
      b ;
    }
    else if (c)
    {
      d ;
    }
    else
    {
      e ;
    }
    """
    return "", "\n", ""

def If(node):
    """
If in if/then/else branch


Args:
    node (If): Current position in node-tree

Return:
    str : Translation of current node.

Children:
    Expression Block

    Expression:
        Branch condition
    Block:
        Code to be evaluated give condition

Examples:
    >>> print(mc.qscript("if a, b"))
    if (a)
    {
      b ;
    }
    >>> print(mc.qscript("if a, end"))
    if (a)
    {
      // Empty block
    }
    """
    return """if (%(0)s)
{
%(1)s
}"""


def Elif(node):
    """
Elseif in if/then/else branch

Args:
    node (Elif): Current position in node-tree

Return:
    str : Translation of current node.

Children:
    Expression Block

    Expression:
        Branch condition
    Block:
        Code to be evaluated give condition

Examples:
    >>> print(mc.qscript("if a, b; elseif c, d"))
    if (a)
    {
      b ;
    }
    else if (c)
    {
      d ;
    }
    >>> print(mc.qscript("if a, b; elseif c, end"))
    if (a)
    {
      b ;
    }
    else if (c)
    {
      // Empty block
    }
    """
    return """else if (%(0)s)
{
%(1)s
}"""


def Else(node):
    """
Else in if/then/else branch

Args:
    node (Else): Current position in node-tree

Return:
    str : Translation of current node.

Children:
    Block

    Block:
        Code to be evaluated give condition

Examples:
    >>> print(mc.qscript("if a, b; else c"))
    if (a)
    {
      b ;
    }
    else
    {
      c ;
    }
    >>> print(mc.qscript("if a, b; else; end"))
    if (a)
    {
      b ;
    }
    else
    {
      // Empty block
    }
    """
    return """else
{
%(0)s
}"""


def Switch(node):
    """
Root of switch/case branch

Args:
    node (Switch): Current position in node-tree

Return:
    str : Translation of current node.

Children:
    Expression Case+ Otherwise?

    Expression:
        Test-expression
    Case:
        Case-block
    Otherwise:
        Otherwise-block

Examples:
    >>> print(mc.qscript("a=1; switch a; case b; c; otherwise; d"))
    a = 1 ;
    if (b == a)
    {
      c ;
    }
    else
    {
      d ;
    }
    """
    if node[0].cls == "Var":
        out = ""

    # create switch variable
    else:
        node.type = node[0].type
        out = "%(type)s _var_%(type)s = %(0)s ;\n"
    return out + "\n".join(map(str, node[1:]))

def Case(node):
    """
Case in switch/case

Args:
    node (Case): Current position in node-tree

Return:
    str : Translation of current node.

Children:
    Expression Block

    Expression:
        Condition
    Block:
        Code to be evaluated give condition

Example:
    >>> print(mc.qscript("switch 1; case b; c"))
    int _var_int = 1 ;
    if (b == _var_int)
    {
      c ;
    }
    >>> print(mc.qscript("a=1; switch a; case b; c;"))
    a = 1 ;
    if (b == a)
    {
      c ;
    }
    """

    # first in row
    if node is node.parent[1]:
        out = "if (%(0)s == "
    else:
        out = "else if (%(0)s == "

    # define name
    if node.parent[0].cls == "Var":
        out = out + node.parent[0].name

    else:
        node.type = node.parent[0].type
        out += "_var_%(type)s"

    out = out + ")\n{\n%(1)s\n}"
    return out


def Otherwise(node):
    """
Otherwise in switch/case

Args:
    node (Otherwise): Current position in node-tree

Return:
    str : Translation of current node.

Children:
    Block

    Block:
        Code to be evaluated give condition

Example:
    >>> print(mc.qscript("switch 1; case a; b; otherwise; c"))
    int _var_int = 1 ;
    if (a == _var_int)
    {
      b ;
    }
    else
    {
      c ;
    }
    """
    return "else\n{\n%(0)s\n}"

def Tryblock(node):
    """
Root of try/catch

Args:
    node (Tryblock): Current position in node-tree

Return:
    str : Translation of current node.

Children:
    Try Catch+

    Try:
        Try-block
    Catch:
        Catch-block

Examples:
    >>> print(mc.qscript("try; a; catch; b"))
    try
    {
      a ;
    }
    catch (...)
    {
      b ;
    }
    """
    node.error("Try-statement are currently not supported.")
    return "", "\n", ""


def Try(node):
    """Try

Args:
    node (Try): Current position in node-tree

Return:
    str : Translation of current node.

Children:
    Block

    Block : Try content
    """
    return "try\n{\n", "", "\n}"


def Catch(node):
    """
Catch-block in Try/Catch

Args:
    node (Catch): Current position in node-tree

Return:
    str : Translation of current node.

Children:
    Block

    Block : Catch content
    """
    
    name = node.name

    if not name:
        return "catch (...)\n{\n", "", "\n}"

    if name[0] != "@":
        return "catch ("+node.type()+" "+name+")\n{\n", "", "\n}"

    return "catch (...)\n{\n", "", "\n}"


def Block(node):
    """
Codeblock

Args:
    node (Block): Current position in node-tree

Return:
    str : Translation of current node.

Children:
    Codeline*

    Codeline : Sub-block, statement or assigments

Examples:
    >>> print(mc.qscript("a; if b; c; end; d"))
    a ;
    if (b)
    {
      c ;
    }
    d ;
    """
    if not len(node):
        return "// Empty block"

    out = str(node[0])
    for child in node[1:]:
        if child.cls == "Ecomment":
            out = out + " " + str(child)
        else:
            out = out + "\n" + str(child)

    return out

def Assigns(node):
    """
Multiple assignment

Args:
    node (Assigns): Current position in node-tree

Return:
    str : Translation of current node.

Children:
    Lhs Lhs+ Expression

    Lhs:
        Left hand side of assignment
    Expression:
        Right hand side of assignment

Examples:
    >>> print(mc.qscript("[a,b,c] = d"))
    [a, b, c] = d ;
    >>> print(mc.qscript("[a,b,c] = [1,2,3]"))
    sword __aux_irowvec_1 [] = {1, 2, 3} ;
    _aux_irowvec_1 = irowvec(__aux_irowvec_1, 3, false) ;
    a = _aux_irowvec_1(0) ;
    b = _aux_irowvec_1(1) ;
    c = _aux_irowvec_1(2) ;
    """

    # left-hand-side not a variable -> create auxillary variable that is
    if node[-1].cls != "Var":
        node[-1].auxiliary()

    # split into multiple lines
    out = ""
    for i in xrange(len(node[:-1])):
        i = str(i)
        out += "%(" +i+ ")s = " +str(node[-1])+ "(" +i+ ") ;\n"
    out = out[:-1]

    return out

def Parfor(node):
    """
Parfor-loop

Args:
    node (For): Current position in node-tree

Return:
    str : Translation of current node.

Children:
    Var Expression Block

    Var:
        Variable running the loop
    Expression:
        Container for loop (special handle for Colon)
    Block:
        Content to loop over

Examples:
    >>> print(mc.qscript("parfor i=1:10; a"))
    for (i=1; i<=10; i++)
    {
      a ;
    }
    >>> print(mc.qscript("parfor i=1:2:10; a"))
    for (i=1; i<=10; i+=2)
    {
      a ;
    }
    >>> print(mc.qscript("parfor i=a; b"))
    for (int _i=0; _i<length(a); _i++)
    {
      i = a[_i] ;
      b ;
    }
    """
    var, range = node[:2]
    omp = node.project.builder.enable_omp
    tbb = node.project.builder.enable_tbb

    if range.cls == "Colon":

        # <start>:<stop>
        if len(range) == 2:
            start, stop = range
            step = "1"
        
        # <start>:<step>:<stop>
        elif len(range) == 3:
            start, step, stop = range
        start, step, stop = map(str, [start, step, stop])

        # return
        if omp:
            node.include("omp")

            out = parallel.omp(node, start, stop, step)

        elif tbb:
            node.include("tbb")

            #windows
            if os.name == 'nt':
                node.include("no_min_max")

            out = parallel.tbb(node, start, stop, step)

            return out

        else:
            out = "for (%(0)s=" + start + \
                  "; %(0)s<=" + stop + "; %(0)s"

        # special case for '+= 1'
        if step == "1":
            out += "++"
        else:
            out += "+=" + step

        out += ")\n{\n%(2)s\n}"

        #if tbb:
        #    out += "\n});"

        return out

    # default
    return """for (int _%(0)s=0; _%(0)s<length(%(1)s); _%(0)s++)
{
%(0)s = %(1)s[_%(0)s] ;
%(2)s
}"""

def For(node):
    """
For-loop

Args:
    node (For): Current position in node-tree

Return:
    str : Translation of current node.

Children:
    Var Expression Block

    Var:
        Variable running the loop
    Expression:
        Container for loop (special handle for Colon)
    Block:
        Content to loop over

Examples:
    >>> print(mc.qscript("for i=1:10; a"))
    for (i=1; i<=10; i++)
    {
      a ;
    }
    >>> print(mc.qscript("for i=1:2:10; a"))
    for (i=1; i<=10; i+=2)
    {
      a ;
    }
    >>> print(mc.qscript("for i=a; b"))
    for (int _i=0; _i<length(a); _i++)
    {
      i = a[_i] ;
      b ;
    }
    """
    var, range = node[:2]
    omp = node.project.builder.enable_omp
    tbb = node.project.builder.enable_tbb

    index = node.parent.children.index(node)
    parallel_loop = node.parent.children[index - 1].cls in ["Pragma_for", "Tbb_for"]

    if range.cls == "Colon":
        # <start>:<stop>
        if len(range) == 2:
            start, stop = range
            step = "1"

        # <start>:<step>:<stop>
        elif len(range) == 3:
            start, step, stop = range
        start, step, stop = map(str, [start, step, stop])

        if omp and parallel_loop:
            node.include("omp")

            out = parallel.omp(node, start, stop, step)

        elif tbb and parallel_loop:
            node.include("tbb")

            #windows
            if os.name == 'nt':
                node.include("no_min_max")

            out = parallel.tbb(node, start, stop, step)

            return out

        else:
            out = "for (%(0)s=" + start + \
                  "; %(0)s<=" + stop + "; %(0)s"

        # special case for '+= 1'
        if step == "1":
            out += "++"
        else:
            out += "+=" + step

        out += ")\n{\n%(2)s\n}"

        return out

    # i = [1, 2, 3, 4]
    if len(node) == 3:
        if node[1].dim in [1, 2]:
            return """for (auto %(0)s : %(1)s)
{
%(2)s
}
"""
    # default
    return """for (int _%(0)s=0; _%(0)s<length(%(1)s); _%(0)s++)
{
%(0)s = %(1)s[_%(0)s] ;
%(2)s
}"""

def Pragma_for(node):
    #node.include("omp")
    #return node
    #return "//__percent__%(value)s"
    return ""

def Bcomment(node):
    """
Block comment

Args:
    node (Bcomment): Current position in node-tree

Return:
    str : Translation of current node.

Examples:
    >>> print(mc.qscript("function f(); %{ comment %}"))
    void f()
    {
      /* comment */
    }
    """
    return "/*%(value)s*/"


def Lcomment(node):
    """
Line comment

Args:
    node (Lcomment): Current position in node-tree

Return:
    str : Translation of current node.

Examples:
    >>> print(mc.qscript("function f(); % comment"))
    void f()
    {
      // comment
    }
    """
    return "//%(value)s"


def Ecomment(node):
    """
End comment

Args:
    node (Ecomment): Current position in node-tree

Return:
    str : Translation of current node.

Examples:
    >>> print(mc.qscript("a % comment"))
    a ; // comment
    """
    return "//%(value)s"


if __name__ == "__main__":
    import doctest
    doctest.testmod()
