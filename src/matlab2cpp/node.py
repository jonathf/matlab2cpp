import datatype as dt
import snippets
import reference as ref
import collection


class Node(object):
    """
General definition of a token representation of code
    """

    dim = dt.Dim()
    mem = dt.Mem()
    num = dt.Num()
    type = dt.Type()
    suggest = dt.Suggest()

    func = ref.Func_reference()
    program = ref.Program_reference()
    line = ref.Line_reference()
    group = ref.Group_reference()
    declare = ref.Declare_reference()

    names = ref.Names()

    backend = ref.Property_reference("backend")
    str = ref.Property_reference("str")
    ret = ref.Property_reference("ret")
    value = ref.Property_reference("value")
    pointer = ref.Property_reference("pointer")
    cls = ref.Property_reference("class")
    name = ref.Property_reference("name")

    line = ref.Recursive_property_reference("line")
    cur = ref.Recursive_property_reference("cur")
    code = ref.Recursive_property_reference("code")

    def __init__(self, parent, name="", backend="unknown", value="",
            type="TYPE", pointer=0, line=None, cur=None, code=None):
        """
Parameters
----------
parent : Node
    Node parent in the token tree
name : str
    Optional name of the node
        """
        self.children = []
        self.prop = {"type":type, "suggest":type,
                "value":value, "str":"", "name":name,
                "pointer":pointer, "backend":backend,
                "line":line, "cur":cur, "code":code,
                "ret":"",
                "class":self.__class__.__name__}

        # Parental relationship
        self.parent = parent

        if not (self is parent):
            parent.children.append(self)


    def summary(self):
        "Node summary"
        return utils.node_summary(self, None)


    def translate_tree(self, opt=None):
        """Generate code"""

        return utils.translate(self, opt)

    def properties(self):

        prop = self.prop.copy()
        I = len(self)
        for i in xrange(I):
            prop[str(i)] = prop["-"+str(I-i)] = self[i]["str"]
        return prop

    def translate_node(self, opt=None):
        utils.node_translate(self, opt)


    def auxiliary(self, type=None, convert=False):
        """Create a auxiliary variablele and
move actual calcuations to own line.

Parameters
----------
type : str, None
    If provided, auxiliary variable type will be converted
        """
        utils.create_auxillary(self, type, convert)


    def resize(self):
        utils.create_resize(self)


    def include(self, name, **kws):

        key, include_code, library_code = snippets.retrieve(self, name, **kws)

        includes = self.program[0]
        if key not in includes.names:
            collection.Include(includes, key, include_code)

        library = self.program.parent[0]
        if key not in library:
            collection.Snippet(library, key, library_code)

    def warning(self, msg):
        utils.create_error(self, msg, True)

    def error(self, msg):
        utils.create_error(self, msg, False)

    def create_declare(self):
        utils.create_declare(self)

    def __getitem__(self, i):
        if isinstance(i, str):
            out = self.prop[i]
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


import utils
