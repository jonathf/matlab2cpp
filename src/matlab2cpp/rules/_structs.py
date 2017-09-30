#from assign import Assign
from .variables import *
import matlab2cpp as mc

Declare = "struct %(name)s"

def Counter(node):
    return "%(name)s = %(value)s"

#def Fvar(node): #defined in variables.py
#    return "%(name)s.%(value)s"
    
def Fget(node):
    pass

def Fset(node):
    return "%(name)s.%(value)s[", ", ", "-1]"

def Matrix(node):
    if node.backend == "structs":
        if node[0].cls == "Vector":
            if len(node[0]) == 1:
                return "%(0)s"
    return "[", ", ", "]"

"""def Assign(node):
    lhs, rhs = node
    print('here')
    # assign a my_var = [a.val], a is a structs, my_var should be a vec
    if node[1].cls == "Matrix" and node[1].backend == "structs":
        element = rhs[0][0]
        if element.backend == "structs":
            size = rhs.str
            var = lhs.name
            name = element.name
            value = element.value

            declares = node.func[0]
            if "_i" not in declares:
                declare = mc.collection.Var(declares, "_i")
                declare.type = "int"
                declare.backend = "int"
                declares.translate()
            
            string = var + ".resize(" + size + ") ;\n" +\
                "for (_i=0; _i<" + size + "; ++_i)\n  "+\
                var + "[_i] = " + name + "[_i]." + value + " ;"

            return string

    return "%(0)s = %(1)s"""""

