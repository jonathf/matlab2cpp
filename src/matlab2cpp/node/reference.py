"""
Each node has a set of attributes that allows for quick access to properties and
other node of interest.  For example, if `node` has a name, it can be referred
to by `node.name`.  Another example is to access the parent node by
`node.parent`.

Note that, if a reference does not exist, the node itself will be returned.
"""

groups = [
    "Assign", "Assigns", "Branch", "For", "Func", "Main",
    "Set", "Cset", "Fset", "Nset", "Sset",
    "Get", "Cget", "Fget", "Nget", "Sget",
    "Statement", "Switch", "Tryblock", "Matrix",
    "While", "Block", "Node", "Transpose", "Ctranspose",
]

nondeclares = ("Program", "Project", "Include", "Includes", "Struct", "Structs")
structvars = ("Fvar", "Fget", "Fset", "Nget", "Nset", "Sget", "Sset")

class Property_reference(object):
    "general property node"

    def __init__(self, name, default=None):
        self.name = name

    def __get__(self, instance, owner):
        return instance.prop[self.name]

    def __set__(self, instance, value):
        instance.prop[self.name] = value

class Recursive_property_reference(object):
    "recursive property node"

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):

        a = instance.prop[self.name]
        if not (a is None):
            return a

        assert not (instance is instance.parent)

        a = Recursive_property_reference.__get__(self, instance.parent, owner)
        instance.prop[self.name] = a

        return a

    def __set__(self, instance, value):
        instance.prop[self.name] = value

class File_reference(object):
    def __get__(self, instance, owner):
        if hasattr(instance, "_file"):
            return instance._file

        if instance.cls == "Program":
            file_name = instance.name
        else:
            file_name = instance.program.name

        instance._file = file_name
        return file_name


class Line_reference(object):

    def __get__(self, instance, owner):
        if hasattr(instance, "_line"):
            return instance._line

        if instance.cls == "Project":
            line = 0

        elif instance.cls == "Funcs":
            line = 1

        else:
            pline = instance.parent.line
            pcur = instance.parent.cur
            cur = instance.cur

            if pcur == cur:
                line = pline
            else:
                line = pline + instance.program.code.count("\n", pcur, cur)

        instance._line = line
        return line


class Group_reference(object):

    def __get__(self, instance, owner):

        if hasattr(instance, "_group"):
            return instance._group

        if instance.parent.cls in groups:
            group = instance.parent

        else:
            group = instance.parent.group
        
        instance._group = group
        return group


class Func_reference(object):

    def __get__(self, instance, owner):

        if hasattr(instance, "_func"):
            return instance._func

        if instance.cls in ("Func", "Main", "Program"):
            func = instance
        else:
            func = instance.parent.func

        instance._func = func
        return func

class Program_reference(object):
    def __get__(self, instance, owner):

        if hasattr(instance, "_program"):
            return instance._program

        if instance.cls == "Program":
            program = instance
        else:
            program = instance.parent.program

        instance._program = program
        return program

class Project_reference(object):
    def __get__(self, instance, owner):

        if hasattr(instance, "_project"):
            return instance._project

        if instance.cls == "Project":
            project = instance
        else:
            project = instance.parent.project

        instance._project = project
        return project


class Names(object):
    def __get__(self, instance, owner):
        return [i.prop["name"] for i in instance.children]


class Declare_reference(object):

    def __get__(self, instance, owner):

        if hasattr(instance, "_declare"):
            return instance._declare

        if instance.cls in nondeclares:
            return instance

        if instance.cls in structvars or\
                instance.backend in ("structs", "struct"):

            if instance.cls in ("Nget", "Nset"):
                if instance[0].cls == "String":
                    value = instance[0]["value"]
                else:
                    return instance

            else:
                value = instance.value

            if instance not in instance.program[3]:
                return instance

            struct = instance.program[3][instance]

            if value not in struct.names:
                return instance

            out = struct[struct.names.index(value)]
            instance._declare = out
            return out

        elif instance.parent.cls in "Struct":
            return instance

        else:

            if instance in instance.func[0]:
                out = instance.func[0][instance]
                instance._declare = out
                return out

            if instance in instance.func[2]:
                out = instance.func[2][instance]
                instance._declare = out
                return out


        return instance

