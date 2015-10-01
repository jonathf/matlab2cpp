"""
The main codeblock loop
"""

from matlab2cpp.node import collection as col

import findend
import constants as c

def create_codeblock(self, parent, start):

    cur = start
    block = col.Block(parent, cur=cur)

    if self.disp:
        print "%4d Codeblock" % cur

    while True:

        if self.code[cur] in " \t;":
            pass

        elif self.code[cur] == "\n":
            if len(self.code)-cur < 3:
                break

        elif self.code[cur] == "%":
            cur = self.create_comment(block, cur)

        elif self.code[cur] == "[":

            # Divide between statement and assignment
            eq_loc = findend.matrix(self, cur)+1

            while self.code[eq_loc] in " \t":
                eq_loc += 1

            if self.code[eq_loc] == "=" and self.code[eq_loc+1] != "=":

                cur = self.create_assigns(block, cur, eq_loc)

            else:

                statement = col.Statement(block, cur=cur)

                end = findend.expression(self, cur)
                if self.disp:
                    print "%4d   Statement    " % cur,
                    print repr(self.code[cur:end+1])

                statement.code = self.code[cur:end+1]

                cur = self.create_expression(
                        statement, cur, end=end)


        elif self.code[cur] == "'":

            end = findend.string(self, cur)
            if self.disp:
                print "%4d   Statement    " % cur,
                print repr(self.code[cur:end+1])

            statement = col.Statement(block, cur=cur,
                    code=self.code[cur:end+1])

            cur = self.create_string(statement, cur)

        elif self.code[cur:cur+4] == "case" and self.code[cur+4] in c.k_end:
            break

        elif self.code[cur:cur+5] == "catch" and self.code[cur+5] in c.k_end:
            break

        elif self.code[cur:cur+3] == "end" and self.code[cur+3] in c.k_end:
            cur += 3
            break

        elif self.code[cur:cur+4] == "else" and self.code[cur+4] in c.k_end:
            break

        elif self.code[cur:cur+6] == "elseif" and self.code[cur+6] in c.k_end:
            break

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
                    cur = self.create_lambda(block, cur, eq_loc)
                else:
                    cur = self.create_assign(block, cur, eq_loc)

            else:
                end = findend.expression(self, cur)
                if self.disp:
                    print "%4d   Statement    " % cur,
                    print repr(self.code[cur:end+1])

                statement = col.Statement(block, cur=cur,
                        code=self.code[cur:end+1])

                cur = self.create_expression(statement,
                        cur, end=end)

        cur += 1

        if len(self.code)-cur<3:
            break

    block.code = self.code[start:cur+1]
    return cur

