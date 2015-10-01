"""
This module contains all the codeblock related nodes.
Each node can then here be nested on top of each other.
They are static in the sense that there only exists one copy, unaffected by type
and have the backend fixd to `code_block`.
"""

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
    >>> print mc.qtranslate("'text'")
    "text" ;
    >>> print mc.qtranslate("123")
    123 ;
    >>> print mc.qtranslate("[1,2]")
    {1, 2} ;
    >>> print mc.qtranslate("a")
    a ;
    >>> print mc.qtranslate("f()")
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
    >>> print mc.qtranslate("while 1, f()")
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
    >>> print mc.qtranslate("if a, b; elseif c, d; else e")
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
    >>> print mc.qtranslate("if a, b")
    if (a)
    {
    b ;
    }
    >>> print mc.qtranslate("if a, end")
    if (a)
    {
    // Empty block
    }
    """
    return "if (%(0)s)\n{\n%(1)s\n}"


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
    >>> print mc.qtranslate("if a, b; elseif c, d")
    if (a)
    {
    b ;
    }
    else if (c)
    {
    d ;
    }
    >>> print mc.qtranslate("if a, b; elseif c, end")
    if (a)
    {
    b ;
    }
    else if (c)
    {
    // Empty block
    }
    """
    return "else if (%(0)s)\n{\n%(1)s\n}"


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
    >>> print mc.qtranslate("if a, b; else c")
    if (a)
    {
    b ;
    }
    else
    {
    c ;
    }
    >>> print mc.qtranslate("if a, b; else; end")
    if (a)
    {
    b ;
    }
    else
    {
    // Empty block
    }
    """
    return "else\n{\n%(0)s\n}"


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
    >>> print mc.qtranslate("a=1; switch a; case b; c; otherwise; d")
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
    >>> print mc.qtranslate("switch 1; case b; c")
    int _var_int = 1 ;
    if (b == _var_int)
    {
    c ;
    }
    >>> print mc.qtranslate("a=1; switch a; case b; c;")
    a = 1 ;
    if (b == a)
    {
    c ;
    }
    """

    if node is node.parent[1]:
        out = "if (%(0)s == "
    else:
        out = "else if (%(0)s == "
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
    >>> print mc.qtranslate("switch 1; case a; b; otherwise; c")
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
    >>> print mc.qtranslate("try; a; catch; b")
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
    
    name = node["name"]
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
    >>> print mc.qtranslate("a; if b; c; end; d")
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
    >>> print mc.qtranslate("[a,b,c] = d")
    a = d(0) ;
    b = d(1) ;
    c = d(2) ;
    >>> print mc.qtranslate("[a,b,c] = 4")
    _aux_int_1 = 4 ;
    a = _aux_int_1(0) ;
    b = _aux_int_1(1) ;
    c = _aux_int_1(2) ;
    """

    if node[-1].cls != "Var":
        node[-1].auxiliary()

    out = ""
    for i in xrange(len(node[:-1])):
        i = str(i)
        out += "%(" +i+ ")s = " +str(node[-1])+ "(" +i+ ") ;\n"
    out = out[:-1]
    return out

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
    >>> print mc.qtranslate("for i=1:10; a")
    for (i=1; i<=10; i++)
    {
    a ;
    }
    >>> print mc.qtranslate("for i=1:2:10; a")
    for (i=1; i<=10; i+=2)
    {
    a ;
    }
    >>> print mc.qtranslate("for i=a; b")
    for (int _i=0; _i<length(a); _i++)
    {
    i = a[_i] ;
    b ;
    }
    """

    var, range = node[:2]

    if range["class"] == "Colon":
        if len(range) == 2:
            start, stop = range
            step = "1"
        elif len(range) == 3:
            start, step, stop = range
        start, step, stop = map(str, [start, step, stop])

        out = "for (%(0)s=" + start + \
            "; %(0)s<=" + stop + "; %(0)s"
        if step == "1":
            out += "++"
        else:
            out += "+=" + step
        out += ")\n{\n%(2)s\n}"
        return out

    return """for (int _%(0)s=0; _%(0)s<length(%(1)s); _%(0)s++)
{
%(0)s = %(1)s[_%(0)s] ;
%(2)s
}"""

def Bcomment(node):
    """
Block comment

Args:
    node (Bcomment): Current position in node-tree

Return:
    str : Translation of current node.

Examples:
    >>> print mc.qtranslate("%{ comment %}")
    /* comment */
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
    >>> print mc.qtranslate("% comment")
    // comment
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
    >>> print mc.qtranslate("a % comment")
    a ; // comment
    """
    return "//%(value)s"


if __name__ == "__main__":
    import matlab2cpp as mc
    import doctest
    doctest.testmod()
