from . import (
    expression,
    functions,
    variables,
    misc,
    branches,
    iterate,
    assign,
    codeblock,
    suppliment,
    identify,
)

import matlab2cpp as mc

class Builder(object):
    """
Convert Matlab-code to a tree of nodes.

Given that one or more Matlab programs are loaded, each one can be accessed
through indexing the Builder instance. For example::

    >>> builder = mc.Builder()
    >>> builder.load("prg1.m", "function y=prg1(x); y=x")
    >>> builder.load("prg2.m", "prg1(4)")
    >>> builder.configure(suggest=True)
    >>> builder.translate()
    >>> prg1, prg2 = builder
    >>> print(prg1.cls, prg1.name)
    Program prg1.m
    >>> print(prg2.cls, prg2.name)
    Program prg2.m

Programs that are loaded, configured and translated, can be converted into C++
code through the front end functions in :py:mod:`matlab2cpp.qfunctions`::

    >>> print(mc.qhpp(prg1))
    #ifndef PRG1_M_HPP
    #define PRG1_M_HPP
    <BLANKLINE>
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    int prg1(int x)
    {
      int y ;
      y = x ;
      return y ;
    }
    #endif
    >>> print(mc.qcpp(prg2))
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    int main(int argc, char** argv)
    {
      prg1(4) ;
      return 0 ;
    }
    """

    def __init__(self, disp=False, comments=True, original=False, enable_omp=False, enable_tbb=False,
                 reference=False, **kws):
        """
Args:
    disp (bool):
        Verbose output while loading code
    comments (bool):
        Include comments in the code interpretation
    **kws: 
        Optional arguments are passed to :py:mod:`matlab2cpp.rules`
        """

        self.disp = disp
        self.comments = comments
        self.original = original
        self.project = mc.collection.Project()
        self.project.kws = kws
        self.project.builder = self
        self.enable_omp = enable_omp
        self.enable_tbb = enable_tbb
        self.reference = reference
        self.configured = False


    def __getitem__(self, index):
        """
Get root node for a program through indexing

builder[index] <=> Builder.__getitem__(builder, index)


Args:
    index (int): Loaded order

Example:

    >>> builder = mc.Builder()
    >>> builder.load("prg1.m", "function y=prg1(x); y=x")
    >>> builder.load("prg2.m", "prg1(4)")
    >>> prg1 = builder[0]
    >>> prg2 = builder[1]
        """
        return self.project[index]

    def __str__(self):
        """
Summary of all node trees

Same as :py:func:`matlab2cpp.Node.summary`, but for the whole project.

str(builder) <=> Builder.__str__(builder)

Example:
    >>> builder = mc.Builder()
    >>> print(builder) # doctest: +NORMALIZE_WHITESPACE
         Project    unknown      TYPE

See also:
    :py:func:`matlab2cpp.Node.summary`
        """
        return self.project.summary()


    def load(self, name, code):
        """
Load a Matlab code into the node tree.

The code is inserted into the attribute `self.code` and initiate the
:py:func:`matlab2cpp.Builder.create_program`, which evoces various other
``create_*`` methods. Each method creates nodes and/or pushes the job over to
other create methods.

Args:
    name (str): Name of program (usually valid filename).
    code (str): Matlab code to be loaded

Raises:
    SyntaxError: Error in the Matlab code.

Example::
    >>> builder = mc.Builder()
    >>> builder.load("unnamed.m", "")
    >>> print(builder) # doctest: +NORMALIZE_WHITESPACE
         Project    unknown      TYPE
         | Program    unknown      TYPE    unnamed.m
         | | Includes   unknown      TYPE
     1  1| | Funcs      unknown      TYPE    unnamed.m
         | | Inlines    unknown      TYPE    unnamed.m
         | | Structs    unknown      TYPE    unnamed.m
         | | Headers    unknown      TYPE    unnamed.m
         | | Log        unknown      TYPE    unnamed.m
        """
        assert isinstance(name, str)
        assert isinstance(code, str)

        if self.disp:
            print("loading", name)
        
        #Replace ... [stuff] \n with ... [stuff] \n " "
        l = 0
        while l != -1:  #str.find returns -1 if not found
            l = code.find("...", l)
            if l != -1:
                m = code.find("\n", l)
                if m != -1:
                    #m = m+1
                    code = code[:m+1] + " " + code[m+1:]
                l = m
        
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


    def get_unknowns(self, index=-1):
        """
Get unknown variables and function calls names in a program.

Args:
    index (int, str): Either loading index or the name of the program.

Returns:
    list: strings of the names of the unknown variables and calls.

Example:
    >>> builder = Builder(); builder.load("prg.m", "a;b;c")
    >>> print(builder.get_unknowns())
    ['a', 'c', 'b']
        """
        if isinstance(index, str):
            index = self.project.names.index(index)
        assert isinstance(index, int)
        return self.project[index].unassigned


    def configure(self, suggest=True, **kws):
        """
Configure node tree with datatypes.

Args:
    suggest (bool): Uses suggestion engine to fill in types

Example::
    >>> builder = mc.Builder()
    >>> builder.load("unnamed.m", "a=1; b=2.; c='c'")
    >>> print(builder) # doctest: +NORMALIZE_WHITESPACE
         Project    unknown      TYPE
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
    >>> print(builder) # doctest: +NORMALIZE_WHITESPACE
         Project    program      TYPE
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
     1  1| | | | | Assign     int          int 
     1  1| | | | | | Var        int          int     a
     1  3| | | | | | Int        int          int
     1  6| | | | | Assign     double       double
     1  6| | | | | | Var        double       double  b
     1  8| | | | | | Float      double       double
     1 12| | | | | Assign     string       string
     1 12| | | | | | Var        string       string  c
     1 14| | | | | | String     string       string
         | | Inlines    program      TYPE    unnamed.m
         | | Structs    program      TYPE    unnamed.m
         | | Headers    program      TYPE    unnamed.m
         | | Log        program      TYPE    unnamed.m

Raises:
    RuntimeError: Method can only be run once.
    """
        if self.configured:
            raise RuntimeError("configure can only be run once")
        self.configured = True
        mc.configure.configure(self, suggest, **kws)


    def translate(self):
        """
Perform translation on all nodes in all programs in builder.
Also runs configure if not done already.

See also:
    :py:mod:`matlab2cpp.rules`
        """

        if not self.configured:
            self.configure()

        for program in self.project:
            program.translate()


    def syntaxerror(self, cur, text):
        """
Raise an SyntaxError related to the Matlab code. Called from various
``create_*`` methods when code is invalid.

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
    SyntaxError: File: unnamed.m, line 1 in Matlab code:
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

        out = "File: %s, line %d in Matlab code:\n" % (self.project[-1].name, self.code.count("\n", 0, cur)+1)
        out += self.code[start:end] + "\n" + " "*(cur-start) + "^\n"
        out += "Expected: " + text
        raise SyntaxError(out)


    def create_program(self, name):
        """
Create program meta variables and initiates to fill them

| Structure:
|   Program
|   | Includes
|   | Funcs
|   | Inlines
|   | Structs
|   | Headers
|   | Log

Args:
    name (str): filename of program

Returns:
    int: position in program when scanning is complete.

See also:
    :py:func:`matlab2cpp.tree.functions.program`
    """
        assert isinstance(name, (int, str))
        return functions.program(self, name)


    def create_function(self, parent, cur):
        """
Create function (not main)

| Structure:
|   Func
|   | Declares
|   | Returns
|   | Params
|   | <code block>

Args:
    parent (Funcs): Reference to parent node
    cur (int): position where function is identified

Returns:
    int: position where function ends

See also:
    :py:func:`matlab2cpp.tree.functions.function`
    """
        assert isinstance(parent, mc.collection.Funcs)
        return functions.function(self, parent, cur)


    def create_main(self, parent, cur):
        """
Create main function

| Structure:
|   Main
|   | Declares
|   | Returns
|   | Params
|   | <code block>

Args:
    parent (Funcs): Reference to parent node
    cur (int): position where main function is identified

Returns:
    int: position where main function ends

See also:
    :py:func:`matlab2cpp.tree.functions.main`
    """
        assert isinstance(parent, mc.collection.Funcs)
        return functions.main(self, parent, cur)


    def create_lambda_assign(self, parent, cur, eq_loc):
        """
Create assignments involving lambda functions

| Structure:
|   Assign
|   | <assign variable>
|   | <lambda function>

Args:
    parent (Block): Reference to parent node
    cur (int): position where Lambda assignment is identified
    eq_loc (int): position of assignment equal sign

Returns:
    int: position where Lambda assignment ends

See also:
    :py:func:`matlab2cpp.tree.functions.lambda_assign`
    """
        assert isinstance(parent, mc.collection.Block)
        return functions.lambda_assign(self, parent, cur, eq_loc)


    def create_lambda_func(self, parent, cur):
        """
Create lambda function

| Structure (function part):
|   Func
|   | Declares
|   | Returns
|   | | Var (_retval)
|   | Params
|   | Block
|   | | Assign
|   | | | Var (_retval)
|   | | | <expression>
|
| Structure (lambda part):
|   Lambda


Args:
    parent (Assign): Reference to parent node
    cur (int): position where Lambda function is identified

Returns:
    int: position where Lambda function ends

See also:
    :py:func:`matlab2cpp.tree.functions.lambda_func`
    """
        assert isinstance(parent, mc.collection.Assign)
        return functions.lambda_func(self, parent, cur)


    def create_codeblock(self, parent, cur):
        """
Create codeblock Block

| Structure:
|   Assign|Assigns|Bcomment|Ecomment|Lcomment|Statement

`Statements` are handled locally and evoces <expression>

Legal parents:
Case, Catch, Elif, Else, For, Func, If, Main, Otherwise, Switch, Try, While

Args:
    parent (Node): Reference to parent node
    cur (int): position where codeblock is identified

Returns:
    int: position where codeblock ends

See also:
    :py:func:`matlab2cpp.tree.codeblock.codeblock`
    """
        pnames = [ "Case", "Catch", "Elif", "Else", "Parfor", "For", "Func", "If",
                "Main", "Otherwise", "Switch", "Try", "While"]
        pnodes = [getattr(mc.collection, name) for name in pnames]
        ppart = [isinstance(parent, node) for node in pnodes]
        if not any(ppart):
            raise AssertionError(
                    "parent of Block: %s not valid group parent\n%s" %\
                    (parent.cls, str(pnames)))
        return codeblock.codeblock(self, parent, cur)


    def create_assigns(self, parent, cur, eq_loc):
        """
Create assignment with multiple returns

| Structure:
|   Assigns
|   | <list of return vars>
|   | Get|Var

Args:
    parent (Block): Reference to parent node
    cur (int): position where assignments is identified
    eq_loc (int): position of assignment equal sign

Returns:
    int: position where assignments ends

See also:
    :py:func:`matlab2cpp.tree.assign.multi`
    """
        assert isinstance(parent, mc.collection.Block)
        return assign.multi(self, parent, cur, eq_loc)


    def create_assign(self, parent, cur, eq_loc):
        """
Create assignment with single return

| Structure:
|   Assign
|   | <return var>
|   | Get|Var

Args:
    parent (Block): Reference to parent node
    cur (int): position where assignment is identified
    eq_loc (int): position of assignment equal sign

Returns:
    int: position where assignment ends

See also:
    :py:func:`matlab2cpp.tree.assign.single`
    """
        assert isinstance(parent, mc.collection.Block)
        return assign.single(self, parent, cur, eq_loc)

    def create_parfor(self, parent, cur):
        """
Create parfor-loop

| Structure:
|   Parfor
|   | <loop variable>
|   | <loop expression>
|   | <code block>

Args:
    parent (Block): Reference to parent node
    cur (int): position where for-loop is identified

Returns:
    int: position where for-loop ends
        """

        assert isinstance(parent, mc.collection.Block)
        return branches.parforloop(self, parent, cur)
    
    def create_for(self, parent, cur):
        """
Create For-loop

| Structure:
|   For
|   | <loop variable>
|   | <loop expression>
|   | <code block>

Args:
    parent (Block): Reference to parent node
    cur (int): position where for-loop is identified

Returns:
    int: position where for-loop ends

See also:
    :py:func:`matlab2cpp.tree.branches.forloop`
    """
        assert isinstance(parent, mc.collection.Block)
        return branches.forloop(self, parent, cur)


    def create_if(self, parent, cur):
        """
Create if-branch

| Structure (main):
|   Branch
|   | If
|   | | <cond expression>
|   | | <code block>
|   | <else if>*
|   | <else>?
|
| Structure (else if):
|   Elif
|   | <cond expression>
|   | <code block>
|
| Structure (else):
|   Else
|   | <code block>

Args:
    parent (Block): Reference to parent node
    cur (int): position where if-branch is identified

Returns:
    int: position where if-branch ends

See also:
    :py:func:`matlab2cpp.tree.branches.ifbranch`
    """
        assert isinstance(parent, mc.collection.Block)
        return branches.ifbranch(self, parent, cur)


    def create_while(self, parent, cur):
        """
Create while-loop

| Structure:
|   While
|   | <cond expression>
|   | <code block>

Args:
    parent (Block): Reference to parent node
    cur (int): position where while-loop is identified

Returns:
    int: position where while-loop ends

See also:
    :py:func:`matlab2cpp.tree.branches.whileloop`
    """
        assert isinstance(parent, mc.collection.Block)
        return branches.whileloop(self, parent, cur)


    def create_switch(self, parent, cur):
        """
Create switch-branch

| Structure (main):
|   Switch
|   | <cond expression>
|   | <case>+
|   | <otherwise>?
|
| Structure (case):
|   Case
|   | <cond expression>
|   | <code block>
|
| Structure (otherwise):
|   Otherwise
|   | <code block>

Args:
    parent (Block): Reference to parent node
    cur (int): position where switch is identified

Returns:
    int: position where switch ends

See also:
    :py:func:`matlab2cpp.tree.branches.switch`
    """
        assert isinstance(parent, mc.collection.Block)
        return branches.switch(self, parent, cur)


    def create_try(self, parent, cur):
        """
Create try-block

| Structure:
|   Tryblock
|   | Try
|   | | <code block>
|   | Catch
|   | | <code block>

Args:
    parent (Block): Reference to parent node
    cur (int): position where try-block is identified

Returns:
    int: position where try-block ends

See also:
    :py:func:`matlab2cpp.tree.branches.trybranch`
    """
        assert isinstance(parent, mc.collection.Block)
        return branches.trybranch(self, parent, cur)


    def create_cell(self, parent, cur):
        """
Create cell-structure (expression)

| Structure:
|   Cell
|   | <expression>+

Args:
    parent (Node): Reference to parent node
    cur (int): position where cell is identified

Returns:
    int: position where cell ends

See also:
    :py:func:`matlab2cpp.tree.misc.cell`
    """
        return misc.cell(self, parent, cur)

    def create_pragma_parfor(self, parent, cur):
        assert isinstance(parent, mc.collection.Block)
        return misc.pragma_for(self, parent, cur)

    def create_comment(self, parent, cur):
        """
Create comment

| Structure:
|   Bcomment|Ecomment|Lcomment

Args:
    parent (Block): Reference to parent node
    cur (int): position where comment is identified

Returns:
    int: position where comment ends

See also:
    :py:func:`matlab2cpp.tree.misc.comment`
    """
        assert isinstance(parent, mc.collection.Block)
        return misc.comment(self, parent, cur)


    def create_verbatim(self, parent, cur):
        """
Create verbatim translation

A manual overrides switch provided by the user to perform translations.

| Structure:
|   Verbatim

Args:
    parent (Block): Reference to parent node
    cur (int): position where verbatim is identified
    
Returns:
    int: position where verbatim ends

See also:
    :py:func:`matlab2cpp.tree.misc.verbatim`
    """
        return misc.verbatim(self, parent, cur)
    

    def create_string(self, parent, cur):
        """
Create string (Expression)

| Structure:
|   String

Args:
    parent (Node): Reference to parent node
    cur (int): position where string is identified

Returns:
    int: position where string ends

See also:
    :py:func:`matlab2cpp.tree.misc.string`
    """
        return misc.string(self, parent, cur)


    def create_list(self, parent, cur):
        """
Create list of expressions

| Structure:
|   <expression>*

Args:
    parent (Node): Reference to parent node
    cur (int): position where list is identified

Returns:
    int: position where list ends

See also:
    :py:func:`matlab2cpp.tree.misc.list`
    """
        return misc.list(self, parent, cur)


    def create_matrix(self, parent, cur):
        """
Create matrix (Expression)

| Structure (main):
|   Matrix
|   | <vector>*
|
| Structure (vector):
|   Vector
|   | <expression>*

Args:
    parent (Node): Reference to parent node
    cur (int): position where matrix is identified

Returns:
    int: position where matrix ends

See also:
    :py:func:`matlab2cpp.tree.misc.matrix`
    """
        return misc.matrix(self, parent, cur)


    def create_number(self, parent, cur):
        """
Create number (Expression)

| Structure:
|   Int|Float|Imag

Args:
    parent (Node): Reference to parent node
    cur (int): position where number is identified

Returns:
    int: position where number ends

See also:
    :py:func:`matlab2cpp.tree.misc.number`
    """
        return misc.number(self, parent, cur)


    def create_reserved(self, parent, cur):
        """
Create Matlab reserved keywords.

Some words like "hold", "grid" and "clear", behaves differently than regular
Matlab. They take arguments after space, not in parenthesis.

| Structure (main):
|   Get
|   | <string>*
|
| Structure (string):
|   String

Args:
    parent (Block): Reference to parent node
    cur (int): position where reserved statement is identified

Returns:
    int: position where reserved statement ends

See also:
    :py:func:`matlab2cpp.tree.misc.reserved`
    """
        assert isinstance(parent, mc.collection.Block)
        return misc.reserved(self, parent, cur)


    def create_variable(self, parent, cur):
        """
Create left-hand-side variable (Expression)

| Structure:
|   Cget|Cvar|Fget|Fvar|Get|Nget|Var|Sget|Svar
|   | <list of expression>?

Args:
    parent (Node): Reference to parent node
    cur (int): position where variable is identified

Returns:
    int: position where variable ends

See also:
    :py:func:`matlab2cpp.tree.variables.variable`
    """
        return variables.variable(self, parent, cur)

    def create_assign_variable(self, parent, cur, end=None):
        """
Create right-hand-side variable (Expression)

| Structure:
|   Cset|Cvar|Fset|Fvar|Nset|Var|Set|Sset|Svar
|   | <list of expression>?

Args:
    parent (Node): Reference to parent node
    cur (int): position where variable is identified
    end (int, optional): position where variable ends

Returns:
    int: position where variable ends

See also:
    :py:func:`matlab2cpp.tree.variables.assign`
    """
        return variables.assign(self, parent, cur, end)


    def create_expression(self, parent, cur, end=None):
        """
Create expression

Main engine for creating expression.

Args:
    parent (Node): Reference to parent node
    cur (int): position where expression is identified
    end (int, optional): position where expression ends

Returns:
    int: position where expression ends

See also:
    :py:func:`matlab2cpp.tree.expression.create`
    """
        return expression.create(self, parent, cur, end)



if __name__ == "__main__":
    import doctest
    doctest.testmod()
