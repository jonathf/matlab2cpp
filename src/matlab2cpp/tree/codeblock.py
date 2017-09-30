# encoding: utf-8

"""
The main codeblock loop
"""

import matlab2cpp as mc

from . import findend, constants as c

def codeblock(self, parent, start):
    '''
If-ifelse-else branch

Args:
    self (Builder): Code constructor
    parent (Node): Parent node
    cur (int): Current position in code

Returns:
	int: Index to end of codeblock

Example:
    >>> builder = mc.Builder(True)
    >>> builder.load("unnamed", "a; 'b'; 3")
    loading unnamed
         Program     functions.program
       0 Main        functions.main
       0 Codeblock   codeblock.codeblock 
       0   Statement     codeblock.codeblock  'a'
       0     Expression  expression.create    'a'
       0     Var         variables.variable   'a'
       3   Statement     codeblock.codeblock  "'b'"
       3     String  misc.string          "'b'"
       8   Statement     codeblock.codeblock  '3'
       8     Expression  expression.create    '3'
       8     Int         misc.number          '3'
    >>> builder.configure()
    >>> print(mc.qtree(builder, core=True)) # doctest: +NORMALIZE_WHITESPACE
    1  1Block      code_block   TYPE
    1  1| Statement  code_block   TYPE
    1  1| | Var        unknown      TYPE    a
    1  4| Statement  code_block   TYPE
    1  4| | String     string       string
    1  9| Statement  code_block   TYPE
    1  9| | Int        int          int
    '''
    cur = start
    block = mc.collection.Block(parent, cur=cur)

    if self.disp:
        print("%4d Codeblock  " % cur,)
        print("%-20s" % "codeblock.codeblock")

    is_end_terminated = False

    while True:
        #print(self.code[cur:cur+5])
        if self.code[cur] in " \t;":
            pass

        elif self.code[cur] == "\n":
            if len(self.code)-cur < 3:
                break

        #%#PARFOR token
        elif self.code[cur:cur+8] == "%#PARFOR":
            cur = self.create_pragma_parfor(block, cur)

        elif self.code[cur] == "%":
            cur = self.create_comment(block, cur)

        elif self.code[cur:cur+3] == "___":
            cur = self.create_verbatim(block, cur)

        elif self.code[cur] == "[":
            # Divide between statement and assignment
            eq_loc = findend.matrix(self, cur)+1

            while self.code[eq_loc] in " \t":
                eq_loc += 1

            if self.code[eq_loc] == "=" and self.code[eq_loc+1] != "=":
                cur = self.create_assigns(block, cur, eq_loc)

            else:
                statement = mc.collection.Statement(block, cur=cur)

                end = findend.expression(self, cur)
                if self.disp:
                    print("%4d   Statement    " % cur,)
                    print("%-20s" % "codeblock.codeblock",)
                    print(repr(self.code[cur:end+1]))

                statement.code = self.code[cur:end+1]

                cur = self.create_expression(
                        statement, cur, end=end)


        elif self.code[cur] == "'":
            end = findend.string(self, cur)
            if self.disp:
                print("%4d   Statement    " % cur,)
                print("%-20s" % "codeblock.codeblock",)
                print(repr(self.code[cur:end+1]))

            statement = mc.collection.Statement(block, cur=cur,
                    code=self.code[cur:end+1])

            cur = self.create_string(statement, cur)

        elif self.code[cur:cur+4] == "case" and self.code[cur+4] in c.k_end:
            break

        elif self.code[cur:cur+5] == "catch" and self.code[cur+5] in c.k_end:
            break

        elif self.code[cur:cur+3] == "end" and self.code[cur+3] in c.k_end:
            cur += 3
            is_end_terminated = True
            break

        elif self.code[cur:cur+4] == "else" and self.code[cur+4] in c.k_end:
            break

        elif self.code[cur:cur+6] == "elseif" and self.code[cur+6] in c.k_end:
            break

        elif self.code[cur:cur+6] == "parfor" and self.code[cur+6] in c.k_end:
            cur = self.create_parfor(block, cur)

        elif self.code[cur:cur+3] == "for" and self.code[cur+3] in c.k_end:
            cur = self.create_for(block, cur)

        elif self.code[cur:cur+8] == "function" and\
                self.code[cur+8] in c.k_end + "[":
            cur -= 1
            break

        elif self.code[cur:cur+2] == "if" and self.code[cur+2] in c.k_end:
            cur = self.create_if(block, cur)

        elif self.code[cur:cur+9] == "otherwise" and self.code[cur+9] in c.k_end:
            break

        elif self.code[cur:cur+6] == "switch" and self.code[cur+6] in c.k_end:
            cur = self.create_switch(block, cur)

        elif self.code[cur:cur+3] == "try" and self.code[cur+3] in c.k_end:
            cur = self.create_try(block, cur)

        elif self.code[cur:cur+5] == "while" and self.code[cur+5] in c.k_end:
            cur = self.create_while(block, cur)

        elif self.code[cur:cur+4] == "hold" and \
            self.code[cur+4] not in c.letters+c.digits+"_":
            cur = self.create_reserved(block, cur)

        elif self.code[cur:cur+4] == "load" and \
            self.code[cur+4] not in c.letters+c.digits+"_":
            cur = self.create_reserved(block, cur)

        elif self.code[cur:cur+4] == "disp" and \
            self.code[cur+4] not in c.letters+c.digits+"_":
            cur = self.create_reserved(block, cur)

        elif self.code[cur:cur+4] == "grid" and \
            self.code[cur+4] not in c.letters+c.digits+"_":
            cur = self.create_reserved(block, cur)

        elif self.code[cur] in c.e_start:
            j = findend.expression(self, cur)

            j += 1
            while self.code[j] in " \t":
                j += 1
            eq_loc = j

            if self.code[eq_loc] == "=": # and self.code[eq_loc+1] != "=":

                j = eq_loc +1
                while self.code[j] in " \t":
                    j += 1
                if self.code[j] == "@":
                    cur = self.create_lambda_assign(block, cur, eq_loc)
                else:
                    cur = self.create_assign(block, cur, eq_loc)

            else:
                end = findend.expression(self, cur)
                if self.disp:
                    print("%4d   Statement    " % cur,)
                    print("%-20s" % "codeblock.codeblock",)
                    print(repr(self.code[cur:end+1]))

                statement = mc.collection.Statement(block, cur=cur,
                        code=self.code[cur:end+1])

                cur = self.create_expression(statement,
                        cur, end=end)

        cur += 1

        if len(self.code)-cur<3:
            break
    block.is_end_terminated = is_end_terminated
    block.code = self.code[start:cur+1]
    return cur


if __name__ == "__main__":
    import doctest
    doctest.testmod()
