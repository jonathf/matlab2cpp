"""
The node contains the following attributes:

+----------------+-------+-----------------------------------------------------+
| Attribute name | type  | Description                                         |
+================+=======+=====================================================+
| backend        | str   | The currently set translation backend. Available in |
|                |       | the string format as `%(backend)s`.                 |
+----------------+-------+-----------------------------------------------------+
| children       | list  | A list of node children ordered from first to last  |
|                |       | child. Accessible using indexing                    |
|                |       | (`node[0]`, `node[1]`, ...). Alse available in the  |
|                |       | string format as `%(0)s`, `%(1)s`, ...              |
+----------------+-------+-----------------------------------------------------+
| cls            | str   | A string representation of the class name. Avalable |
|                |       | in the string format as `%(class)s`                 |
+----------------+-------+-----------------------------------------------------+
| code           | str   | The code that concived this node.                   |
+----------------+-------+-----------------------------------------------------+
| cur            | int   | The index to the position in the code where this    |
|                |       | node was concived. It takes the value 0 for nodes   |
|                |       | not created from code.                              |
+----------------+-------+-----------------------------------------------------+
| declare        | Node  | A reference to the node of same name where it is    |
|                |       | defined. This would be under `Declares`, `Params`   |
|                |       | or `Struct`. Useful for setting scope defined       |
|                |       | common datatypes. Returns itself if no declared     |
|                |       | variable has the same name as current node.         |
+----------------+-------+-----------------------------------------------------+
| dim            | int   | The number of dimensions in a numerical datatype.   |
|                |       | The values 0 through 4 represents scalar, column    |
|                |       | vector, row vector, matrix and cube respectively.   |
|                |       | The value is None if datatype is not numerical.     |
|                |       | Interconnected with `type`.                         |
+----------------+-------+-----------------------------------------------------+
| file           | str   | Name of the program. In projects, it should be the  |
|                |       | absolute path to the Matlab source file. Available  |
|                |       | in the string format as `%(file)s`                  |
+----------------+-------+-----------------------------------------------------+
| func           | Node  | A reference to Func (function) ancestor. Uses root  |
|                |       | if not found.                                       |
+----------------+-------+-----------------------------------------------------+
| group          | Node  | A reference to the first ancestor where the         |
|                |       | datatype does not automatically affect nodes        |
|                |       | upwards. A list of these nodes are listed in        |
|                |       | `mc.reference.groups`.                              |
+----------------+-------+-----------------------------------------------------+
| line           | int   | The codeline number in original code where this     |
|                |       | node was concived. It takes the value 0 for nodes   |
|                |       | not created from code.                              |
+----------------+-------+-----------------------------------------------------+
| name           | str   | The name of the node. Available in the string       |
|                |       | format as `%(name)s`.                               |
+----------------+-------+-----------------------------------------------------+
| names          | list  | A list of the names (if any) of the nodes children. |
+----------------+-------+-----------------------------------------------------+
| mem            | int   | The amount of type-space reserved per element in a  |
|                |       | numerical datatype.  The value 0 through 4          |
|                |       | represents unsigned int, int, float, double and     |
|                |       | complex.  The value is None if datatype is not      |
|                |       | numerical. Interconnected with `type`.              |
+----------------+-------+-----------------------------------------------------+
| num            | bool  | A bool value that is true if and only if the        |
|                |       | datatype is numerical.  Interconnected with `type`. |
+----------------+-------+-----------------------------------------------------+
| parent         | Node  | A reference to the direct node parent above the     |
|                |       | current one.                                        |
+----------------+-------+-----------------------------------------------------+
| pointer        | int   | A numerical value of the reference count. The value |
|                |       | 0 imply that the node refer to the actual variable, |
|                |       | 1 is a reference to the variable, 2 is a reference  |
|                |       | of references, and so on.                           |
+----------------+-------+-----------------------------------------------------+
| program        | Node  | A reference to program ancestor. Uses root if not   |
|                |       | found.                                              |
+----------------+-------+-----------------------------------------------------+
| project        | Node  | A reference to root node.                           |
+----------------+-------+-----------------------------------------------------+
| reference      | Node  | If node is a lambda function (backend               |
|                |       | `func_lambda`), the variable is declared locally,   |
|                |       | but it's content might be available in it's own     |
|                |       | function.  If so, the node will have a `reference`  |
|                |       | attribute to that function. Use `hasattr` to        |
|                |       | ensure it is the case.                              |
+----------------+-------+-----------------------------------------------------+
| ret            | tuple | The raw translation of the node. Same as            |
|                | str   | `node.str`, but on the exact form the tranlsation   |
|                |       | rule returned it.                                   |
+----------------+-------+-----------------------------------------------------+
| str            | str   | The translation of the node. Note that the code is  |
|                |       | translated leaf to root, and parents will not be    |
|                |       | translated before after current node is translated. |
|                |       | Current and all ancestors will have an empty        |
|                |       | string.                                             |
+----------------+-------+-----------------------------------------------------+
| suggest        | str   | A short string representation of the suggested      |
|                |       | datatype. It is used for suggesting datatype in     |
|                |       | general, and can only be assigned, not read.        |
|                |       | Typically only the declared variables will be read, |
|                |       | so adding a suggestion is typically done            |
|                |       | `node.declare.type = "..."`.                        |
+----------------+-------+-----------------------------------------------------+
| type           | str   | A short string representation of the nodes          |
|                |       | datatype. Interconnected with `dim`, `mem` and      |
|                |       | `num`.  Available in string format as `%(type)s`    |
+----------------+-------+-----------------------------------------------------+
| value          | str   | A free variable resereved for content. The use      |
|                |       | varies from node to node.  Available in the string  |
|                |       | format as `%(value)s`.                              |
+----------------+-------+-----------------------------------------------------+
    """
import reference as ref
import backend

import matlab2cpp.datatype as dt
import matlab2cpp.supplement as sup
import matlab2cpp as mc

class Node(object):
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
            if prop[key] is None and hasattr(self, key):
                prop[key] = getattr(self, key)

        I = len(self.children)
        for i in xrange(I):
            prop[str(i)] = prop["-"+str(I-i)] = self[i].prop["str"]
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

    def __getitem__(self, index):
        """
Retrieve node child.

Args:
    index (int): Get node child by positional order
    index (str): Get first instance with `node.name==index`
    index (Node): Get first instance with `node.name==index.name`
    index (slice): Get sublist of `node.children`

Examples:

    >>> node = mc.Var(None, "a")
    >>> node["b"]
    Traceback (most recent call last):
        ...
    IndexError: node child "b" not found
    >>> node[0]
    Traceback (most recent call last):
        ...
    IndexError: index of Var out of range (0)
    >>> node[()]
    Traceback (most recent call last):
        ...
    TypeError: index of Var must be in (int, str, slice, Node), not tuple
        """
        i = index # shorter
        if isinstance(i, Node):
            i = i.name

        if isinstance(i, str):
            if i not in self.names:
                raise IndexError("node child \"%s\" not found" % i)
            i = self.names.index(i)

        if isinstance(i, int):

            if len(self) <= i:
                raise IndexError(
                        "index of %s out of range (%d)" % (self.cls, i))
            return self.children[i]

        if isinstance(i, slice):
            return self.children[i]

        raise TypeError(
                "index of %s must be in (int, str, slice, Node), not %s" \
                % (self.cls, i.__class__.__name__))


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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
