from variables import *

def Declare(node):
    name = node["name"]
    return "_"+name.capitalize() + " " + name + " ;"

