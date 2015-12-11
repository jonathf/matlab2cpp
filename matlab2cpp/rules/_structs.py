from assign import Assign
from variables import *

def Counter(node):
    return "%(name)s = %(value)s"

def Fget(node):
    pass

def Fset(node):
    return "%(name)s.%(value)s[", ", ", "-1]"


def Matrix(node):
    return ""

def Assign(node):
    return ""
