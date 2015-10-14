"""
Support functions for identifying assignments.

+-------------------------------------------+----------------------------------+
| Function                                  | Description                      |
+===========================================+==================================+
| :py:func:`~matlab2cpp.tree.assign.single` | Assignment with single return    |
+-------------------------------------------+----------------------------------+
| :py:func:`~matlab2cpp.tree.assign.multi`  | Assignment with multiple returns |
+-------------------------------------------+----------------------------------+
"""
import matlab2cpp

import findend
import constants as c

def multi(self, parent, cur, eq_loc):
    """
Assignment with multiple return

Args:
    self (Builder): Code constructor.
    parent (Node): Parent node
    cur (int): Current position in code
    eq_loc (int): position of the assignment marker ('='-sign)

Returns:
	int: Index to end of assignment

Example:
    >>> builder = mc.Builder(True)
    >>> builder.load("unnamed", "[a,b] = c")
    loading unnamed
         Program     functions.program
       0 Main        functions.main
       0 Codeblock   codeblock.codeblock 
       0   Assigns     assign.multi         '[a,b] = c'
       1     Var         variables.assign     'a'
       3     Var         variables.assign     'b'
       8     Expression  expression.create    'c'
       8     Var         variables.variable   'c'
    >>> print mc.qtree(builder, core=True)
      1   1 Block      code_block   TYPE    
      1   1 Assigns    code_block   TYPE    c
      1   2 | Var        unknown      TYPE    a
      1   4 | Var        unknown      TYPE    b
      1   9 | Var        unknown      TYPE    c
    """

    if  self.code[cur] != "[":
        self.syntaxerror(cur, "multi-assign start")
    if  self.code[eq_loc] != "=":
        self.syntaxerror(cur, "assignment sign (=)")

    j = eq_loc+1
    while self.code[j] in " \t.":
        if self.code[j] == ".":
            j = findend.dots(self, j)+1
        else:
            j += 1
    end = findend.expression(self, j)

    if self.disp:
        print "%4d   Assigns    " %\
                cur,
        print "%-20s" % "assign.multi",
        print repr(self.code[cur:end+1])

    l = self.iterate_list(cur)

    if len(l[0]) == 1:
        return self.create_assign(parent, l[0][0][0], eq_loc)

    assigns = matlab2cpp.collection.Assigns(parent, cur=cur, code=self.code[cur:end+1])

    for vector in l:
        for start,stop in vector:
            self.create_assign_variable(assigns, start, end=stop)

    cur = eq_loc + 1
    while self.code[cur] in " \t":
        cur += 1

    cur_ =  self.create_expression(assigns, cur)

    assigns.name = assigns[-1].name

    return cur_


def single(self, parent, cur, eq_loc):
    """
Assignment with single return.

Args:
    self (Builder): Code constructor
    parent (Node): Parent node
    cur (int): Current position in code
    eq_loc (int): position of the assignment marker ('='-sign)

Returns:
	int: Index to end of assignment

Example:
    >>> builder = mc.Builder(True)
    >>> builder.load("unnamed", "a=b")
    loading unnamed
         Program     functions.program
       0 Main        functions.main
       0 Codeblock   codeblock.codeblock 
       0   Assign      assign.single        'a=b'
       0     Var         variables.assign     'a'
       2     Expression  expression.create    'b'
       2     Var         variables.variable   'b'
    >>> print mc.qtree(builder, core=True)
      1   1 Block      code_block   TYPE    
      1   1 Assign     unknown      TYPE    b
      1   1 | Var        unknown      TYPE    a
      1   3 | Var        unknown      TYPE    b
    """

    if  self.code[cur] not in c.letters:
        self.syntaxerror(cur, "assignment start")
    if  self.code[eq_loc] != "=":
        self.syntaxerror(cur, "assignment indicator (=)")

    j = eq_loc+1
    while self.code[j] in " \t":
        j += 1
    end = findend.expression(self, j)

    if self.disp:
        print "%4d   Assign     " %\
                cur,
        print "%-20s" % "assign.single",
        print repr(self.code[cur:end+1])

    assign = matlab2cpp.collection.Assign(parent, cur=cur, code=self.code[cur:end+1])

    cur = self.create_assign_variable(assign, cur, eq_loc)

    cur += 1
    while self.code[cur] in " \t":
        cur += 1

    if self.code[cur] == "]":
        cur += 1
        while self.code[cur] in " \t":
            cur += 1

    if  self.code[cur] != "=":
        self.syntaxerror(cur, "assignment indicator (=)")

    k = cur+1
    while self.code[k] in " \t":
        k += 1

    self.create_expression(assign, k, end)
    assign.name = assign[-1].name

    if  len(assign) != 2:
        self.syntaxerror(k, "single assign when multi-assign")

    return end

if __name__ == "__main__":
    import matlab2cpp as mc
    import doctest
    doctest.testmod()
