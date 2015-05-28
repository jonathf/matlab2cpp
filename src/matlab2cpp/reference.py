

groups = [
    "Assign", "Assigns", "Branch", "For", "Func",
    "Set", "Cset", "Fset", "Nset", "Sset",
    "Get", "Cget", "Fget", "Nget", "Sget",
    "Statement", "Switch", "Tryblock",
    "While", "Program", "Block", "Node",
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

        instances = [instance]
        while True:
            instance = instance.parent
            a = instance.prop.get(self.name, None)
            instances.append(instance)
            if a is None:
                assert instance["class"] not in ("Project", "Node")
            else:
                break

        for instance in instances[:-1]:
            instance.prop[self.name] = a

        return a

    def __set__(self, instance, value):
        instance.prop[self.name] = value

class Line_reference(object):

    def __get__(self, instance, owner):

        if hasattr(instance, "_line"):
            return instance._line

        node = instance
        while node.parent.cls != "Block" and\
                not (node.parent is node):
            node = node.parent
        
        instance._line = node
        return node


class Group_reference(object):

    def __get__(self, instance, owner):

        if hasattr(instance, "_group"):
            return instance._group

        node = instance
        while node.parent.cls not in groups and\
                not (node.parent is node):
            node = node.parent
        
        instance._group = node
        return node


class Func_reference(object):

    def __get__(self, instance, owner):

        if hasattr(instance, "_func"):
            return instance._func

        node = instance
        while node.cls != "Func" and\
                not (node.parent is node) and\
                not hasattr(node, "_func"):
            node = node.parent

        if node.cls == "Func" or node.parent is node:
            instance._func = node
        else:
            instance._func = node._func

        return instance._func

class Program_reference(object):
    def __get__(self, instance, owner):

        if hasattr(instance, "_program"):
            return instance._program

        node = instance
        while node.cls != "Program" and\
                not hasattr(node, "_program"):
            node = node.parent

        if node.cls == "Program":
            instance._program = node
        else:
            instance._program = node._program

        assert instance._program.cls == "Program"

        return instance._program


class Names(object):
    def __get__(self, instance, owner):
        return [i.prop["name"] for i in instance.children]


class Declare_reference(object):

    def __get__(self, instance, owner):
        if instance.cls in nondeclares:
            return instance

        if instance.cls in structvars:
            if instance.cls in ("Nget", "Nset"):
                if instance[0].cls == "String":
                    value = instance[0]["value"]
                else:
                    return instance

            else:
                value = instance.value

            if instance not in instance.program[1]:
                return instance

            struct = instance.program[1][instance]

            if value not in struct.names:
                return instance

            return struct[struct.names.index(value)]

        elif instance.parent.cls == "Struct":

            return instance

        else:

            if instance in instance.func[0]:
                return instance.func[0][instance]

            if instance in instance.func[2]:
                return instance.func[2][instance]


        return instance

