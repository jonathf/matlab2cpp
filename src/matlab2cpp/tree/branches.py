"""
Iterpretors related to branches, loops and try.

+------------------------------------------------+-----------------------+
| Function                                       | Description           |
+================================================+=======================+
| :py:func:`~matlab2cpp.tree.branches.trybranch` | Try-catch block       |
+------------------------------------------------+-----------------------+
| :py:func:`~matlab2cpp.tree.branches.switch`    | Switch-case branch    |
+------------------------------------------------+-----------------------+
| :py:func:`~matlab2cpp.tree.branches.whileloop` | While loop            |
+------------------------------------------------+-----------------------+
| :py:func:`~matlab2cpp.tree.branches.forloop`   | For loop              |
+------------------------------------------------+-----------------------+
| :py:func:`~matlab2cpp.tree.branches.ifbranch`  | If-ifelse-else branch |
+------------------------------------------------+-----------------------+
"""

import matlab2cpp as mc

from . import constants as c, findend


def trybranch(self, parent, cur):
    '''
Try-catch block

Args:
    self (Builder): Code constructor.
    parent (Node): Parent node
    cur (int): Current position in code

Returns:
	int: Index to end of block

Example:
    >>> builder = mc.Builder(True)
    >>> builder.load("unnamed",
    ... """try
    ...   a
    ... catch
    ...   b""")
    loading unnamed
         Program     functions.program
       0 Main        functions.main
       0 Codeblock   codeblock.codeblock 
       0   Try           branches.trybranch   'try'
       6 Codeblock   codeblock.codeblock 
       6   Statement     codeblock.codeblock  'a'
       6     Expression  expression.create    'a'
       6     Var         variables.variable   'a'
      16 Codeblock   codeblock.codeblock 
      16   Statement     codeblock.codeblock  'b'
      16     Expression  expression.create    'b'
      16     Var         variables.variable   'b'
    >>> builder.configure()
    >>> print(mc.qtree(builder, core=True)) # doctest: +NORMALIZE_WHITESPACE
    1  1Block      code_block   TYPE
    1  1| Tryblock   code_block   TYPE
    1  1| | Try        code_block   TYPE
    2  7| | | Block      code_block   TYPE
    2  7| | | | Statement  code_block   TYPE
    2  7| | | | | Var        unknown      TYPE    a
    3  9| | Catch      code_block   TYPE
    4 17| | | Block      code_block   TYPE
    4 17| | | | Statement  code_block   TYPE
    4 17| | | | | Var        unknown      TYPE    b
    '''

    if  self.code[cur:cur+3] != "try" or self.code[cur+3] not in c.k_end:
        self.syntaxerror(cur, "start of try-block")

    if self.disp:
        print("%4d   Try          " % cur,)
        print("%-20s" % "branches.trybranch",)
        print(repr(self.code[cur:cur+3]))

    start = cur

    tryblock = mc.collection.Tryblock(parent, cur=cur)

    trybranch = mc.collection.Try(tryblock)

    cur += 3
    while self.code[cur] in " \t\n,;":
        cur += 1

    cur = self.create_codeblock(trybranch, cur)

    trybranch.code = self.code[start:cur]

    if  self.code[cur:cur+5] != "catch" or self.code[cur+5] not in c.k_end:
        self.syntaxerror(cur, "start of catch-block")

    catch_ = mc.collection.Catch(tryblock, cur=cur)

    start_ = cur
    cur += 5
    while self.code[cur] in " \t\n,;":
        cur += 1

    cur = self.create_codeblock(catch_, cur)

    catch_.code = self.code[start_:cur]
    tryblock.code = self.code[start:cur]

    return cur


def switch(self, parent, cur):
    '''
Switch-case branch

Args:
    self (Builder): Code constructor.
    parent (Node): Parent node
    cur (int): Current position in code

Returns:
	int: Index to end of codeblock

Example:
    >>> builder = mc.Builder(True)
    >>> builder.load("unnamed",
    ... """switch a
    ... case b
    ...   c
    ... case d
    ...   d
    ... end""")
    loading unnamed
         Program     functions.program
       0 Main        functions.main
       0 Codeblock   codeblock.codeblock 
       0   Switch        branches.switch      'switch a'
       7     Expression  expression.create    'a'
       7     Var         variables.variable   'a'
       9   Case          branches.switch      'case b'
      14     Expression  expression.create    'b'
      14     Var         variables.variable   'b'
      18 Codeblock   codeblock.codeblock 
      18   Statement     codeblock.codeblock  'c'
      18     Expression  expression.create    'c'
      18     Var         variables.variable   'c'
      20   Case          branches.switch      'case d'
      25     Expression  expression.create    'd'
      25     Var         variables.variable   'd'
      29 Codeblock   codeblock.codeblock 
      29   Statement     codeblock.codeblock  'd'
      29     Expression  expression.create    'd'
      29     Var         variables.variable   'd'
    >>> builder.configure()
    >>> print(mc.qtree(builder, core=True)) # doctest: +NORMALIZE_WHITESPACE
    1  1Block      code_block   TYPE
    1  1| Switch     code_block   TYPE
    1  8| | Var        unknown      TYPE    a
    2 10| | Case       code_block   TYPE
    2 15| | | Var        unknown      TYPE    b
    3 19| | | Block      code_block   TYPE
    3 19| | | | Statement  code_block   TYPE
    3 19| | | | | Var        unknown      TYPE    c
    4 21| | Case       code_block   TYPE
    4 26| | | Var        unknown      TYPE    d
    5 30| | | Block      code_block   TYPE
    5 30| | | | Statement  code_block   TYPE
    5 30| | | | | Var        unknown      TYPE    d
    '''

    if not (self.code[cur:cur+6] == "switch" and\
            self.code[cur+6] in " \t("):
        self.syntaxerror(cur, "start of switch branch")

    k = cur+6
    while self.code[k] in " \t":
        k += 1

    end = findend.expression(self, k)

    if self.disp:
        print("%4d   Switch       " % cur,)
        print("%-20s" % "branches.switch",)
        print(repr(self.code[cur:end+1]))

    switch = mc.collection.Switch(parent, cur=cur)

    self.create_expression(switch, k, end)

    k = end+1

    while self.code[k] in " \t\n;,":
        k += 1

    while self.code[k:k+4] == "case" and self.code[k+4] in " \t(":

        cur = k

        k += 4
        while self.code[k] in " \t":
            k += 1

        end = findend.expression(self, k)

        if self.disp:
            print("%4d   Case         " % cur,)
            print("%-20s" % "branches.switch",)
            print(repr(self.code[cur:end+1]))

        case = mc.collection.Case(switch, cur=cur)

        cur = self.create_expression(case, k, end)

        k = cur+1
        while self.code[k] in " \t;,\n":
            k += 1

        k = self.create_codeblock(case, k)

    if self.code[k:k+9] == "otherwise" and self.code[k+9] in " \t(,;\n":

        cur = k

        if self.disp:
            print("%4d   Otherwise    " % cur,)
            print("%-20s" % "branches.switch",)
            print(repr(self.code[cur:cur+10]))

        otherwise = mc.collection.Otherwise(switch, cur=cur)

        k += 9
        while self.code[k] in " \t\n;,":
            k += 1

        k = self.create_codeblock(otherwise, k)

    return k


def whileloop(self, parent, cur):
    '''
While loop

Args:
    self (Builder): Code constructor.
    parent (Node): Parent node
    cur (int): Current position in code

Returns:
	int: Index to end of code block

Example:
    >>> builder = mc.Builder(True)
    >>> builder.load("unnamed",
    ... """while a
    ...   b
    ... end""")
    loading unnamed
         Program     functions.program
       0 Main        functions.main
       0 Codeblock   codeblock.codeblock 
       0   While         branches.whileloop   'while a'
       6     Expression  expression.create    'a'
       6     Var         variables.variable   'a'
      10 Codeblock   codeblock.codeblock 
      10   Statement     codeblock.codeblock  'b'
      10     Expression  expression.create    'b'
      10     Var         variables.variable   'b'
    >>> builder.configure()
    >>> print(mc.qtree(builder, core=True)) # doctest: +NORMALIZE_WHITESPACE
    1  1Block      code_block   TYPE
    1  1| While      code_block   TYPE
    1  7| | Var        unknown      TYPE    a
    2 11| | Block      code_block   TYPE
    2 11| | | Statement  code_block   TYPE
    2 11| | | | Var        unknown      TYPE    b
    '''

    if  self.code[cur:cur+5] != "while" and self.code[cur+5] not in c.k_end:
        self.syntaxerror(cur, "start of while-loop")
    start = cur

    k = cur+5
    while self.code[k] in " \t":
        k += 1

    end = findend.expression(self, k)

    if self.disp:
        print("%4d   While        " % cur,)
        print("%-20s" % "branches.whileloop",)
        print(repr(self.code[cur:end+1]))

    whileloop = mc.collection.While(parent, cur=cur, code=self.code[cur:end+1])

    if self.code[k] == "(":
        k += 1
        while self.code[k] in " \t":
            k += 1

    cur = self.create_expression(whileloop, k)
    cur += 1

    cur += 1
    while self.code[cur] in " \t":
        cur += 1

    end = self.create_codeblock(whileloop, cur)

    #whileloop.code = self.code[start:end+1]

    return end

def parforloop(self, parent, cur):
    if  self.code[cur:cur+6] != "parfor":
        self.syntaxerror(cur, "parfor loop start")

    start = cur

    if self.disp:
        print("%4d   Parfor          " % cur,)
        print(repr(self.code[cur:self.code.find("\n", cur)]),)
        print("branches.parforloop")

    parfor_loop = mc.collection.Parfor(parent, cur=cur, code=self.code[cur:self.code.find("\n", cur)])

    cur = cur+6
    while self.code[cur] in "( \t":
        cur += 1

    cur = self.create_variable(parfor_loop, cur)

    if parfor_loop.project.builder.enable_tbb:
        parfor_loop[0].type = "uword"

    else:
        parfor_loop[0].create_declare()
        parfor_loop[0].suggest = "int"

    cur += 1
    while self.code[cur] in " \t":
        cur += 1

    if self.code[cur] != "=":
        self.syntaxerror(cur, "for-loop assignment (=)")
    cur += 1

    while self.code[cur] in " \t":
        cur += 1

    cur = self.create_expression(parfor_loop, cur)
    cur += 1

    while self.code[cur] in ") \t":
        cur += 1

    if self.code[cur] == ",":
        cur += 1

    while self.code[cur] in " \t\n;":
        cur += 1
    end = self.create_codeblock(parfor_loop, cur)

    #parfor_loop.code = self.code[start:end]

    return end

def forloop(self, parent, cur):
    '''
For loop

Args:
    self (Builder): Code constructor.
    parent (Node): Parent node
    cur (int): Current position in code

Returns:
	int: Index to end of code block

Example:
    >>> builder = mc.Builder(True)
    >>> builder.load("unnamed",
    ... """for a = b
    ...   c
    ... end""")
    loading unnamed
         Program     functions.program
       0 Main        functions.main
       0 Codeblock   codeblock.codeblock 
       0   For           'for a = b' branches.forloop
       4     Var         variables.variable   'a'
       8     Expression  expression.create    'b'
       8     Var         variables.variable   'b'
      12 Codeblock   codeblock.codeblock 
      12   Statement     codeblock.codeblock  'c'
      12     Expression  expression.create    'c'
      12     Var         variables.variable   'c'
    >>> builder.configure(suggest=False)
    >>> print(mc.qtree(builder, core=True)) # doctest: +NORMALIZE_WHITESPACE
    1  1Block      code_block   TYPE
    1  1| For        code_block   TYPE
    1  5| | Var        unknown      (int)   a
    1  9| | Var        unknown      TYPE    b
    2 13| | Block      code_block   TYPE
    2 13| | | Statement  code_block   TYPE
    2 13| | | | Var        unknown      TYPE    c
    '''

    if  self.code[cur:cur+3] != "for":
        self.syntaxerror(cur, "for loop start")

    start = cur

    if self.disp:
        print("%4d   For          " % cur,)
        print(repr(self.code[cur:self.code.find("\n", cur)]),)
        print("branches.forloop")

    for_loop = mc.collection.For(parent, cur=cur, code=self.code[cur:self.code.find("\n", cur)])

    cur = cur+3
    while self.code[cur] in "( \t":
        cur += 1

    cur = self.create_variable(for_loop, cur)

    index = for_loop.parent.children.index(for_loop)
    tbb = for_loop.parent.children[index - 1].cls
    if tbb == "Tbb_for":
        for_loop[0].create_declare()
        for_loop[0].suggest = "uword"

    else:
        for_loop[0].create_declare()
        for_loop[0].suggest = "int"


    cur += 1
    while self.code[cur] in " \t":
        cur += 1

    if self.code[cur] != "=":
        self.syntaxerror(cur, "for-loop assignment (=)")
    cur += 1

    while self.code[cur] in " \t":
        cur += 1

    cur = self.create_expression(for_loop, cur)
    cur += 1

    while self.code[cur] in ") \t":
        cur += 1

    if self.code[cur] == ",":
        cur += 1

    while self.code[cur] in " \t\n;":
        cur += 1

    end = self.create_codeblock(for_loop, cur)

    #for_loop.code = self.code[start:end]

    return end


def ifbranch(self, parent, start):
    '''
If-ifelse-else branch

Args:
    self (Builder): Code constructor.
    parent (Node): Parent node
    cur (int): Current position in code

Returns:
	int: Index to end of code block

Example:
    >>> builder = mc.Builder(True)
    >>> builder.load("unnamed",
    ... """if a
    ...   b
    ... elseif c
    ...   d
    ... end""")
    loading unnamed
         Program     functions.program
       0 Main        functions.main
       0 Codeblock   codeblock.codeblock 
       0   If            branches.ifbranch    'if a'
       3     Expression  expression.create    'a'
       3     Var         variables.variable   'a'
       4 Codeblock   codeblock.codeblock 
       7   Statement     codeblock.codeblock  'b'
       7     Expression  expression.create    'b'
       7     Var         variables.variable   'b'
       9   Else if       branches.ifbranch    'elseif c'
      16     Expression  expression.create    'c'
      16     Var         variables.variable   'c'
      17 Codeblock   codeblock.codeblock 
      20   Statement     codeblock.codeblock  'd'
      20     Expression  expression.create    'd'
      20     Var         variables.variable   'd'
    >>> builder.configure()
    >>> print(mc.qtree(builder, core=True)) # doctest: +NORMALIZE_WHITESPACE
    1  1Block      code_block   TYPE
    1  1| Branch     code_block   TYPE
    1  4| | If         code_block   TYPE
    1  4| | | Var        unknown      TYPE    a
    1  5| | | Block      code_block   TYPE
    2  8| | | | Statement  code_block   TYPE
    2  8| | | | | Var        unknown      TYPE    b
    3 10| | Elif       code_block   TYPE
    3 17| | | Var        unknown      TYPE    c
    3 18| | | Block      code_block   TYPE
    4 21| | | | Statement  code_block   TYPE
    4 21| | | | | Var        unknown      TYPE    d
    '''

    if  self.code[start:start+2] != "if" or self.code[start+2] not in c.k_end:
        self.syntaxerror(start, "if branch start")

    branch = mc.collection.Branch(parent, cur=start)

    cur = start

    cur += 2
    while self.code[cur] in " \t":
        cur += 1

    if  self.code[cur] not in c.e_start:
        self.syntaxerror(cur, "expression start")

    end = findend.expression(self, cur)

    if self.disp:
        print("%4d   If           " % (start),)
        print("%-20s" % "branches.ifbranch",)
        print(repr(self.code[start:end+1]))

    node = mc.collection.If(branch, cur=cur, code=self.code[start:end+1])

    # this code below gives error if the if statement is: if (a > 1) && (a < 6)
    #because it digs down recursevly in (a > 1) and not the whole statement
    #if self.code[cur] == "(":
    #    cur += 1
    #    while self.code[cur] in " \t":
    #        cur += 1
    self.create_expression(node, cur)

    cur = end+1

    end = self.create_codeblock(node, cur)
    #node.code = self.code[cur:end]
    cur = end

    while self.code[cur:cur+6] == "elseif" and self.code[cur+6] in c.k_end:

        #node.code = self.code[start:cur]
        start = cur

        cur += 6
        while self.code[cur] in " \t":
            cur += 1

        end = findend.expression(self, cur)

        if self.disp:
            print("%4d   Else if      " % (start),)
            print("%-20s" % "branches.ifbranch",)
            print(repr(self.code[start:end+1]))

        node = mc.collection.Elif(branch, cur=start, code=self.code[start:end+1])

        #if self.code[cur] == "(":
        #    cur += 1
        #    while self.code[cur] in " \t":
        #        cur += 1

        self.create_expression(node, cur)
        cur = end+1

        cur = end = self.create_codeblock(node, cur)


    cur = end
    #node.code = self.code[start:cur]

    if self.code[cur:cur+4] == "else" and self.code[cur+4] in c.k_end:

        start = cur

        cur += 4

        if self.disp:
            print("%4d   Else         " % (start),)
            print("%-20s" % "branches.ifbranch",)
            print(repr(self.code[start:start+5]))

        node = mc.collection.Else(branch, cur=start)

        end = self.create_codeblock(node, cur)
        #node.code = self.code[start:end+1]

    branch.code = self.code[start:end+1]

    return end


if __name__ == "__main__":
    import doctest
    doctest.testmod()
