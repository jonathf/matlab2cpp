from variables import *

def Counter(node):
    return "%(name)s = %(value)s"

# def Var(node):
#  
#     index = node.declare.parent.names.index("_size")
#     number = node.declare.parent[index].value
#     return node.name + "[" + number + "]"

def Vector(node):
    node.type = node[0].type
    return "%(0)s"

def Matrix(node):
    node.type = node[0].type
    return "%(0)s"

