"""
Interpretors that didn't fit other places
"""

import matlab2cpp
import constants as c
import findend


def number(self, node, start):

    if not (self.code[start] in c.digits or\
            self.code[start] == "." and self.code[start+1] in c.digits):
        self.syntaxerror(start, "number")

    k = start

    while self.code[k] in c.digits:
        k += 1
    last = k-1

    integer = True
    if self.code[k] == ".":
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
            node = matlab2cpp.collection.Imag(node, number, cur=start,
                    code=self.code[start:last+1])
            if self.disp:
                print "%4d     Imag       " % (start),
                print repr(self.code[start:last+1])

        else:
            node = matlab2cpp.collection.Float(node, number, cur=start,
                    code=self.code[start:last+1])
            if self.disp:
                print "%4d     Float      " % (start),
                print repr(self.code[start:last+1])

    elif integer:

        number = self.code[start:k]

        if self.code[k] in "ij":

            node = matlab2cpp.collection.Imag(node, self.code[start:k], cur=start,
                    code=self.code[start:last+1])
            k += 1
            if self.disp:
                print "%4d     Imag       " % (start),
                print repr(self.code[start:last+1])

        else:
            node = matlab2cpp.collection.Int(node, self.code[start:k], cur=start,
                    code=self.code[start:last+1])
            if self.disp:
                print "%4d     Int        " % (start),
                print repr(self.code[start:last+1])

    else:

        if self.code[k] in "ij":

            node = matlab2cpp.collection.Imag(node, self.code[start:k], cur=start,
                    code=self.code[start:last+1])
            k += 1
            if self.disp:
                print "%4d     Imag       " % (start),
                print repr(self.code[start:last+1])

        else:
            node = matlab2cpp.collection.Float(node, self.code[start:k], cur=start,
                    code=self.code[start:k])
            if self.disp:
                print "%4d     Float      " % (start),
                print repr(self.code[start:last+1])

    return k-1


def string(self, parent, cur):

    end = findend.string(self, cur)

    if  "\n" in self.code[cur:end]:
        self.syntaxerror(cur, "no line-feed character in string")

    matlab2cpp.collection.String(parent, self.code[cur+1:end], cur=cur,
            code=self.code[cur:end+1])

    if self.disp:
        print "%4d   String " % cur,
        print repr(self.code[cur:end+1])

    return end


def list(self, parent, cur):

    if  self.code[cur] not in "({":
        self.syntaxerror(cur, "start of list character")

    end = cur
    for vector in self.iterate_comma_list(cur):
        for start,end in vector:
            self.create_expression(parent, start, end)

    end += 1
    while self.code[end] in " \t":
        end += 1

    if  self.code[end] not in ")}":
        self.syntaxerror(cur, "end of list character")

    return end


def comment(self, parent, cur):

    assert parent.cls == "Block"

    if  self.code[cur] != "%":
        self.syntaxerror(cur, "comment")

    end = findend.comment(self, cur)

    if self.comments:
        return end

    if self.disp:
        print "%4d   Comment      " % cur,
        print repr(self.code[cur:end+1])

    if self.code[cur+1] == "{":
        comment = matlab2cpp.collection.Bcomment(parent, self.code[cur+2:end-1], cur=cur)
    else:
        k = cur-1
        while self.code[k] in " \t":
            k -= 1
        if self.code[k] == "\n":
            comment = matlab2cpp.collection.Lcomment(parent, self.code[cur+1:end], cur=cur)
        else:
            comment = matlab2cpp.collection.Ecomment(parent, self.code[cur+1:end], cur=cur)

    comment.code = self.code[cur:end+1]

    return end


def matrix(self, node, cur):

    if  self.code[cur] != "[":
        self.syntaxerror(cur, "bracket start")

    end = findend.matrix(self, cur)
    if self.disp:
        print "%4d     Matrix     " % cur,
        print repr(self.code[cur:end+1])

    L = self.iterate_list(cur)
    matrix = matlab2cpp.collection.Matrix(node, cur=cur, code=self.code[cur:end+1])

    for array in L:

        if array:
            start = array[0][0]
            end = array[-1][-1]
        else:
            start = cur

        vector = matlab2cpp.collection.Vector(matrix, cur=start,
                code=self.code[start:end+1])

        if self.disp:
            print "%4d     Vector     " % (start),
            print repr(self.code[start:end+1])

        for start,end in array:

            self.create_expression(vector, start, end)

    if not L:

        if self.disp:
            print "%4d     Vector     " % cur,
            print repr("")
        vector = matlab2cpp.collection.Vector(matrix, cur=cur, code="")


    return findend.matrix(self, cur)


def cell(self, node, cur):

    if  self.code[cur] != "{":
        self.syntaxerror(cur, "curly braces")

    end = findend.cell(self, cur)
    if self.disp:
        print "%4d     Cell       " % cur,
        print repr(self.code[cur:end+1])

    L = self.iterate_list(cur)
    cell = matlab2cpp.collection.Cell(node, cur=cur, code=self.code[cur:end+1])

    for array in L:

        if array:
            start = array[0][0]
            end = array[-1][-1]
        else:
            start = cur

        for start,end in array:

            self.create_expression(cell, start, end)


    return findend.cell(self, cur)


def cell_arg(self, cset, cur):

    if  self.code[cur] == "{":
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
