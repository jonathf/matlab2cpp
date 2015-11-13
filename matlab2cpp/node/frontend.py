import reference as ref
import backend

import matlab2cpp.datatype as dt
import matlab2cpp.supplement as sup
import matlab2cpp

class Node(object):
    """
    """

    backend = ref.Property_reference("backend")
    cls = ref.Property_reference("class")
    code = ref.Recursive_property_reference("code")
    cur = ref.Recursive_property_reference("cur")
    dim = dt.Dim()
    file = ref.Recursive_property_reference("file")
    line = ref.Line_reference()
    mem = dt.Mem()
    name = ref.Property_reference("name")
    names = ref.Names()
    num = dt.Num()
    pointer = ref.Property_reference("pointer")
    ret = ref.Property_reference("ret")
    str = ref.Property_reference("str")
    suggest = dt.Suggest()
    type = dt.Type()
    value = ref.Property_reference("value")

    func = ref.Func_reference()
    program = ref.Program_reference()
    project = ref.Project_reference()
    group = ref.Group_reference()
    declare = ref.Declare_reference()

    ftypes = sup.Ftypes()
    itypes = sup.Itypes()
    stypes = sup.Stypes()
    vtypes = sup.Vtypes()

    def __init__(self, parent, name="", backend="unknown", value="",
            type="TYPE", pointer=0, line=None, cur=None, code=None, file=None):
        """
Parameters
----------
parent : Node
    Node parent in the Node tree
name : str
    Optional name of the node
        """
        self.children = []
        self.prop = {"type":type, "suggest":type,
                "value":value, "str":"", "name":name,
                "pointer":pointer, "backend":backend,
                "line":line, "cur":cur, "code":code,
                "ret":"", "file":file,
                "class":self.__class__.__name__}

        # Parental relationship
        self.parent = parent

        if self is self.parent or (not hasattr(parent, "children")):
            pass
        else:
            parent.children.append(self)


    def summary(self, args=None):
        """
Generate a summary of the tree structure with some meta-information.

Returns:
	str: Summary of the node tree

See also:
    `mc.qtree`
        """
        return backend.summary(self, args)


    def configure(self, suggest=False):
        matlab2cpp.configure.configure(self, suggest)

    def translate(self, opt=None, only=False):
        """Generate code"""
        if not self.project.builder.configured:
            self.project.builder.configure()

        if only:
            backend.translate_one(self, opt)
        else:
            backend.translate(self, opt)


    def properties(self):

        prop = self.prop.copy()
        for key in self.prop:
            if prop[key] is None:
                prop[key] = self[key]

        I = len(self)
        for i in xrange(I):
            prop[str(i)] = prop["-"+str(I-i)] = self[i]["str"]
        return prop



    def auxiliary(self, type=None, convert=False):
        """Create a auxiliary variablele and
move actual calcuations to own line.

Parameters
----------
type : str, None
    If provided, auxiliary variable type will be converted
        """
        return backend.auxillary(self, type, convert)


    def resize(self):
        backend.resize(self)


    def include(self, name, **kws):
        backend.include(self, name, **kws)

    def warning(self, msg):
        backend.error(self, msg, True)

    def error(self, msg):
        backend.error(self, msg, False)

    def create_declare(self):
        backend.create_declare(self)

    def suggest_datatype(self):
        return backend.suggest_datatype(self)

    def wall_clock(self):
        return backend.wall_clock(self)

    def __getitem__(self, i):
        if isinstance(i, str):
            out = self.prop[i]
            if out is None:
                if i == "cls":
                    return self.cls
                elif hasattr(self, i):
                    return getattr(self, i)
            return out

        if isinstance(i, Node):
            i = self.names.index(i.name)

        return self.children[i]

    def __contains__(self, i):
        if isinstance(i, str):
            return i in self.names
        return i.name in self.names

    def __setitem__(self, key, val):
        self.prop[key] = val

    def __hasitem__(self, key):
        return key in self.prop

    def __len__(self):
        return len(self.children)

    def __str__(self):
        return self.prop["str"]

    def __add__(self, val):
        return str(self)+str(val)

    def __radd__(self, val):
        return str(val)+str(val)

    def __iter__(self):
        return self.children.__iter__()

    def append(self, node):
        node.children.append(node)

    def pop(self, index):
        return self.children.pop(index)

    def flatten(self, ordered=False, reverse=False, inverse=False):
        r"""
Return a list of all nodes

Tree:
  A
  |\
  B C
 /| |\
D E F G

Sorted [o]rdered, [r]everse and [i]nverse:

ori :
    : A B D E C F G
o   : A B C D E F G
 r  : A C G F B E D
  i : D E B F G C A
or  : A C B G F E D
o i : D E F G B C A
 ri : E D B G F C A
ori : G F E D C B A

Args:

    node (Node): Root node to start from
    ordered (bool): If True, make sure the nodes are hierarcically ordered.
    reverse (bool): If True, children are itterated in reverse order.
    inverse (bool): If True, tree is itterated in reverse order.

Return:
    list: All nodes in a flatten list.
        """
        return backend.flatten(self, ordered, reverse, inverse)

    def plotting(self):
        return backend.plotting(self)

