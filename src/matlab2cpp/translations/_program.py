import re
import os
import time
from datetime import datetime as date

def add_indenting(text):

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

    # Cosmetic fix
    for p0,p1,p2 in set(re.findall(r"(([ ,(])(-?\d+)-1)", text)):
        val = int(p2)-1
        val = p1+str(val)
        text = val.join(text.split(p0))

    for p0,p1,p2 in \
            set(re.findall(r"(([+\- ])(\d+)-1)", text)):
        if p1=="-":     val = int(p2)+1
        else:           val = int(p2)-1
        if val:         val = p1+str(val)
        else:           val = ""
        text = val.join(text.split(p0))

    text = re.sub(r"\+-", r"-", text)
    return text

def strip(text):

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
    return ""

def Includes(node):
    return "", "\n", ""

def Headers(node):
    return "", "\n", ""

def Header(node):
    func = node.program[1][node.program[1].names.index(node.name)]
    if func.backend == "func_return":
        code = func[1][0].type + " " + func.name + "(" +\
            ", ".join([p.type + " " + p.name for p in func[2]]) + ") ;"

    elif func.backend == "func_returns" and not func[1]:
        code = "void " + func.name + "(" +\
            ", ".join([p.type + " " + p.name for p in func[2]]) + ") ;"

    elif func.backend == "func_returns" and func[1]:
        code = "void " + func.name + "(" +\
            ", ".join([p.type + " " + p.name for p in func[2]]) + ", " +\
            ", ".join([p.type + "& " + p.name for p in func[1]]) + ") ;"
    return code

Include = "%(name)s"

def Funcs(node):
    text = "\n\n".join(map(str, node[:]))
    text = add_indenting(text)
    text = number_fix(text)
    text = re.sub(r"\n *(\n *)+", r"\n\n", text)
    text = strip(text)

    if node and node[0].cls == "Main":
        text = '#include "' + os.path.basename(node.file) + '.ipp"\n\n' + text

    return text

def Inlines(node):

    if not node:
        return ""

    text = "\n\n".join(map(str, node[:]))

    text = """#ifndef MCONVERT_H
#define MCONVERT_H

namespace m2cpp
{
""" + text + """
}

#endif
"""
    text = add_indenting(text)
    return text

Inline = "%(name)s"

Structs = "", "\n\n", ""

def Log(node):
    if not node.children:
        return ""
    ts = time.time()
    log = "Translated on " +\
            date.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S\n\n')
    return log, "\n\n", ""


def Error(node):
    return '''Error [%(line)d,%(cur)d]: %(value)s in %(cls)s
"%(code)s"'''

def Warning(node):
    return '''Warning [%(line)d,%(cur)d]: %(value)s in %(cls)s
"%(code)s"'''

def Struct(node):

    name = "_"+node["name"].capitalize()

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

    out = "struct " + name + "\n{"
    for key, val in declares.items():
        out = out + "\n" + key + " " + ", ".join([str(v) for v in val]) + " ;"
    out = out + "\n} ;"

    return out
