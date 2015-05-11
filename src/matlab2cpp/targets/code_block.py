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
While = "while (%(0)s)\n{\n%(1)s\n}"
Cond = "", ",", ""

Branch = "", "\n", ""

def If(node):
    if len(node) == 1:
        return "if (%(0)s)\n{\n// Empty block\n}"
    return "if (%(0)s)\n{\n%(1)s\n}"

def Elif(node):
    if len(node) == 1:
        return "else if (%(0)s)\n{\n// Empty block\n}"
    return "else if (%(0)s)\n{\n%(1)s\n}"
Else = "else\n{\n%(0)s\n}"

def Switch(node):
    if node[0].cls != "Var" and node[0].type != "TYPE":
        node[0].auxiliary()
    return "\n".join(map(str, node[1:]))
#      return "", "\n", ""
#  
#      if node[-1].cls == "Otherwise":
#          return ["if (", " == "] +\
#                  ["\n}\nelse if (%(0)s == "]*(len(node)-3) +\
#                  ["\n}\nelse\n{\n", "\n}"]
#      else:
#          return "if (%(0)s == ", "\n}\nelse if (%(0)s == ", "\n}"

def Case(node):
    var = node.parent[0]

    if node is node.parent[1]:
        if var.cls != "Var" and var.type != "TYPE":
            var.auxiliary()

        return "if (%(0)s == " + str(var)+")\n{\n%(1)s\n}"

    return "else if (%(0)s == " + str(var) + ")\n{\n%(1)s\n}"

def Otherwise(node):
    return "else\n{\n%(0)s\n}"

def Tryblock(node):
    return "", "\n", ""
Try = "try\n{\n", "", "\n}"
def Catch(node):
    name = node["name"]
    if not name:
        return "catch (...)\n{\n", "", "\n}"
    if name[0] != "@":
        return "catch ("+node.type()+" "+name+")\n{\n", "", "\n}"
    return "catch (...)\n{\n", "", "\n}"

def Block(node):
    if not len(node):
        return ""

    out = str(node[0])
    for child in node[1:]:
        if child.cls == "Ecomment":
            out = out + " " + str(child)
        else:
            out = out + "\n" + str(child)

    return out

def Assigns(node):

    if node[-1]["class"] != "Var":
        node[-1].auxiliary()

    out = ""
    n = str(len(node)-1)
    for i in xrange(len(node[:-1])):
        i = str(i)
        out += "%(" +i+ ")s = %(" +n+ ")s(" +i+ ") ;\n"
    out = out[:-1]
    return out

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
Ecomment = "//%(value)s"
