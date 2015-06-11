import datatype as dt
import snippets
import reference as ref
import collection


class Node(object):
    """
General definition of a token representation of code
    """

    dim = dt.Dim()
    """The number of dimensions in a numerical datatype. The values 0
through 4 represents scalar, column vector, row vector, matrix and cube
respectively. The value is None if datatype is not numerical."""

    mem = dt.Mem()
    """The amount of type-space reserved per element in a numerical datatype.
The value 0 through 4 represents unsigned int, int, float, double and complex.
The value is None if datatype is not numerical."""

    num = dt.Num()
    """A bool value that is true if and only if the datatype is numerical."""

    type = dt.Type()
    """A short string representation of the nodes datatype."""

    suggest = dt.Suggest()
    """A short string representation of the suggested datatype. It is used
for suggesting datatype in general, and can only be assigned, not read."""

    pointer = ref.Property_reference("pointer")
    """A numerical value of the reference count. The value 0 imply that the
node refer to the actual variable, 1 is a reference to the variable, 2 is a
reference of references, and so on."""

    func = ref.Func_reference()
    "A reference to Func (function) ancestor."

    program = ref.Program_reference()
    "A reference to program ancestor."

    line = ref.Line_reference()
    "A refrence to the first child of a Block."

    group = ref.Group_reference()
    """A reference to the first ancestor where the datatype does not
autmatically affect nodes upwards. A list of these nodes are listed in
mc.reference.groups`."""

    declare = ref.Declare_reference()
    """A reference to the node of same name where it is defined.
This would be under `Declares`, `Params` or `Struct`.
Useful for setting scope defined common datatypes"""

    names = ref.Names()
    """A list of the names of the nodes children."""

    backend = ref.Property_reference("backend")
    """The currently set translation backend."""
        
    str = ref.Property_reference("str")
    """The translation of the node. Note that the code is translated leaf to
root, and parents will not be translated before after current node is
translated."""

    ret = ref.Property_reference("ret")
    """The raw translation of the node. Same as `node.str`, but on the exact
form the tranlsation rule returned it."""

    value = ref.Property_reference("value")
    """A free variable resereved for content. The use varies from node to node."""

    cls = ref.Property_reference("class")
    """A string representation of the class name. Note that the word `class`
is reserved in Python, so the name `cls` is used instead."""

    name = ref.Property_reference("name")
    """The name of the node."""

    line = ref.Recursive_property_reference("line")
    """The codeline number in original code where this node was concived."""

    cur = ref.Recursive_property_reference("cur")
    """The index to the position in the code where this node was concived."""

    code = ref.Recursive_property_reference("code")
    """The code that concived this node."""

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
