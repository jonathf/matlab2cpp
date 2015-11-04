"""
Iterating through Matlab code always starts with constructing a builder::

    >>> builder = mc.Builder()

This is an empty shell without any content. To give it content, we supply it
with code::

    >>> builder.load("file1.m", "a = 4")

The function saves the code locally as `builder.code` and initiate the
`create_program` method with index 0. The various `create_*` are then called and
used to populate the node tree. The code is considered static, instead the
index, which refer to the position in the code is increased to move forward in
the code. The various constructors uses the support modules in the
:py:mod:`~matlab2cpp.mc.tree` to build a full toke tree.  The result is as
follows::

    >>> print builder # doctest: +NORMALIZE_WHITESPACE
       | Project    program      TYPE    project
       | | Program    program      TYPE    file1.m
       | | | Includes   program      TYPE
    1 1| | | Funcs      program      TYPE    file1.m
    1 1| | | | Main       func_common  TYPE    main
    1 1| | | | | Declares   func_return  TYPE
    1 1| | | | | | Var        unknown      TYPE    a
    1 1| | | | | Returns    func_return  TYPE
    1 1| | | | | Params     func_return  TYPE
    1 1| | | | | Block      code_block   TYPE
    1 1| | | | | | Assign     unknown      TYPE
    1 1| | | | | | | Var        unknown      TYPE    a
    1 5| | | | | | | Int        int          int
       | | | Inlines    program      TYPE    file1.m
       | | | Structs    program      TYPE    file1.m
       | | | Headers    program      TYPE    file1.m
       | | | Log        program      TYPE    file1.m

If is possible to get a detailed output of how this process is done, by turning
the `disp` flag on::

    >>> builder = mc.Builder(disp=True)
    >>> builder.load("file1.m", "a = 4")
    loading file1.m
         Program     functions.program
       0 Main        functions.main
       0 Codeblock   codeblock.codeblock 
       0   Assign      assign.single        'a = 4'
       0     Var         variables.assign     'a'
       4     Expression  expression.create    '4'
       4     Int         misc.number          '4'

This printout lists the core Matlab translation. In the four columns the first
is the index to the position in the Matlab code, the second is the node created,
the third is the file and function where the node was created, and lastly the
fourth column is a code snippet from the Matlab code. This allows for quick
diagnostics about where an error in interpretation might have occurred.

Note that the tree above for the most part doesn't have any relevant data types
configure. To configure datatypes, use the `configure` method::

    >>> builder.configure(suggest=True)
    >>> print builder # doctest: +NORMALIZE_WHITESPACE
       | Project    program      TYPE    project
       | | Program    program      TYPE    file1.m
       | | | Includes   program      TYPE
    1 1| | | Funcs      program      TYPE    file1.m
    1 1| | | | Main       func_common  TYPE    main
    1 1| | | | | Declares   func_return  int
    1 1| | | | | | Var        int          int     a
    1 1| | | | | Returns    func_return  TYPE
    1 1| | | | | Params     func_return  TYPE
    1 1| | | | | Block      code_block   TYPE
    1 1| | | | | | Assign     unknown      TYPE
    1 1| | | | | | | Var        int          int     a
    1 5| | | | | | | Int        int          int
       | | | Inlines    program      TYPE    file1.m
       | | | Structs    program      TYPE    file1.m
       | | | Headers    program      TYPE    file1.m
       | | | Log        program      TYPE    file1.m

Multiple program can be loaded into the same builder. This allows for building
of projects that involves multiple files. For example::

    >>> builder = mc.Builder()
    >>> builder.load("a.m", "function y=a(x); y = x+1")
    >>> builder.load("b.m", "b = a(2)")

The two programs refer to each other through their names. This can the
suggestion engine use::

    >>> builder.configure(suggest=True)
    >>> print mc.qscript(builder[0])
    int a(int x)
    {
      int y ;
      y = x+1 ;
      return y ;
    }
    >>> print mc.qscript(builder[1])
    b = a(2) ;
"""

import matlab2cpp as mc

import expression
import functions
import variables
import misc
import branches
import iterate
import assign
import codeblock

class Builder(object):
    """
Convert Matlab-code to a tree of nodes.

+--------------------------------------------+---------------------------------+
| Method                                     | Description                     |
+============================================+=================================+
| :py:func:`~matlab2cpp.Builder.configure`   | Use assigned values and         |
|                                            | suggestion                      |
|                                            | engine to fill in datatypes     |
+--------------------------------------------+---------------------------------+
| :py:func:`~matlab2cpp.Builder.load`        | Load code with a given name     |
+--------------------------------------------+---------------------------------+
| :py:func:`~matlab2cpp.Builder.syntaxerror` | Throw an apropriate SyntaxError |
|                                            | for the Matlab code             |
+--------------------------------------------+--------------------++-----------+
| :py:func:`~matlab2cpp.Builder.translate`   | Translate tree to C++           |
+--------------------------------------------+--------------------++-----------+

    """

    def __init__(self, disp=False, comments=True, **kws):
        """
Args:
    disp (bool):
        Verbose output while loading code
    comments (bool):
        Include comments in the code interpretation
    **kws: 
        Optional arguments are passed to :py:mod:`~matlab2cpp.rules`

See also:
    :py:mod:`~matlab2cpp.rules`
        """

        self.disp = disp
        self.comments = comments
        self.project = mc.collection.Project()
        self.project.kws = kws
        self.project.builder = self

    def load(self, name, code):
        """
Load a Matlab code into the node tree.

Args:
    name (str): Name of program (usually valid filename).
    code (str): Matlab code to be loaded

Raises:
    SyntaxError: Error in the Matlab code.

Example::

    >>> builder = mc.Builder()
    >>> print builder
      | Project    program      TYPE    project
    >>> builder.load("unnamed.m", "")
    >>> print builder # doctest: +NORMALIZE_WHITESPACE
       | Project    program      TYPE    project
       | | Program    program      TYPE    unnamed.m
       | | | Includes   program      TYPE
    1 1| | | Funcs      program      TYPE    unnamed.m
       | | | Inlines    program      TYPE    unnamed.m
       | | | Structs    program      TYPE    unnamed.m
       | | | Headers    program      TYPE    unnamed.m
       | | | Log        program      TYPE    unnamed.m
        """

        if self.disp:
            print "loading", name

        self.code = code + "\n\n\n"
        self.create_program(name)


    def configure(self, suggest=True, **kws):
        """
Configure node tree with datatypes.

Args:
    suggest (bool): Uses suggestion engine to fill in types

Example::

    >>> builder = mc.Builder()
    >>> builder.load("unnamed.m", "a=1; b=2.; c='c'")
    >>> print builder # doctest: +NORMALIZE_WHITESPACE
       | Project    program      TYPE    project
       | | Program    program      TYPE    unnamed.m
       | | | Includes   program      TYPE
    1 1| | | Funcs      program      TYPE    unnamed.m
    1 1| | | | Main       func_common  TYPE    main
    1 1| | | | | Declares   func_return  TYPE
    1 1| | | | | | Var        unknown      TYPE    a
    1 1| | | | | | Var        unknown      TYPE    b
    1 1| | | | | | Var        unknown      TYPE    c
    1 1| | | | | Returns    func_return  TYPE
    1 1| | | | | Params     func_return  TYPE
    1 1| | | | | Block      code_block   TYPE
    1 1| | | | | | Assign     unknown      TYPE
    1 1| | | | | | | Var        unknown      TYPE    a
    1 3| | | | | | | Int        int          int
    1 6| | | | | | Assign     unknown      TYPE
    1 6| | | | | | | Var        unknown      TYPE    b
    1 8| | | | | | | Float      double       double
    1 12| | | | | | Assign     unknown      TYPE
    1 12| | | | | | | Var        unknown      TYPE    c
    1 14| | | | | | | String     string       string
       | | | Inlines    program      TYPE    unnamed.m
       | | | Structs    program      TYPE    unnamed.m
       | | | Headers    program      TYPE    unnamed.m
       | | | Log        program      TYPE    unnamed.m
    >>> builder.configure(suggest=True)
    >>> print builder # doctest: +NORMALIZE_WHITESPACE
       | Project    program      TYPE    project
       | | Program    program      TYPE    unnamed.m
       | | | Includes   program      TYPE
    1 1| | | Funcs      program      TYPE    unnamed.m
    1 1| | | | Main       func_common  TYPE    main
    1 1| | | | | Declares   func_return  TYPE
    1 1| | | | | | Var        int          int     a
    1 1| | | | | | Var        double       double  b
    1 1| | | | | | Var        string       string  c
    1 1| | | | | Returns    func_return  TYPE
    1 1| | | | | Params     func_return  TYPE
    1 1| | | | | Block      code_block   TYPE
    1 1| | | | | | Assign     unknown      TYPE
    1 1| | | | | | | Var        int          int     a
    1 3| | | | | | | Int        int          int
    1 6| | | | | | Assign     unknown      TYPE
    1 6| | | | | | | Var        double       double  b
    1 8| | | | | | | Float      double       double
    1 12| | | | | | Assign     unknown      TYPE
    1 12| | | | | | | Var        string       string  c
    1 14| | | | | | | String     string       string
       | | | Inlines    program      TYPE    unnamed.m
       | | | Structs    program      TYPE    unnamed.m
       | | | Headers    program      TYPE    unnamed.m
       | | | Log        program      TYPE    unnamed.m
    """
        mc.configure.configure(self, suggest, **kws)

    def translate(self):
        """
Translate node tree
        """
        for program in self.project:
            program.translate()

    def syntaxerror(self, cur, text):
        """
Raise an SyntaxError related to the Matlab code.

Args:
    cur (int): Current location in the Matlab code
    text (str): The related rational presented to the user

Raises:
    SyntaxError: Error in the Matlab code.

Example::

    >>> builder = mc.Builder()
    >>> prg = builder.load("unnamed.m", "0123456789")
    >>> builder.syntaxerror(7, "example of error")
    Traceback (most recent call last):
        ...
    SyntaxError: line 1 in Matlab code:
    0123456789
           ^
    Expected: example of error
    """

        start = cur-1
        while start > 0 and self.code[start] != "\n":
            start -= 1

        end = cur+1
        while end < len(self.code) and self.code[end] != "\n":
            end += 1

        out = "line %d in Matlab code:\n" % (self.code.count("\n", 0, cur)+1)
        out += self.code[start:end] + "\n" + " "*(cur-start) + "^\n"
        out += "Expected: " + text
        raise SyntaxError(out)

    def get_unknowns(self, name):

        program = self.project[self.project.names.index(name)]

        nodes = program.flatten(False, True, False)
        # Find if some names should be reserved
        unassigned = {}
        for node in nodes[::-1]:

            if node.cls not in ("Var", "Fvar", "Cvar", "Set", "Cset", "Sset",
                    "Fset", "Nset", "Get", "Cget", "Fget", "Nget", "Sget"):
                continue

            if node.name not in unassigned:
                unassigned[node.name] = True

            if node.parent.cls in ("Params", "Declares"):
                unassigned[node.name] = False

        unassigned = [k for k,v in unassigned.items() if v]

        reserved = set([])
        for i in xrange(len(unassigned)-1, -1, -1):

            if unassigned[i] in mc.rules._reserved.reserved:
                reserved.add(unassigned.pop(i))

        for node in nodes[::-1]:

            if node.name in reserved:
                node.backend = "reserved"

        return unassigned

    def __getitem__(self, i):
        return self.project[i]

    def __str__(self):
        return self.project.summary()
        

    def create_program(self, name):
        return functions.program(self, name)

    def create_function(self, parent, cur):
        return functions.function(self, parent, cur)

    def create_main(self, parent, cur):
        return functions.main(self, parent, cur)

    def create_lambda_assign(self, parent, cur, eq_loc):
        return functions.lambda_assign(self, parent, cur, eq_loc)

    def create_lambda_func(self, parent, cur):
        return functions.lambda_func(self, parent, cur)


    def create_codeblock(self, parent, start):
        return codeblock.codeblock(self, parent, start)


    def create_assigns(self, parent, cur, eq_loc):
        return assign.multi(self, parent, cur, eq_loc)

    def create_assign(self, parent, cur, eq_loc):
        return assign.single(self, parent, cur, eq_loc)


    def create_for(self, parent, cur):
        return branches.forloop(self, parent, cur)

    def create_if(self, parent, start):
        return branches.ifbranch(self, parent, start)

    def create_while(self, parent, cur):
        return branches.whileloop(self, parent, cur)

    def create_switch(self, parent, cur):
        return branches.switch(self, parent, cur)

    def create_try(self, parent, cur):
        return branches.trybranch(self, parent, cur)


    def create_cell(self, node, cur):
        return misc.cell(self, node, cur)

    def create_cell_arg(self, cset, cur):
        return misc.cell_arg(self, cset, cur)

    def create_comment(self, parent, cur):
        return misc.comment(self, parent, cur)

    #verbatim node
    def create_verbatim(self, parent, cur):
        return misc.verbatim(self, parent, cur)
    
    def create_string(self, parent, cur):
        return misc.string(self, parent, cur)

    def create_list(self, parent, cur):
        return misc.list(self, parent, cur)

    def create_matrix(self, parent, cur):
        return misc.matrix(self, parent, cur)

    def create_number(self, node, start):
        return misc.number(self, node, start)


    def create_variable(self, parent, cur):
        return variables.variable(self, parent, cur)

    def create_assign_variable(self, node, cur, end=None):
        return variables.assign(self, node, cur, end)


    def create_expression(self, node, start, end=None):
        return expression.create(self, node, start, end)


    def iterate_list(self, cur):
        return iterate.list(self, cur)

    def iterate_comma_list(self, cur):
        return iterate.comma_list(self, cur)

    def iterate_space_list(self, cur):
        return iterate.space_list(self, cur)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
