"""
Variable interpretor
"""

import matlab2cpp as mc

from . import constants as c, findend, iterate


def assign(self, parent, cur, end=None):
    """
Variable left side of an assignment

Args:
    self (Builder): Code constructor
    parent (Node): Parent node
    cur (int): Current position in code

Kwargs:
    end (int, optional): End of variable

Returns:
	int : End of variable

Example:
    >>> builder = mc.Builder(True)
    >>> builder.load("unnamed", "a = 4")
    loading unnamed
         Program     functions.program
       0 Main        functions.main
       0 Codeblock   codeblock.codeblock 
       0   Assign      assign.single        'a = 4'
       0     Var         variables.assign     'a'
       4     Expression  expression.create    '4'
       4     Int         misc.number          '4'
    >>> builder.configure(suggest=False)
    >>> print(mc.qtree(builder, core=True)) # doctest: +NORMALIZE_WHITESPACE
    1 1Block      code_block   TYPE
    1 1| Assign     int          int 
    1 1| | Var        unknown      (int)   a
    1 5| | Int        int          int
    """

    if  self.code[cur] not in c.letters + '~':
        self.syntaxerror(cur, "assign variable name")


    k = cur+1
    while self.code[k] in c.letters+c.digits+"_":
        k += 1

    name = self.code[cur:k]
    last = k

    while self.code[k] in " \t":
        k += 1

    # Get value of cell
    if self.code[k] == "{":

        end = findend.cell(self, k)
        end = end+1
        while self.code[end] in " \t":
            end += 1

        if self.code[end] == "(":

            end = findend.paren(self, end)
            node = mc.collection.Cset(parent, name, cur=cur,
                    code=self.code[cur:end+1])

            if self.disp:
                print("%4d     Cset       " % cur,)
                print("%-20s" % "variables.assign",)
                print(repr(self.code[cur:end+1]))

            n_fields = 0
            while self.code[k] == "{":

                #cur = self.iterate_cell(node, k)
                cur = findend.cell(self, k)
                #cur = iterate.comma_list(node, k)

                k = cur+1
                while self.code[k] in " \t":
                    k += 1
                n_fields += 1

            while self.code[k] in " \t":
                k += 1

            if  self.code[k] != "(":
                self.syntaxerror(k, "parenthesis start")

            cur = self.create_list(node, k)

            node["n_fields"] = n_fields
            node["n_args"] = len(node) - n_fields

        else:
            end = findend.cell(self, k)
            node = mc.collection.Cvar(parent, name, cur=cur,
                    code=self.code[cur:end+1])

            if self.disp:
                print("%4d     Cvar       " % cur,)
                print("%-20s" % "variables.assign",)
                print(repr(self.code[cur:end+1]))

            num = 0
            while self.code[k] == "{":

                cur = findend.cell(self, k)
                #cur = self.iterate_cell(node, k)

                #print(node.code)
                #print(k)
                #print("\n\n")

                #l = 0
                #while node.code[l] in c.letters+c.digits+"_":
                #    l += 1

                #list = iterate.comma_list(node, l)
                #for tup in list:
                #    mc.collection.Var(node, node.code[tup[0]:tup[1]+1])

                #print(list)
                #print("LISTAT\n\n")

                k = cur+1
                while self.code[k] in " \t":
                    k += 1
                num += 1


    # Set value of array
    elif self.code[k] == "(":

        end = findend.paren(self, k)
        if self.code[end+1] == "." and self.code[end+2] in c.letters:

            start = end+2
            end += 2
            while self.code[end] in c.letters+c.digits+"_":
                end += 1
            value = self.code[start:end]

            if self.disp:
                print("%4d     Sset        " % cur)
                print("%-20s" % "variables.assign",)
                print(repr(self.code[cur:end]))

            node = mc.collection.Sset(parent, name, value, cur=cur,
                    code=self.code[cur:end], pointer=1)

            last = self.create_list(node, k)
            cur = end-1

        else:

            if self.disp:
                print("%4d     Set        " % cur)
                print("%-20s" % "variables.assign",)
                print(repr(self.code[cur:end+1]))

            node = mc.collection.Set(parent, name, cur=cur,
                    code=self.code[cur:end+1])

            last = self.create_list(node, k)
            cur = last

    elif self.code[k] == ".":

        k += 1

        # Fieldname of type "a.() = ..."
        if self.code[k] == "(":

            end = findend.paren(self, k)

            k += 1

            while self.code[k] in " \t":
                k += 1

            if self.disp:
                print("%4d     Nset       " % cur,)
                print("%-20s" % "variables.assign",)
                print(repr(self.code[cur:end+1]))


            node = mc.collection.Nset(parent, name)
            node.cur = cur
            node.code = self.code[cur:end+1]

            cur = self.create_expression(node, cur)


        elif self.code[k] in c.letters:

            j = k+1
            while self.code[j] in c.letters+c.digits+"_.":
                j += 1

            value = self.code[k:j]
            last = j-1

            while self.code[j] in " \t":
                j += 1

            # Fieldname of type "a.b(...) = ..."
            if self.code[j] == "(":

                end = findend.paren(self, j)
                if self.disp:
                    print("%4d     Fset       " % cur,)
                    print("%-20s" % "variables.assign",)
                    print(repr(self.code[cur:end+1]))

                node = mc.collection.Fset(parent, name, value=value, cur=cur,
                        code=self.code[cur:end+1])

                cur = self.create_list(node, j)

            # Fieldname of type "a.b = ..."
            else:

                if self.disp:
                    print("%4d     Fvar       " % cur,)
                    print("%-20s" % "variables.assign",)
                    print(repr(self.code[cur:last+1]))

                node = mc.collection.Fvar(parent, name, value=value, cur=cur,
                        code=self.code[cur:last+1])

                cur = last

    # Simple variable assignment
    else:
        if self.disp:
            print("%4d     Var        " % cur,)
            print("%-20s" % "variables.assign",)
            print(repr(self.code[cur:last]))


        node = mc.collection.Var(parent, name, cur=cur,
                code=self.code[cur:last])

        cur = last-1

    if name != '~':
        node.create_declare()

    return cur


def variable(self, parent, cur):
    """
Variable not on the left side of an assignment

Args:
    self (Builder): Code constructor
    node (Node): Parent node
    cur (int): Current position in code

Kwargs:
    end (int, optional): End of variable

Returns:
	int : End of variable

Example:
    >>> builder = mc.Builder(True)
    >>> builder.load("unnamed", "a")
    loading unnamed
         Program     functions.program
       0 Main        functions.main
       0 Codeblock   codeblock.codeblock 
       0   Statement     codeblock.codeblock  'a'
       0     Expression  expression.create    'a'
       0     Var         variables.variable   'a'
    >>> builder.configure()
    >>> print(mc.qtree(builder, core=True)) #doctest: +NORMALIZE_WHITESPACE
    1 1Block      code_block   TYPE
    1 1| Statement  code_block   TYPE
    1 1| | Var        unknown      TYPE    a
    """

    k = cur
    if self.code[k] == "@":
        k += 1

    if  self.code[k] not in c.letters:
        self.syntaxerror(k, "variable name")

    k += 1
    while self.code[k] in c.letters+c.digits+"_":
        k += 1

    name = self.code[cur:k]
    last = k

    while self.code[k] in " \t":
        k += 1

    # Get value of cell
    if self.code[k] == "{":

        end = findend.cell(self, k)
        end = end+1
        while self.code[end] in " \t":
            end += 1

        if self.code[end] == "(":

            end = findend.paren(self, end)
            node = mc.collection.Cget(parent, name, cur=cur,
                    code=self.code[cur:end+1])

            if self.disp:
                print("%4d     Cget       " % cur,)
                print("%-20s" % "variables.variable",)
                print(repr(self.code[cur:end+1]))

            n_fields = 0
            while self.code[k] == "{":

                cur = findend.cell(self, k)
                #cur = self.iterate_cell(node, k)
                #cur = iterate.comma_list(node, k)

                k = cur+1
                while self.code[k] in " \t":
                    k += 1
                n_fields += 1

            while self.code[k] in " \t":
                k += 1

            if  self.code[k] != "(":
                self.syntaxerror(k, "argument parenthesis")

            cur = self.create_list(node, k)

            node["n_fields"] = n_fields
            node["n_args"] = len(node) - n_fields

        else:
            end = findend.cell(self, k)
            node = mc.collection.Cvar(parent, name, cur=cur,
                    code=self.code[cur:end+1])

            if self.disp:
                print("%4d     Cvar       " % cur,)
                print("%-20s" % "variables.variable",)
                print(repr(self.code[cur:end+1]))

            num = 0
            while self.code[k] == "{":

                cur = cell_arg(self, node, k)
                k = cur+1
                while self.code[k] in " \t":
                    k += 1
                num += 1


    # Get value of array
    elif self.code[k] == "(":

        end = findend.paren(self, k)
        if self.code[end+1] == "." and self.code[end+2] in c.letters:

            start = end+2
            end += 2
            while self.code[end] in c.letters+c.digits+"_":
                end += 1
            value = self.code[start:end]

            if self.disp:
                print("%4d     Sget        " % cur,)
                print("%-20s" % "variables.variable",)
                print(repr(self.code[cur:end]))

            node = mc.collection.Sget(parent, name, value, cur=cur,
                    code=self.code[cur:end], pointer=1)

            last = self.create_list(node, k)
            cur = end

        else:

            if self.disp:
                print("%4d     Get        " % cur,)
                print("%-20s" % "variables.variable",)
                print(repr(self.code[cur:end+1]))

            node = mc.collection.Get(parent, name, cur=cur,
                    code=self.code[cur:end+1])

            last = self.create_list(node, k)
            cur = last



    elif self.code[k] == "." and self.code[k+1] not in ".*/\\^'":

        k += 1

        # Fieldname of type "a.(..)"
        if self.code[k] == "(":

            end = findend.paren(self, k)

            if self.disp:
                print("%4d     Nget       " % cur,)
                print("%-20s" % "variables.variable",)
                print(repr(self.code[cur:end+1]))

            k += 1

            while self.code[k] in " \t":
                k += 1

            node = mc.collection.Nget(parent, name, cur=cur,
                    code=self.code[cur:end+1])

            cur = self.create_expression(node, k)


        elif self.code[k] in c.letters:

            j = k+1
            while self.code[j] in c.letters+c.digits+"_":
                j += 1

            value = self.code[k:j]
            last = j

            while self.code[j] in " \t":
                j += 1

            # Fieldname of type "a.b(...)"
            if self.code[j] == "(":

                end = findend.paren(self, j)
                if self.disp:
                    print("%4d     Fget       " % cur,)
                    print("%-20s" % "variables.variable",)
                    print(repr(self.code[cur:end+1]))


                node = mc.collection.Fget(parent, name, cur=cur,
                        value=value, code=self.code[cur:end+1])

                j += 1
                while self.code[j] in " \t":
                    j += 1

                cur = self.create_expression(node, j)

                node.create_declare()

            # Fieldname of type "a.b"
            else:

                if self.disp:
                    print("%4d     Fvar       " % cur,)
                    print("%-20s" % "variables.variable",)
                    print(repr(self.code[cur:last]))

                node = mc.collection.Fvar(parent, name, value=value,
                        cur=cur, code=self.code[cur:last])

                cur = last-1

                node.create_declare()


    # Simple variable
    else:

        if self.disp:
            print("%4d     Var        " % cur,)
            print("%-20s" % "variables.variable",)
            print(repr(self.code[cur:last]))

        node = mc.collection.Var(parent, name, cur=cur,
                code=self.code[cur:last])

        cur = last-1

    while self.code[cur] in " \t":
        cur += 1

    return cur


def cell_arg(self, cset, cur):
    """
Argument of a cell call. Support function to `assign` and `variable`.

Args:
    self (Builder): Code constructor
    cset (Node): Parent node
    cur (int): Current position in code

Returns:
	int : End of argument

Example:
    >>> builder = mc.Builder(True)
    >>> builder.load("unnamed", "a{b}")
    loading unnamed
         Program     functions.program
       0 Main        functions.main
       0 Codeblock   codeblock.codeblock 
       0   Statement     codeblock.codeblock  'a{b}'
       0     Expression  expression.create    'a{b}'
       0     Cvar        variables.variable   'a{b}'
       2     Expression  expression.create    'b'
       2     Var         variables.variable   'b'
    >>> builder.configure()
    >>> print(mc.qtree(builder, core=True)) # doctest: +NORMALIZE_WHITESPACE
    1 1Block      code_block   TYPE
    1 1| Statement  code_block   TYPE
    1 1| | Cvar       cell         TYPE    a
    1 3| | | Var        unknown      TYPE    b
    """

    if self.code[cur] != "{":
        self.syntaxerror(cur, "Curly start")

    cur = cur+1

    while True:

        if self.code[cur] == "}":
            return cur

        elif self.code[cur] in c.e_start:

            cur = self.create_expression(cset, cur)

            cur += 1
            while self.code[cur] in " \t":
                cur += 1

            return cur

        elif self.code[cur] == " ":
            pass

        cur += 1


if __name__ == "__main__":
    import doctest
    doctest.testmod()
