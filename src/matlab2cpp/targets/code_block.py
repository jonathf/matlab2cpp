"""
Code-block rules

Nodes
-----
Block : Block of code
    Contains one or more of:
        Assign, Assigns, Branch, For, Func, Set, Set2, Set3,
        Statement, Switch, Tryblock, While

For : For-loop
    Contains: Var, Expr, Block

While : While-loop
    Contains: Expr, Block

Switch : Root of switch/case
    Contains: Expr, Case, ..., (Otherwise)
    Property: hasotherwise (True if Otherwise is included)

Case : Case in switch/case
    Contains: Expr, Block

Otherwise : Alternative if all cases fails in switch/case
    Contains: Block

Branch : Root of if/then/else
    Contains: If, Elif, ..., Else
    Property: haselse (True if Else is included)

If : If in if/then/else
    Contains: Cond, Block

Elif : Else-if in if/then/else
    Contains: Cond, Block

Else : Else in if/then/else
    Contains: Block

Cond : Conditional statement
    Contains: Expr

Tryblock : Root of try/catch
    Contains: Try, Catch, ...

Try : Try in try/catch
    Contains: Block

Catch : Catch in try/catch
    Contains: Block

Statement : Stand-alone codeline without assignment etc.
    Example: "y"
    Contains: Expr

Assigns : Multiple variable assignment
    Example: "[x, y] = f(4)"
    Example: "[x, y] = z"
    Contains: Assigned (lhs), Assignees (rhs)
    Rule: code_block.py
    Property: isvariable (True if Assignees is variable)

Assigned : Lhs in Assigns
    Contains one or more: Var
    Rule : code_block.py
"""


Statement = "%(0)s ;"
While = "while(%(0)s)\n{\n%(1)s\n}"
Cond = "", ",", ""

Branch = "", "\n", ""

def If(node):
    if len(node) == 1:
        return "if (%(0)s)\n{\n// Empty block\n}"
    return "if (%(0)s)\n{\n%(1)s\n}"

Elif = "else if (%(0)s)\n{\n%(1)s\n}"
Else = "else\n{\n%(0)s\n}"

def Switch(node):
    if node[0].cls != "Var" and node[0].type != "TYPE":
        node[0].auxillary()

    if node[-1].cls == "Otherwise":
        return ["if (", " == "] +\
                ["\n}\nelse if (%(0)s == "]*(len(node)-3) +\
                ["\n}\nelse\n{\n", "\n}"]
    else:
        return "if (%(0)s == ", "\n}\nelse if (%(0)s == ", "\n}"

Case = "%(0)s)\n{\n%(1)s"
Otherwise = "%(0)s"

def Tryblock(node):
    return "", "\n", ""
Try = "try\n{\n", "", "\n}"
def Catch(node):
    name = node["name"]
    if name[0] != "@":
        return "catch ("+node.type()+" "+name+")\n{\n", "", "\n}"
    return "catch (...)\n{\n", "", "\n}"



def Block(node):
    return "", "\n", ""

def Assigns(node):

    assigned, expression = node[:-1], node[-1]

    if expression["class"] != "Var":
        expression = expression.auxillary()

    out = ""
    for i in xrange(len(assigned)):
        var = assigned[i]
        out += var + " = " + expression + "(%d) ;\n" % i
    out = out[:-1]
    return out + " ;"



def For(node):

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

    return """for %(0)s=%(1)s
{
%(2)s
}"""

Bcomment = "/*%(value)s*/"
Lcomment = "//%(value)s"
