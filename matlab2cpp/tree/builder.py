from matlab2cpp.node import collection as col

import matlab2cpp.rules as rules

from matlab2cpp.configure import configure

import expression
import functions
import variables
import misc
import branches
import iterate
import assign
import codeblock

class Builder(object):
    """Convert Matlab-code to Node-tree"""

    def __init__(self, disp=False, comments=True, **kws):
        """
   Kwargs:
        disp (bool):
            Verbose output while loading code.
        comments (bool):
            Include comments in the code interpretation.
        """

        self.disp = disp
        self.comments = comments
        self.project = col.Project()
        self.project.kws = kws

    def __getitem__(self, i):
        return self.project[i]

    def syntaxerror(self, cur, text):
        """
Raise an SyntaxError related to the Matlab code.

Args:
    cur (int): Current location in the Matlab code
    text (str): The related rational presented to the user

Example:

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

    def load(self, name, code):
        """
    Load a Matlab code into the node tree.

    Will throw and exception if module loaded without the `folder` option.

    Args:
        name (str):
            Name of program (usually valid filename).
        code (str):
            Matlab code to be loaded
        """

        if self.disp:
            print "loading", name

        self.code = code + "\n\n\n"
        self.create_program(name)
        return self.project[-1]


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

            if unassigned[i] in rules._reserved.reserved:
                reserved.add(unassigned.pop(i))

        for node in nodes[::-1]:

            if node.name in reserved:
                node.backend = "reserved"

        return unassigned

    def configure(self, suggest=True, **kws):
        configure(self, suggest, **kws)


    def create_program(self, name):
        return functions.program(self, name)

    def create_function(self, parent, cur):
        return functions.function(self, parent, cur)

    def create_main(self, parent, cur):
        return functions.main(self, parent, cur)

    def create_lambda(self, parent, cur, eq_loc):
        return functions.lambda_(self, parent, cur, eq_loc)

    def create_lambda_func(self, parent, cur):
        return functions.lambda_func(self, parent, cur)


    def create_codeblock(self, parent, start):
        return codeblock.newblock(self, parent, start)


    def create_assigns(self, parent, cur, eq_loc):
        return assign.multi(self, parent, cur, eq_loc)

    def create_assign(self, parent, cur, eq_loc):
        return assign.single(self, parent, cur, eq_loc)


    def create_for(self, parent, cur):
        return branches.for_(self, parent, cur)

    def create_if(self, parent, start):
        return branches.if_(self, parent, start)

    def create_while(self, parent, cur):
        return branches.while_(self, parent, cur)

    def create_switch(self, parent, cur):
        return branches.switch(self, parent, cur)

    def create_try(self, parent, cur):
        return branches.try_(self, parent, cur)


    def create_cell(self, node, cur):
        return misc.cell(self, node, cur)

    def create_cell_arg(self, cset, cur):
        return misc.cell_arg(self, cset, cur)

    def create_comment(self, parent, cur):
        return misc.comment(self, parent, cur)

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
