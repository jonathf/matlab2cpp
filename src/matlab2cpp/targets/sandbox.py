
def Assign_alt(node):
    return "%(0)s = %(1)s ;"

def Assigned_alt(node):
    if len(node) == 1:
        return "%(0)s"
    return "[", ", ", "]"

def Assignees_alt(node):
    return "%(0)s"

def Var_alt(node): #ID
    return "%(name)s", "", ""

def Call_alt(node): #ID

    if len(node) == 1:
        return "%(name)s(%(0)s)"

    return ("%(name)s",) + ("",)*(len(node)-2) + ("(", ")")

def Cell_alt(node): #ID
    return "{%(name)s}"

def Field1_alt(node): #ID
    return ".%(name)s"

def Field2_alt(node): #ID
    return ".%(name)s(", "", ")"

def Field3_alt(node):
    return ".(", ""; ")"


def Get_alt(node):
    return "%(0)s"
