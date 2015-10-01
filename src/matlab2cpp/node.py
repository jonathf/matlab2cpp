import matlab2cpp.datatype as dt
import matlab2cpp.inlines as inl
import matlab2cpp.reference as ref


class Node(object):
    """
General definition of a token representation of code component.

During translation an instance of the current state in form of a Node will be
provided. It has a set of properties and module functions that can be used to
retrieve and manipulate the state of the nodes.

To illustrate both nodes and relationship we introduce the following example:

    >>> builder = mc.Treebuilder()
    >>> program = builder.load("unnamed", "function y=f(x); y=x+4")
    >>> mc.set_variables(program, {"f" : {"x": "int", "y": "double"}})
    >>> builder.configure()
    >>> program.translate_tree()
    >>> print mc.qtree(program)
            Program    program      TYPE    unnamed           
            Includes   program      TYPE                      
            | Include    program      TYPE    #include <armadillo>
            | Include    program      TYPE    using namespace arma ;
      1   1 Funcs      program      TYPE    unnamed           
      1   1 | Func       func_return  double  f                 
      1   1 | | Declares   func_return  double                    
      1   1 | | | Var        double       double  y                 
      1   1 | | Returns    func_return  double                    
      1  10 | | | Var        double       double  y                 
      1  13 | | Params     func_return  int                       
      1  14 | | | Var        int          int     x                 
      1  16 | | Block      code_block   TYPE                      
      1  18 | | | Assign     unknown      TYPE                      
      1  18 | | | | Var        double       double  y                 
      1  20 | | | | Plus       expression   int                       
      1  20 | | | | | Var        int          int     x                 
      1  22 | | | | | Int        int          int                       
            Inlines    program      TYPE    unnamed           
            Structs    program      TYPE    unnamed           
            Headers    program      TYPE    unnamed           
            | Header     program      TYPE    f                 
            Log        program      TYPE    unnamed           
    
Navigating the tree
~~~~~~~~~~~~~~~~~~~
The program is the root of the tree. To move down from there can be done using
indexing. All nodes are interable, allowing standard Python movement:

    >>> funcs = program[1]
    >>> func = funcs[0]
    >>> assign = func[3][0]
    >>> var_y, plus = assign
    >>> var_x, int_4 = plus

Moving upwards in the tree is done using the `parent` reference:

    >>> block = assign.parent
    >>> print assign is var_y.parent
    True

The `parent` reference is not the only reference available. These include:

children : list
    A list of node children ordered from first to last child. Accessible using
    indexing (`node[0]`, `node[1]`, ...). Alse available in the string format as
    `%(0)s`, `%(1)s`, ...

declare : Node
    A reference to the node of same name where it is defined. This would be
    under `Declares`, `Params` or `Struct`. Useful for setting scope defined
    common datatypes. Returns itself if no declared variable has the same name
    as current node.

func : Node
    A reference to Func (function) ancestor. Uses root if not found.

group : Node
    A reference to the first ancestor where the datatype does not automatically
    affect nodes upwards. A list of these nodes are listed in
    `mc.reference.groups`.

parent : Node
    A reference to the direct node parent above the current one.

program : Node
    A reference to program ancestor. Uses root if not found.

project : Node
    A reference to root node.

reference : Node
    If node is a lambda function (backend `func_lambda`), the variable is
    declared locally, but it's content might be available in it's own function.
    If so, the node will have a `reference` attribute to that function. Use
    `hasattr` to ensure it is the case.


Interactive node attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following node attributes are interactive in the sense that they can both
be observed and changed. Many of them are also interconnected such that change
will automatically affect others. For example:

    >>> print var_y.type
    double
    >>> print var_y.dim
    0
    >>> var_y.dim = 1
    >>> print var_y.type
    vec


dim : int
    The number of dimensions in a numerical datatype. The values 0 through
    4 represents scalar, column vector, row vector, matrix and cube
    respectively. The value is None if datatype is not numerical. Interconnected
    with `type`.

mem : int
    The amount of type-space reserved per element in a numerical datatype.  The
    value 0 through 4 represents unsigned int, int, float, double and complex.
    The value is None if datatype is not numerical. Interconnected with `type`.

num : bool
    A bool value that is true if and only if the datatype is numerical.
    Interconnected with `type`.

pointer : int
    A numerical value of the reference count. The value 0 imply that the node
    refer to the actual variable, 1 is a reference to the variable, 2 is
    a reference of references, and so on.

suggest : str
    A short string representation of the suggested datatype. It is used for
    suggesting datatype in general, and can only be assigned, not read.
    Typically only the declared variables will be read, so adding a suggestion
    is typically done `node.declare.type = "..."`.

type : str
    A short string representation of the nodes datatype. Interconnected with
    `dim`, `mem` and `num`. Available in string format as `%(type)s`

Static node attributes
~~~~~~~~~~~~~~~~~~~~~~

The following attributes are automatically generated by the software and are
provided for convenience.

backend : str
    The currently set translation backend. Available in the string format as
    `%(backend)s`.

cls : str
    A string representation of the class name.  Avalable in the string format as
    `%(class)s`

code : str
    The code that concived this node.

cur : int
    The index to the position in the code where this node was concived. It takes
    the value 0 for nodes not created from code.

file : str
    Name of the program. In projects, it should be the absolute path to the
    Matlab source file. Available in the string format as `%(file)s`

line : int
    The codeline number in original code where this node was concived. It takes
    the value 0 for nodes not created from code.

name : str
    The name of the node. Available in the string format as `%(name)s`.

names : list
    A list of the names (if any) of the nodes children.

ret : str, tuple
    The raw translation of the node. Same as `node.str`, but on the exact form
    the tranlsation rule returned it.

str : str
    The translation of the node. Note that the code is translated leaf to root,
    and parents will not be translated before after current node is
    translated. Current and all ancestors will have an empty string.

value : str
    A free variable resereved for content. The use varies from node to node.
    Available in the string format as `%(value)s`.
    

Context manipulation
~~~~~~~~~~~~~~~~~~~~

auxillary : Push subtree up to its own code line and save it to an
                    auxillary variable.
resize              Resize handler. Used to bring a cube structure down to
                    a matrix and vector properly.
include             
warning
error
suggest_datatype

Tree processing
~~~~~~~~~~~~~~~

translate_node
translate_tree
summary

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

    def __init__(self, parent, name="", backend="unknown", value="",
            type="TYPE", pointer=0, line=None, cur=None, code=None, file=None):
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
                "ret":"", "file":file,
                "class":self.__class__.__name__}

        # Parental relationship
        self.parent = parent

        if not (self is parent):
            parent.children.append(self)


    def summary(self):
        """
Generate a summary of the tree structure with some meta-information.

    Returns:
	str: Summary on format
        """
        return utils.node_summary(self, None)


    def translate_tree(self, opt=None):
        """Generate code"""

        utils.translate(self, opt)

    def properties(self):

        prop = self.prop.copy()
        for key in self.prop:
            if prop[key] is None:
                prop[key] = self[key]

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

        include_code, library_code = inl.retrieve(self, name, **kws)

        includes = self.program[0]
        if include_code and include_code not in includes.names:
            collection.Include(includes, include_code, value=includes.value)

        inlines = self.program[2]
        if library_code and library_code not in inlines:
            collection.Inline(inlines, library_code)

    def warning(self, msg):
        utils.create_error(self, msg, True)

    def error(self, msg):
        utils.create_error(self, msg, False)

    def create_declare(self):
        utils.create_declare(self)

    def suggest_datatype(self):
        return utils.suggest_datatype(self)

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


import matlab2cpp.utils
import matlab2cpp.collection

if __name__ == "__main__":
    import doctest
    import __init__ as mc
    doctest.testmod()
