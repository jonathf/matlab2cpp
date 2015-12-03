"""
"""

import expression
import functions
import variables
import misc
import branches
import iterate
import assign
import codeblock
import suppliment
import identify

import matlab2cpp as mc

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
+--------------------------------------------+---------------------------------+
| :py:func:`~matlab2cpp.Builder.translate`   | Translate tree to C++           |
+--------------------------------------------+---------------------------------+

    """
    ftypes = suppliment.Fbuilder()
    stypes = suppliment.Sbuilder()
    itypes = suppliment.Ibuilder()
    vtypes = suppliment.Vbuilder()

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

        self.configured = False

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
         Project    unknown      TYPE    project
    >>> builder.load("unnamed.m", "")
    >>> print builder # doctest: +NORMALIZE_WHITESPACE
         Project    unknown      TYPE    project
         | Program    unknown      TYPE    unnamed.m
         | | Includes   unknown      TYPE
     1  1| | Funcs      unknown      TYPE    unnamed.m
         | | Inlines    unknown      TYPE    unnamed.m
         | | Structs    unknown      TYPE    unnamed.m
         | | Headers    unknown      TYPE    unnamed.m
         | | Log        unknown      TYPE    unnamed.m
        """

        if self.disp:
            print "loading", name

        self.code = code + "\n\n\n"
        self.create_program(name)

        index = self.project.names.index(name)
        program = self.project[index]

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

        program.unassigned = unassigned

    def get_unknowns(self, name):
        index = self.project.names.index(name)
        return self.project[index].unassigned

    def configure(self, suggest=True, **kws):
        """
Configure node tree with datatypes.

Args:
    suggest (bool): Uses suggestion engine to fill in types

Example::

    >>> builder = mc.Builder()
    >>> builder.load("unnamed.m", "a=1; b=2.; c='c'")
    >>> print builder # doctest: +NORMALIZE_WHITESPACE
         Project    unknown      TYPE    project
         | Program    unknown      TYPE    unnamed.m
         | | Includes   unknown      TYPE
     1  1| | Funcs      unknown      TYPE    unnamed.m
     1  1| | | Main       unknown      TYPE    main
     1  1| | | | Declares   unknown      TYPE
     1  1| | | | | Var        unknown      TYPE    a
     1  1| | | | | Var        unknown      TYPE    b
     1  1| | | | | Var        unknown      TYPE    c
     1  1| | | | Returns    unknown      TYPE
     1  1| | | | Params     unknown      TYPE
     1  1| | | | Block      unknown      TYPE
     1  1| | | | | Assign     unknown      TYPE
     1  1| | | | | | Var        unknown      TYPE    a
     1  3| | | | | | Int        unknown      TYPE
     1  6| | | | | Assign     unknown      TYPE
     1  6| | | | | | Var        unknown      TYPE    b
     1  8| | | | | | Float      unknown      TYPE
     1 12| | | | | Assign     unknown      TYPE
     1 12| | | | | | Var        unknown      TYPE    c
     1 14| | | | | | String     unknown      TYPE
         | | Inlines    unknown      TYPE    unnamed.m
         | | Structs    unknown      TYPE    unnamed.m
         | | Headers    unknown      TYPE    unnamed.m
         | | Log        unknown      TYPE    unnamed.m
    >>> builder.configure(suggest=True)
    >>> print builder # doctest: +NORMALIZE_WHITESPACE
         Project    program      TYPE    project
         | Program    program      TYPE    unnamed.m
         | | Includes   program      TYPE
     1  1| | Funcs      program      TYPE    unnamed.m
     1  1| | | Main       func_return  TYPE    main
     1  1| | | | Declares   func_return  TYPE
     1  1| | | | | Var        int          int     a
     1  1| | | | | Var        double       double  b
     1  1| | | | | Var        string       string  c
     1  1| | | | Returns    func_return  TYPE
     1  1| | | | Params     func_return  TYPE
     1  1| | | | Block      code_block   TYPE
     1  1| | | | | Assign     unknown      int 
     1  1| | | | | | Var        int          int     a
     1  3| | | | | | Int        int          int
     1  6| | | | | Assign     unknown      double
     1  6| | | | | | Var        double       double  b
     1  8| | | | | | Float      double       double
     1 12| | | | | Assign     unknown      string
     1 12| | | | | | Var        string       string  c
     1 14| | | | | | String     string       string
         | | Inlines    program      TYPE    unnamed.m
         | | Structs    program      TYPE    unnamed.m
         | | Headers    program      TYPE    unnamed.m
         | | Log        program      TYPE    unnamed.m
    """
        if self.configured:
            raise Exception("configure can only be run once")
        self.configured = True
        mc.configure.configure(self, suggest, **kws)

    def translate(self):
        """
Translate node tree
        """

        if not self.configured:
            self.configure()

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

    def create_reserved(self, node, start):
        return misc.reserved(self, node, start)


    def create_variable(self, parent, cur):
        return variables.variable(self, parent, cur)

    def create_assign_variable(self, node, cur, end=None):
        return variables.assign(self, node, cur, end)


    def create_expression(self, node, start, end=None):
        return expression.create(self, node, start, end)


    def iterate_list(self, cur):
        if identify.space_delimited(self, cur):
            return self.iterate_space_list(cur)
        return self.iterate_comma_list(cur)

    def iterate_comma_list(self, cur):
        return iterate.comma_list(self, cur)

    def iterate_space_list(self, cur):
        return iterate.space_list(self, cur)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
