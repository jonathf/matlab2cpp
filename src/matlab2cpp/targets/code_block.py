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

Assigned =  "*", ", *", " "

def Assigns(node):

    assigned, expression = node[:]
    if expression["class"] == "Var":
        out = ""
        for i in xrange(len(assigned)):
            var = assigned[i]
            out += var + " = " + expression + "(%d) ;\n" % i
        out = out[:-1]
        return out + " ;"

    return "%(name)s(%(0)s, %(1)s) ;"

Sets = "", ", ", ""
Statement = "%(0)s ;"
While = "while(%(0)s)\n{\n%(1)s\n}"
Cond = "", ",", ""

Branch = "", "\n", ""
If = "if (%(0)s)\n{\n%(1)s\n}"
Elif = "else if (%(0)s)\n{\n%(1)s\n}"
Else = "else\n{\n%(0)s\n}"

#  sw = [""]
#  def Switch(node):
#      sw[0], _ = "", sw[0]
#      return "_case_"+_+" = ", " ;\n", "\nelse", ""
#  
#  def Case(node):
#      if not sw[0]:
#          sw[0] = node[0].type()
#      return "if (_case_"+sw[0]+" == %(0)s)\n{\n%(1)s\n}"
#  
#  def Otherwise(node):
#      return "\n{\n%(0)s\n}"

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


def For(node):

    var, range = node[:2]
    if range["class"] == "Colon":
        var.suggest("int")
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
