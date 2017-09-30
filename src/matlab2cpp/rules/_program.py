import re

import matlab2cpp as mc
from . import armadillo as arma
from .function import type_string

def add_indenting(text):
    """Add identing to text
    """

    lines = text.split("\n")

    indent = 0
    for i in xrange(len(lines)):
        line = lines[i]

        # Fix indentation and linesplit
        if line in ("}", "} ;") or line[:4] == "} //":
            indent -= 1
            line = "  "*indent + line

        elif line == "{":
            line = "  "*indent + line
            indent += 1
        else:
            line = "  "*indent + line
        lines[i] = line

    text = "\n".join(lines)

    return text


def number_fix(text):
    """Code has allot of '-1' statements in indexing. This code substitutes
explicit number subtractions with the single index equivalent.

Examples:
    >>> print(number_fix("a(8-1, 5-1)"))
    a(7, 4)
    """
    # Cosmetic fix
    for p0,p1,p2 in set(re.findall(r"(([ ,(\[])(-?\d+)-1(?![*/]))", text)):
        val = int(p2)-1
        val = p1+str(val)
        text = val.join(text.split(p0))

    for p0,p1,p2 in \
            set(re.findall(r"(([+\- ])(\d+)-1(?![*/]))", text)):
        if p1=="-":     val = int(p2)+1
        else:           val = int(p2)-1
        if val:         val = p1+str(val)
        else:           val = ""
        text = val.join(text.split(p0))

    text = re.sub(r"\+-", r"-", text)
    return text


def strip(text):
    """Remove trailing spaces and linefeeds.
    """
    if not text: return text

    start = 0
    while text[start] in "\n ":
        start += 1
    end = 0
    while text[end-1] in "\n ":
        end -= 1

    if end:
        text = text[start:end]
    else:
        text = text[start:]

    return text

def Project(node):
    return ""

def Program(node):
    arma.include(node)
    return ""

def Includes(node):
    return "", "\n", ""

def Headers(node):
    return "", "\n", ""


def Header(node):
    func = node.program[1][node.program[1].names.index(node.name)]
    if func.backend == "func_return":

        # if -ref, -reference flag option
        if node.project.builder.reference:

            code = func[1][0].type + " " + func.name + "(" +\
                   ", ".join(["const " + type_string(p) + "& " + p.name if p.dim > 0 else
                           type_string(p) + " " + p.name for p in func[2]]) + ") ;"

        else:
            code = func[1][0].type + " " + func.name + "(" +\
            ", ".join([type_string(p) + " " + p.name for p in func[2]]) + ") ;"


    elif func.backend == "func_returns" and not func[1]:

        # if -ref, -reference flag option
        if node.project.builder.reference:
            code = "void " + func.name + "(" +\
                ", ".join(["const " + type_string(p) + "& " + p.name if p.dim > 0 else
                           type_string(p) + " " + p.name for p in func[2]]) + ") ;"

        else:
            code = "void " + func.name + "(" +\
            ", ".join([type_string(p) + " " + p.name for p in func[2]]) + ") ;"

    elif func.backend == "func_returns" and func[1]:

        # if -ref, -reference flag option
        if node.project.builder.reference:
            code = "void " + func.name + "(" +\
                ", ".join(["const " + type_string(p) + "& " + p.name if p.dim > 0 else
                           type_string(p) + " " + p.name for p in func[2]]) + ", " +\
                ", ".join([type_string(p) + "& " + p.name for p in func[1]]) + ") ;"

        else:
            code = "void " + func.name + "(" +\
            ", ".join([type_string(p) + " " + p.name for p in func[2]]) + ", " +\
            ", ".join([type_string(p) + "& " + p.name for p in func[1]]) + ") ;"



    return code

Include = "%(name)s"


def Funcs(node):
    text = "\n\n".join(map(str, node[:]))
    # text = add_indenting(text)
    # text = number_fix(text)
    text = re.sub(r"\n *(\n *)+", r"\n\n", text)
    # text = strip(text)

    return text

def Inlines(node):

    if not node:
        return ""

    text = "\n\n".join([n.name for n in node])

    text = """#ifndef MCONVERT_H
#define MCONVERT_H

namespace m2cpp
{
""" + text + """
}

#endif
"""
    # text = add_indenting(text)
    return text

def Inline(node):
    return ""

Structs = "", "\n\n", ""

def Log(node):
    return "", "\n\n", ""


def Error(node):
    cls = node.name.split(":")[0]
    return 'Error in class ' + cls + ''' on line %(line)d:
%(code)s
''' + " "*node.cur + "^\n%(value)s"

def Warning(node):
    cls = node.name.split(":")[0]
    return 'Warning in class ' + cls + ''' on line %(line)d:
%(code)s
''' + " "*node.cur + "^\n%(value)s"

def Struct(node):

    name = "_"+node.name.capitalize()
    out = "struct " + name + "\n{"

    declares = {}
    for child in node[:]:

        type = child.type
        if type == "func_lambda":
            type == "std::function"

        if type == "structs":
            continue

        if type not in declares:
            declares[type] = []

        declares[type].append(child)

    for key, val in declares.items():
        out = out + "\n" + key + " " + ", ".join([str(v) for v in val]) + " ;"
    out = out + "\n} ;"

    # out = add_indenting(out)

    return out

if __name__ == "__main__":
    import doctest
    doctest.testmod()
