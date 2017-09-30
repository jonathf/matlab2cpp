from .assign import Assign
from .variables import *

Declare = "string %(name)s ;"

def String(node):
    if node.name or node.parent.backend != "matrix":
        return '"%(value)s"'
    else:
        return 'std::string("%(value)s")'
        
