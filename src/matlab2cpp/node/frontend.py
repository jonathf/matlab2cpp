from . import (
    reference as ref,
    backend,
)

import matlab2cpp.datatype as dt
import matlab2cpp.supplement as sup
import matlab2cpp as mc

class Node(object):
    """
A representation of a node in a node tree.

Attributes:
    backend (str): The currently set translation backend. Available in  the
        string format as `%(backend)s`.
    children (list): A list of node children ordered from first to last  child.
        Accessible using indexing  (`node[0]`, `node[1]`, ...). Alse available
        in the  string format as `%(0)s`, `%(1)s`, ...
    cls (str): A string representation of the class name. Avalable  in the
        string format as `%(class)s`
    code (str): The code that concived this node.
    cur (int): The index to the position in the code where this  node was
        concived. It takes the value 0 for nodes  not created from code.
    declare (Node): A reference to the node of same name where it is  defined.
        This would be under `Declares`, `Params`  or `Struct`. Useful for
        setting scope defined  common datatypes. Returns itself if no declared
        variable has the same name as current node.
    dim (int): The number of dimensions in a numerical datatype.  The values
        0 through 4 represents scalar, column  vector, row vector, matrix and
        cube respectively.  The value is None if datatype is not numerical.
        Interconnected with `type`.
    file (str): Name of the program. In projects, it should be the  absolute
        path to the Matlab source file. Available  in the string format as
        `%(file)s`.
    ftypes (dict): Input/output function scoped datatypes.
    func (Node): A reference to Func (function) ancestor. Uses root  if not
        found.
    group (Node): A reference to the first ancestor where the  datatype does
        not automatically affect nodes  upwards. A list of these nodes are
        listed in  `mc.reference.groups`.
    itype (list): Input/output include scope statements
    line (int): The codeline number in original code where this  node was
        concived. It takes the value 0 for nodes  not created from code.
    mem (int): The amount of type-space reserved per element in a  numerical
        datatype.  The value 0 through 4  represents unsigned int, int, float,
        double and  complex.  The value is None if datatype is not  numerical.
        Interconnected with `type`.
    name (str): The name of the node. Available in the string  format as
        `%(name)s`.
    names (list): A list of the names (if any) of the nodes children.
    num (bool): A bool value that is true if and only if the  datatype is
        numerical.  Interconnected with `type`.
    parent (Node): A reference to the direct node parent above the  current
        one.
    pointer (int): A numerical value of the reference count. The value  0 imply
        that the node refer to the actual variable,  1 is a reference to the
        variable, 2 is a reference  of references, and so on.
    program (Node): A reference to program ancestor. Uses root if not  found.
    project (Node): A reference to root node.
    reference (Node): If node is a lambda function (backend  `func_lambda`),
        the variable is declared locally,  but it's content might be available
        in it's own  function.  If so, the node will have a `reference`
        attribute to that function. Use `hasattr` to  ensure it is the case.
    ret (tuple): The raw translation of the node. Same     as (str):
        `node.str`, but on the exact form the tranlsation  rule returned it.
    str (str): The translation of the node. Note that the code is  translated
        leaf to root, and parents will not be  translated before after current
        node is translated.  Current and all ancestors will have an empty
        string.
    stypes (dict): Input/Output struct scoped datatypes.
    suggest (str): A short string representation of the suggested  datatype. It
        is used for suggesting datatype in  general, and can only be assigned,
        not read.  Typically only the declared variables will be read,  so
        adding a suggestion is typically done  `node.declare.type = "..."`.
    type (str): A short string representation of the nodes  datatype.
        Interconnected with `dim`, `mem` and  `num`.  Available in string
        format as `%(type)s`
    value (str): A free variable resereved for content. The use  varies from
        node to node.  Available in the string  format as `%(value)s`.
    vtypes (dict): Verbatim translation in tree (read-only)
    """
    backend = ref.Property_reference("backend")

    cls = ref.Property_reference("class")
    code = ref.Recursive_property_reference("code")
    cur = ref.Recursive_property_reference("cur")

    dim = dt.Dim()
    #file = ref.Recursive_property_reference("file")
    file = ref.File_reference()
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

    def __init__(self, parent=None, name="", value="", pointer=0,
            line=None, cur=None, code=None):
        """
Keyword Args:
    code (str): source code
    cur (int): cursor position (inherited)
    line (int): Line number (inherited)
    name (str): Optional name of the node
    parent (Node): Node parent in the Node tree
    pointer (int): is reference to object (not currently used)
    str (str): Translation content
    value (str): Default node content placeholder
        """
        self.children = []
        self.prop = {"type":"TYPE", "suggest":"TYPE",
                "value":value, "str":"", "name":name,
                "pointer":pointer, "backend":"unknown",
                "line":line, "cur":cur, "code":code,
                "ret":"",
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
        """Generate code translation

Args:
    opt (argparse.Namespace, optional): Extra arguments provided by argparse
    only (bool): If true, translate current node only.
        """

        # configure if not configured
        if not self.project.builder.configured:
            self.project.builder.configure()

        if only:
            backend.translate_one(self, opt)
        else:
            backend.translate(self, opt)


    def properties(self):
        """
Retrieve local node properties.

The following properties are included:
+-------------+-------------------------------------+-----------------------------+
| Name        | Attribute                           | Description                 |
+=============+=====================================+=============================+
| ``backend`` | :py:attr:`~matlab2cpp.Node.backend` | Name of translation backend |
+-------------+-------------------------------------+-----------------------------+
| ``class``   | :py:attr:`~matlab2cpp.Node.cls`     | Node class name             |
+-------------+-------------------------------------+-----------------------------+
| ``code``    | :py:attr:`~matlab2cpp.Node.code`    | Matlab code equivalent      |
+-------------+-------------------------------------+-----------------------------+
| ``cur``     | :py:attr:`~matlab2cpp.Node.cur`     | Position in Matlab code     |
+-------------+-------------------------------------+-----------------------------+
| ``line``    | :py:attr:`~matlab2cpp.Node.line`    | Line number in Matlab code  |
+-------------+-------------------------------------+-----------------------------+
| ``name``    | :py:attr:`~matlab2cpp.Node.name`    | Node name                   |
+-------------+-------------------------------------+-----------------------------+
| ``pointer`` | :py:attr:`~matlab2cpp.Node.pointer` | Pointer reference object    |
+-------------+-------------------------------------+-----------------------------+
| ``str``     | :py:attr:`~matlab2cpp.Node.str`     | Node translation            |
+-------------+-------------------------------------+-----------------------------+
| ``suggest`` | :py:attr:`~matlab2cpp.Node.suggest` | Suggested datatype          |
+-------------+-------------------------------------+-----------------------------+
| ``type``    | :py:attr:`~matlab2cpp.Node.type`    | Node datatype               |
+-------------+-------------------------------------+-----------------------------+
| ``value``   | :py:attr:`~matlab2cpp.Node.value`   | Node value                  |
+-------------+-------------------------------------+-----------------------------+

In addition will number keys (in string format) represents the node
children's ``node.str`` in order.

Returns:
    dict: dictionary with all properties and references to other assosiated
    nodes.

Example:
    >>> var = mc.collection.Var(None, name="A", value="B", line=1, cur=0, code="C")
    >>> print(var.properties()) # doctest: +NORMALIZE_WHITESPACE
    {'code': 'C', 'cur': 0, 'suggest': 'TYPE', 'value': 'B', 'ret': '', 'str':
    '', 'type': 'TYPE', 'line': 1, 'backend': 'unknown', 'pointer': 0, 'class':
    'Var', 'name': 'A'}
        """

        prop = self.prop.copy()
        for key in self.prop:
            if prop[key] is None and hasattr(self, key):
                prop[key] = getattr(self, key)

        I = len(self.children)
        for i in xrange(I):
            prop[str(i)] = prop["-"+str(I-i)] = self[i].prop["str"]
        return prop



    def auxiliary(self, type=None, convert=False):
        """
Create a auxiliary variable and rearange nodes to but current node on its own
line before.

Args:
    type (str, None):
        If provided, auxiliary variable type will be converted
    convert (bool):
        If true, add an extra function call ``conv_to`` to convert datatype in
        Armadillo.

Example:
    Many statements that works inline in Matlab, must be done on multiple lines in
    C++. Take for example the statement ``[1,2]+3``. In C++, the rowvec ``[1,2]``
    must first be initialized and converted into ``rowvec`` before arithmetics can
    be used::

    >>> print(mc.qscript("[1,2]+3"))
    sword __aux_irowvec_1 [] = {1, 2} ;
    _aux_irowvec_1 = irowvec(__aux_irowvec_1, 2, false) ;
    _aux_irowvec_1+3 ;

    The difference in tree structure is as follows:

    >>> print(mc.qtree("[1,2]", core=True)) # doctest: +NORMALIZE_WHITESPACE
     1  1Block      code_block   TYPE
     1  1| Statement  code_block   TYPE
     1  1| | Matrix     matrix       irowvec
     1  2| | | Vector     matrix       irowvec
     1  2| | | | Int        int          int
     1  4| | | | Int        int          int
    >>> print(mc.qtree("[1,2]+3", core=True)) # doctest: +NORMALIZE_WHITESPACE
     1  1Block      code_block   TYPE
     1  1| Assign     matrix       int
     1  1| | Var        irowvec      irowvec _aux_irowvec_1
     1  1| | Matrix     matrix       irowvec
     1  2| | | Vector     matrix       irowvec
     1  2| | | | Int        int          int
     1  4| | | | Int        int          int
     1  1| Statement  code_block   TYPE
     1  1| | Plus       expression   irowvec
     1  1| | | Var        unknown      irowvec _aux_irowvec_1
     1  7| | | Int        int          int
        """
        return backend.auxillary(self, type, convert)


    def resize(self):
        """
Resize function.

Very similar to the function :py:func:`~matlab2cpp.Node.auxiliary`, but
specific for reshaping cubes into slices.

Might need to be rewritten.
        """
        backend.resize(self)

    def include(self, name, **kws):
        """
Include library in the header of the file.

These include::

+--------------+--------------------------+
| Name         | Description              |
+==============+==========================+
| ``SPlot``    | Local SPlot library      |
+--------------+--------------------------+
| ``m2cpp``    | Local M2cpp library      |
+--------------+--------------------------+
| ``arma``     | Global Armadillo library |
+--------------+--------------------------+
| ``iostream`` | Global iostream library  |
+--------------+--------------------------+

Args:
    name (str): Name of header to include
    **kws (str, optional): Optional args for header. Mostly not in use.
    """
        backend.include(self, name, **kws)

    def warning(self, msg):
        """
Add a warning to the log file.

Args:
    msg (str): Content of the warning

See also:
    :py:func:`~matlab2cpp.Node.error`
    """
        backend.error(self, msg, True)

    def error(self, msg):
        """
Add an error to the log file.

Args:
    msg (str): Content of the error

Example:
    >>> print(mc.qlog("  a"))
    Error in class Var on line 1:
      a
      ^
    unknown data type
    """
        backend.error(self, msg, False)

    def create_declare(self):
        """
Investigate if the current node is declared (either in Params, Declares or in
Structs), and create such a node if non exists in Declares.

The declared variable's datatype will be the same as current node.

Returns:
    Node : the (newly) declared node
        """
        backend.create_declare(self)

    def suggest_datatype(self):
        """
Try to figure out from context, what the datatype should be for current node.

Returns:
    (tuple): Suggestion on the form ``(dim, mem)``
        """
        return backend.suggest_datatype(self)

    def wall_clock(self):
        """
Prepare for the use of ``tic`` and ``toc`` functionality in code.

Does nothing if called before.
        """
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
        """
Test if (Node with) name ``i`` is contained in code.
        """

        if isinstance(i, str):
            return i in self.names
        return i.name in self.names

    def __setitem__(self, key, val):
        self.prop[key] = val

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

| Structure:
|   A
|   | B
|   | | D
|   | | E
|   | C
|   | | F
|   | | G
|
| Sorted [o]rdered, [r]everse and [i]nverse:
|
| ori
| ___ : A B D E C F G
| o__ : A B C D E F G
| _r_ : A C G F B E D
| __i : D E B F G C A
| or_ : A C B G F E D
| o_i : D E F G B C A
| _ri : E D B G F C A
| ori : G F E D C B A

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
        """
Prepare the code for plotting functionality.
        """
        return backend.plotting(self)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
