"""
Program rules

Nodes
-----
Program : The root node
    Contains: Func, ...
    Rule: program.py
"""
import re

def Program(tree):

    lines = "\n\n".join(map(str, tree[:])).split("\n")
    indent = 0

    for i in xrange(len(lines)):
        line = lines[i]

        # Fix indentation and linesplit
        if line == "}":
            indent -= 1
        line = "  "*indent + line

        if line and line[-1] == "{":
            indent += 1
        lines[i] = line

    text = "\n".join(lines)

    # Cosmetic fix
    for p0,p1,p2 in set(re.findall(r"(([ ,(])(-?\d+)-1)", text)):
        val = int(p2)-1
        if val:     val = p1+str(val)
        else:       val = p1+"0"

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


Includes = "", "\n\n", ""
Include = "%(value)s"


