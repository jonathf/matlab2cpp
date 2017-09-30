# encoding: utf-8

"""
Interpretors that didn't fit other places
"""

import matlab2cpp as mc

from . import constants as c, findend, expression, iterate, identify


def number(self, node, start):
    """
Verbatim number

Args:
    self (Builder): Code constructor
    node (Node): Parent node
    start (int): Current position in code

Returns:
	int : End of number

Example:
    >>> builder = mc.Builder(True)
    >>> builder.load("unnamed", "42.")
    loading unnamed
         Program     functions.program
       0 Main        functions.main
       0 Codeblock   codeblock.codeblock 
       0   Statement     codeblock.codeblock  '42.'
       0     Expression  expression.create    '42.'
       0     Float       misc.number          '42.'
    >>> builder.configure()
    >>> print(mc.qtree(builder, core=True)) # doctest: +NORMALIZE_WHITESPACE
    1 1Block      code_block   TYPE
    1 1| Statement  code_block   TYPE
    1 1| | Float      double       double
    """

    if not (self.code[start] in c.digits or\
            self.code[start] == "." and self.code[start+1] in c.digits):
        self.syntaxerror(start, "number")

    k = start

    while self.code[k] in c.digits:
        k += 1
    last = k-1

    integer = True
    if self.code[k] == "." and \
      (self.code[k+1:k+3] != ".." and self.code[k+1] not in "*/"): 
        integer = False

        k += 1
        while self.code[k] in c.digits:
            k += 1
        last = k-1

    if self.code[k] in "eEdD":

        exp = k

        k = k+1
        if self.code[k] in "+-":
            k += 1

        while self.code[k] in c.digits:
            k += 1

        number = self.code[start:exp] + "e" + self.code[exp+1:k]

        last = k-1

        if self.code[k] in "ij":

            k += 1
            node = mc.collection.Imag(node, number, cur=start,
                    code=self.code[start:last+1])
            if self.disp:
                print("%4d     Imag       " % (start),)
                print("%-20s" % "misc.number",)
                print(repr(self.code[start:last+1]))

        else:
            node = mc.collection.Float(node, number, cur=start,
                    code=self.code[start:last+1])
            if self.disp:
                print("%4d     Float      " % (start),)
                print("%-20s" % "misc.number",)
                print(repr(self.code[start:last+1]))

    elif integer:

        number = self.code[start:k]

        if self.code[k] in "ij":

            node = mc.collection.Imag(node, self.code[start:k], cur=start,
                    code=self.code[start:last+1])
            k += 1
            if self.disp:
                print("%4d     Imag       " % (start),)
                print("%-20s" % "misc.number",)
                print(repr(self.code[start:last+1]))

        else:
            node = mc.collection.Int(node, self.code[start:k], cur=start,
                    code=self.code[start:last+1])
            if self.disp:
                print("%4d     Int        " % (start),)
                print("%-20s" % "misc.number",)
                print(repr(self.code[start:last+1]))

    else:

        if self.code[k] in "ij":

            node = mc.collection.Imag(node, self.code[start:k], cur=start,
                    code=self.code[start:last+1])
            k += 1
            if self.disp:
                print("%4d     Imag       " % (start),)
                print("%-20s" % "misc.number",)
                print(repr(self.code[start:last+1]))

        else:
            node = mc.collection.Float(node, self.code[start:k], cur=start,
                    code=self.code[start:k])
            if self.disp:
                print("%4d     Float      " % (start),)
                print("%-20s" % "misc.number",)
                print(repr(self.code[start:last+1]))

    return k-1


def string(self, parent, cur):
    """
Verbatim string

Args:
    self (Builder): Code constructor
    parent (Node): Parent node
    start (int): Current position in code

Returns:
	int : End of string

Example:
    >>> builder = mc.Builder(True)
    >>> builder.load("unnamed", "'abc'")
    loading unnamed
         Program     functions.program
       0 Main        functions.main
       0 Codeblock   codeblock.codeblock 
       0   Statement     codeblock.codeblock  "'abc'"
       0     String  misc.string          "'abc'"
    >>> builder.configure()
    >>> print(mc.qtree(builder, core=True)) # doctest: +NORMALIZE_WHITESPACE
    1 1Block      code_block   TYPE
    1 1| Statement  code_block   TYPE
    1 1| | String     string       string
    """

    end = findend.string(self, cur)

    if  "\n" in self.code[cur:end]:
        self.syntaxerror(cur, "no line-feed character in string")

    mc.collection.String(parent, self.code[cur+1:end], cur=cur,
            code=self.code[cur:end+1])

    if self.disp:
        print("%4d     String " % cur,)
        print("%-20s" % "misc.string",)
        print(repr(self.code[cur:end+1]))

    return end


def list(self, parent, cur):
    """
A list (both comma or space delimited)

Args:
    self (Builder): Code constructor
    parent (Node): Parent node
    cur (int): Current position in code

Returns:
	int : End of list

Example:
    >>> builder = mc.Builder(True)
    >>> builder.load("unnamed", "[2 -3]")
    loading unnamed
         Program     functions.program
       0 Main        functions.main
       0 Codeblock   codeblock.codeblock 
       0   Statement     codeblock.codeblock  '[2 -3]'
       0     Expression  expression.create    '[2 -3]'
       0     Matrix      misc.matrix          '[2 -3]'
       1     Vector      misc.matrix          '2 -3'
       1     Expression  expression.create    '2'
       1     Int         misc.number          '2'
       3     Expression  expression.create    '-3'
       4     Int         misc.number          '3'
    >>> builder.configure(suggest=False)
    >>> print(mc.qtree(builder, core=True)) # doctest: +NORMALIZE_WHITESPACE
     1  1Block      code_block   TYPE
     1  1| Statement  code_block   TYPE
     1  1| | Matrix     matrix       irowvec
     1  2| | | Vector     matrix       irowvec
     1  2| | | | Int        int          int
     1  4| | | | Neg        expression   int
     1  5| | | | | Int        int          int
    """

    if  self.code[cur] not in "({":
        self.syntaxerror(cur, "start of list character")

    end = cur
    for vector in iterate.comma_list(self, cur):
        for start,end in vector:
            self.create_expression(parent, start, end)

    end += 1
    while self.code[end] in " \t":
        end += 1

    if self.code[end] not in ")}":
        self.syntaxerror(cur, "end of list character")

    return end

def pragma_for(self, parent, cur):

    assert parent.cls == "Block"

    if self.code[cur:cur+8] != "%#PARFOR":
        self.syntaxerror(cur, "pragma_for")

    k = cur+8

    end = findend.pragma_for(self, k)

    if self.disp:
        print("%4d   Pragma_for   " % cur,)
        print("%-20s" % "misc.pragma_for",)
        print(repr(self.code[cur:end]))

    mc.collection.Pragma_for(parent, self.code[cur+1:end], cur=cur)

    return end

def comment(self, parent, cur):
    """
Comments on any form

Args:
    self (Builder): Code constructor
    parent (Node): Parent node
    cur (int): Current position in code

Returns:
	int : End of comment

Example:
    >>> builder = mc.Builder(True, comments=True)
    >>> builder.load("unnamed", "4 % comment")
    loading unnamed
         Program     functions.program
       0 Main        functions.main
       0 Codeblock   codeblock.codeblock 
       0   Statement     codeblock.codeblock  '4'
       0     Expression  expression.create    '4'
       0     Int         misc.number          '4'
       2   Comment       misc.comment         '% comment'
    >>> builder.configure(suggest=False)
    >>> print(mc.qtree(builder, core=True)) # doctest: +NORMALIZE_WHITESPACE
    1  1Block      code_block   TYPE
    1  1| Statement  code_block   TYPE
    1  1| | Int        int          int
    1  3| Ecomment   code_block   TYPE
    """

    assert parent.cls == "Block"

    if  self.code[cur] != "%":
        self.syntaxerror(cur, "comment")

    end = findend.comment(self, cur)

    if not self.comments:
        return end

    if self.disp:
        print("%4d   Comment      " % cur,)
        print("%-20s" % "misc.comment",)
        print(repr(self.code[cur:end]))

    if self.code[cur+1] == "{":
        comment = mc.collection.Bcomment(parent, self.code[cur+2:end-1], cur=cur)
    else:
        k = cur-1
        while self.code[k] in " \t":
            k -= 1
        if self.code[k] == "\n":
            comment = mc.collection.Lcomment(parent, self.code[cur+1:end], cur=cur)
        else:
            comment = mc.collection.Ecomment(parent, self.code[cur+1:end], cur=cur)

    comment.code = self.code[cur:end+1]

    return end

def verbatim(self, parent, cur):
    """
    Verbatim, indicated by _

Args:
    self (Builder): Code constructor
    parent (Node): Parent node
    cur (int): Current position in code

Returns:
	int : End of verbatim
    """
    
    assert parent.cls == "Block"

    end = findend.verbatim(self, cur)

    if self.disp:
        print("%4d   Verbatim     " % cur,)
        print("%-20s" % "misc.verbatim",)
        print(repr(self.code[cur:end+1]))

    keys = self.code[cur:end+1].split("___")
    name = keys[1]
    value = "\n".join(keys[2:])
    verbatim = mc.collection.Verbatim(parent, name, value, cur=cur,
            code=self.code[cur:end+1])

    return end    
    
def matrix(self, node, cur):
    """
Verbatim matrices

Args:
    self (Builder): Code constructor
    node (Node): Parent node
    cur (int): Current position in code

Returns:
	int : End of matrix

Example:
    >>> builder = mc.Builder(True)
    >>> builder.load("unnamed", "[[1 2] [3 4]]")
    loading unnamed
         Program     functions.program
       0 Main        functions.main
       0 Codeblock   codeblock.codeblock 
       0   Statement     codeblock.codeblock  '[[1 2] [3 4]]'
       0     Expression  expression.create    '[[1 2] [3 4]]'
       0     Matrix      misc.matrix          '[[1 2] [3 4]]'
       1     Vector      misc.matrix          '[1 2] [3 4]'
       1     Expression  expression.create    '[1 2]'
       1     Matrix      misc.matrix          '[1 2]'
       2     Vector      misc.matrix          '1 2'
       2     Expression  expression.create    '1'
       2     Int         misc.number          '1'
       4     Expression  expression.create    '2'
       4     Int         misc.number          '2'
       7     Expression  expression.create    '[3 4]'
       7     Matrix      misc.matrix          '[3 4]'
       8     Vector      misc.matrix          '3 4'
       8     Expression  expression.create    '3'
       8     Int         misc.number          '3'
      10     Expression  expression.create    '4'
      10     Int         misc.number          '4'
    >>> builder.configure(suggest=False)
    >>> print(mc.qtree(builder, core=True)) # doctest: +NORMALIZE_WHITESPACE
     1   1Block      code_block   TYPE
     1   1| Statement  code_block   TYPE
     1   1| | Matrix     matrix       irowvec
     1   2| | | Vector     matrix       irowvec
     1   2| | | | Matrix     matrix       irowvec
     1   3| | | | | Vector     matrix       irowvec
     1   3| | | | | | Int        int          int
     1   5| | | | | | Int        int          int
     1   8| | | | Matrix     matrix       irowvec
     1   9| | | | | Vector     matrix       irowvec
     1   9| | | | | | Int        int          int
     1  11| | | | | | Int        int          int
    """

    if  self.code[cur] != "[":
        self.syntaxerror(cur, "bracket start")

    end = findend.matrix(self, cur)
    if self.disp:
        print("%4d     Matrix     " % cur,)
        print("%-20s" % "misc.matrix",)
        print(repr(self.code[cur:end+1]))

    if identify.space_delimited(self, cur):
        L = iterate.space_list(self, cur)
    else:
        L = iterate.comma_list(self, cur)
    matrix = mc.collection.Matrix(node, cur=cur, code=self.code[cur:end+1])

    for array in L:

        if array:
            start = array[0][0]
            end = array[-1][-1]
        else:
            start = cur

        vector = mc.collection.Vector(matrix, cur=start,
                code=self.code[start:end+1])

        if self.disp:
            print("%4d     Vector     " % (start),)
            print("%-20s" % "misc.matrix",)
            print(repr(self.code[start:end+1]))

        for start,end in array:

            self.create_expression(vector, start, end)

    if not L:

        if self.disp:
            print("%4d     Vector     " % cur,)
            print("%-20s" % "misc.matrix",)
            print(repr(""))
        vector = mc.collection.Vector(matrix, cur=cur, code="")


    return findend.matrix(self, cur)


def cell(self, node, cur):
    """
Verbatim cells

Args:
    self (Builder): Code constructor
    node (Node): Parent node
    cur (int): Current position in code

Returns:
	int : End of cell

Example:
    >>> builder = mc.Builder(True)
    >>> builder.load("unnamed", "{1, 2}")
    loading unnamed
         Program     functions.program
       0 Main        functions.main
       0 Codeblock   codeblock.codeblock 
       0   Statement     codeblock.codeblock  '{1, 2}'
       0     Expression  expression.create    '{1, 2}'
       0     Cell        misc.cell            '{1, 2}'
       1     Expression  expression.create    '1'
       1     Int         misc.number          '1'
       4     Expression  expression.create    '2'
       4     Int         misc.number          '2'
    >>> builder.configure(suggest=False)
    >>> print(mc.qtree(builder, core=True)) # doctest: +NORMALIZE_WHITESPACE
    1 1Block      code_block   TYPE
    1 1| Statement  code_block   TYPE
    1 1| | Cell       cell         TYPE
    1 2| | | Int        int          int
    1 5| | | Int        int          int
    """

    if  self.code[cur] != "{":
        self.syntaxerror(cur, "curly braces")

    end = findend.cell(self, cur)
    if self.disp:
        print("%4d     Cell       " % cur,)
        print("%-20s" % "misc.cell",)
        print(repr(self.code[cur:end+1]))

    if identify.space_delimited(self, cur):
        L = iterate.space_list(self, cur)
    else:
        L = iterate.comma_list(self, cur)
    cell = mc.collection.Cell(node, cur=cur, code=self.code[cur:end+1])

    for array in L:

        if array:
            start = array[0][0]
            end = array[-1][-1]
        else:
            start = cur

        for start,end in array:

            self.create_expression(cell, start, end)


    return findend.cell(self, cur)


def reserved(self, node, start):
    """Reserved keywords
    """

    k = start

    l = k

    while self.code[l] not in ";\n":
        l += 1
    newline = l

    if self.disp:
        print("%4d     reserved       " % k,)
        print("%-20s" % "misc.reserved",)
        print(repr(self.code[k:newline]))

    if self.code[k:k+4] == "disp":
        statement = mc.collection.Statement(node, cur=start,
                                            code=self.code[start:newline])

        l = k+4
        while self.code[l] in " \t":
            l += 1

        if self.code[l] == "(":
            return expression.create(self, statement, k)

        k += 4
        while self.code[k] in " \t":
            k += 1

        name = ""
        if self.code[k] == "\'":
            l = findend.string(self, k)
            name = str(self.code[k+1:l])
        else:
            l = k
            while self.code[l] not in " \t\n":
                l += 1
            name = str(self.code[k:l])

        get = mc.collection.Get(statement, name="disp", cur=start, value=self.code[k:l])

        #name = str(self.code[k+1:l])
        node = mc.collection.String(get, name)
        #node.create_declare()

        while self.code[k] not in ";\n":
            k += 1


        return k


    if self.code[k:k+4] == "load":

        statement = mc.collection.Statement(node, cur=start,
                                            code=self.code[start:newline])

        l = k+4
        while self.code[l] in " \t":
            l += 1

        if self.code[l] == "(":
            return expression.create(self, statement, k)

        k += 4
        while self.code[k] in " \t\n'":
            k += 1

        l = k
        while self.code[l] not in " \t\n":
            l += 1

        get = mc.collection.Get(statement, name="load", cur=start, value=self.code[k:l])

        name = str(self.code[k:l]).split(".")[0]
        node = mc.collection.Var(get, name)
        node.create_declare()

        while self.code[k] not in ";\n":
            k += 1


        return k
    
    if self.code[k:k+4] == "hold":

        statement = mc.collection.Statement(node, cur=start,
                                            code=self.code[start:newline])
        
        l = k+4
        while self.code[l] in " \t":
            l += 1
        
        if self.code[l] == "(":
            return expression.create(self, statement, k)

        k += 4
        while self.code[k] in " \t":
            k += 1

        get = mc.collection.Get(statement, name="hold", cur=start)

        if self.code[k:k+2] == "on"  and (self.code[k+2] in c.k_end):
            mc.collection.String(get, "on")
            return k+2
    
        if self.code[k:k+3] == "off"  and (self.code[k+3] in c.k_end):
            mc.collection.String(get, "off")
            return k+3

        if self.code[k:k+3] == "all"  and (self.code[k+3] in c.k_end):
            mc.collection.String(get, "all")
            return k+3

        while self.code[k] not in ";\n":
            k += 1

        return k

    if self.code[k:k+4] == "grid":

        statement = mc.collection.Statement(node, cur=start,
                                            code=self.code[k:newline])
        
        l = k+4
        while self.code[l] in " \t":
            l += 1
            
        if self.code[l] == "(":
            return expression.create(self, statement, k)

        k += 4
        while self.code[k] in " \t":
            k += 1

        get = mc.collection.Get(statement, name="grid", cur=start)

        if self.code[k:k+2] == "on"  and (self.code[k+2] in c.k_end):
            mc.collection.String(get, "on", cur=k)
            return k+2

        if self.code[k:k+3] == "off"  and (self.code[k+3] in c.k_end):
            mc.collection.String(get, "off", cur=k)
            return k+3

        if self.code[k:k+5] == "minor"  and (self.code[k+5] in c.k_end):
            mc.collection.String(get, "minor", cur=k)
            return k+5

        while self.code[k] not in ";\n":
            k += 1

        return k
        
        
    if self.code[k:k+5] == "clear":
        pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
