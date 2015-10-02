"""
Variable interpretor
"""

from matlab2cpp.node import collection as col

import constants as c
import findend


def assign(self, node, cur, end=None):

    if  self.code[cur] not in c.letters:
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
            node = col.Cset(node, name, cur=cur,
                    code=self.code[cur:end+1])

            if self.disp:
                print "%4d     Cset       " % cur,
                print repr(self.code[cur:end+1])

            n_fields = 0
            while self.code[k] == "{":

                cur = self.iterate_cell(node, k)
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
            node = col.Cvar(node, name, cur=cur,
                    code=self.code[cur:end+1])

            if self.disp:
                print "%4d     Cvar       " % cur,
                print repr(self.code[cur:end+1])

            num = 0
            while self.code[k] == "{":

                cur = self.iterate_cell(node, k)
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
                print "%4d     Sset        " %\
                        cur,
                print repr(self.code[cur:end])

            node = col.Sset(node, name, value, cur=cur,
                    code=self.code[cur:end], pointer=1)

            last = self.create_list(node, k)
            cur = end

        else:

            if self.disp:
                print "%4d     Set        " %\
                        cur,
                print repr(self.code[cur:end+1])

            node = col.Set(node, name, cur=cur,
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
                print "%4d     Nset       " % cur,
                print repr(self.code[cur:end+1])


            node = col.Nset(node, name)
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
                    print "%4d     Fset       " % cur,
                    print repr(self.code[cur:end+1])

                node = col.Fset(node, name, value=value, cur=cur,
                        code=self.code[cur:end+1])

                cur = self.create_list(node, j)

            # Fieldname of type "a.b = ..."
            else:

                if self.disp:
                    print "%4d     Fvar       " % cur,
                    print repr(self.code[cur:last+1])

                node = col.Fvar(node, name, value=value, cur=cur,
                        code=self.code[cur:last+1])

                cur = last

    # Simple variable assignment
    else:
        if self.disp:
            print "%4d     Var        " % cur,
            print repr(self.code[cur:last])


        node = col.Var(node, name, cur=cur,
                code=self.code[cur:last])

        cur = last-1

    node.create_declare()
    return cur


def variable(self, parent, cur):

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
            node = col.Cget(parent, name, cur=cur,
                    code=self.code[cur:end+1])

            if self.disp:
                print "%4d     Cget       " % cur,
                print repr(self.code[cur:end+1])

            n_fields = 0
            while self.code[k] == "{":

                cur = self.iterate_cell(node, k)
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
            node = col.Cvar(parent, name, cur=cur,
                    code=self.code[cur:end+1])

            if self.disp:
                print "%4d     Cvar       " % cur,
                print repr(self.code[cur:end+1])

            num = 0
            while self.code[k] == "{":

                cur = self.iterate_cell(node, k)
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
                print "%4d     Sget        " %\
                        cur,
                print repr(self.code[cur:end])

            node = col.Sget(parent, name, value, cur=cur,
                    code=self.code[cur:end], pointer=1)

            last = self.create_list(node, k)
            cur = end

        else:

            if self.disp:
                print "%4d     Get        " %\
                        cur,
                print repr(self.code[cur:end+1])

            node = col.Get(parent, name, cur=cur,
                    code=self.code[cur:end+1])

            last = self.create_list(node, k)
            cur = last



    elif self.code[k] == "." and self.code[k+1] not in "*/\\^'":

        k += 1

        # Fieldname of type "a.(..)"
        if self.code[k] == "(":

            end = findend.paren(self, k)

            if self.disp:
                print "%4d     Nget       " % cur,
                print repr(self.code[cur:end+1])

            k += 1

            while self.code[k] in " \t":
                k += 1

            node = col.Nget(parent, name, cur=cur,
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
                    print "%4d     Fget       " % cur,
                    print repr(self.code[cur:end+1])


                node = col.Fget(parent, name, cur=cur,
                        value=value, code=self.code[cur:end+1])

                j += 1
                while self.code[j] in " \t":
                    j += 1

                cur = self.create_expression(node, j)

                node.create_declare()

            # Fieldname of type "a.b"
            else:

                if self.disp:
                    print "%4d     Fvar       " % cur,
                    print repr(self.code[cur:last])

                node = col.Fvar(parent, name, value=value,
                        cur=cur, code=self.code[cur:last])

                cur = last-1

                node.create_declare()


    # Simple variable
    else:

        if self.disp:
            print "%4d     Var        " % cur,
            print repr(self.code[cur:last])

        node = col.Var(parent, name, cur=cur,
                code=self.code[cur:last])

        cur = last-1

    while self.code[cur] in " \t":
        cur += 1

    return cur

