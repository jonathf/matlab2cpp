from _variables import *

Structs = "", "\n\n", ""
def Declare(node):
    name = node["name"]
    return name.capitalize() + " " + name + " ;"

def Struct(node):

    name = node["name"].capitalize()

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
