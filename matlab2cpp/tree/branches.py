"""
Iterpretors related to branches, loops and try
"""

from matlab2cpp.node import collection as col

import constants as c
import findend


def try_(self, parent, cur):

    if  self.code[cur:cur+3] != "try" or self.code[cur+3] not in c.k_end:
        self.syntaxerror(cur, "start of try-block")

    if self.disp:
        print "%4d   Try          " % cur,
        print repr(self.code[cur:cur+3])

    start = cur

    tryblock = col.Tryblock(parent, cur=cur)

    try_ = col.Try(tryblock)

    cur += 3
    while self.code[cur] in " \t\n,;":
        cur += 1

    cur = self.create_codeblock(try_, cur)

    try_.code = self.code[start:cur]

    if  self.code[cur:cur+5] != "catch" or self.code[cur+5] not in c.k_end:
        self.syntaxerror(cur, "start of catch-block")

    catch_ = col.Catch(tryblock, cur=cur)

    start_ = cur
    cur += 5
    while self.code[cur] in " \t\n,;":
        cur += 1

    cur = self.create_codeblock(catch_, cur)

    catch_.code = self.code[start_:cur]
    tryblock.code = self.code[start:cur]

    return cur


def switch(self, parent, cur):

    if  self.code[cur:cur+6] == "switch" and\
            self.code[cur+6] in " \t(":
        self.syntaxerror(cur, "start of switch branch")

    k = cur+6
    while self.code[k] in " \t":
        k += 1

    end = findend.expression(self, k)

    if self.disp:
        print "%4d   Switch       " % cur,
        print repr(self.code[cur:end+1])

    switch = col.Switch(parent, cur=cur)

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
            print "%4d   Case         " % cur,
            print repr(self.code[cur:end+1])

        case = col.Case(switch, cur=cur)

        cur = self.create_expression(case, k, end)

        k = cur+1
        while self.code[k] in " \t;,\n":
            k += 1

        k = self.create_codeblock(case, k)

    if self.code[k:k+9] == "otherwise" and self.code[k+9] in " \t(,;\n":

        cur = k

        if self.disp:
            print "%4d   Otherwise    " % cur,
            print repr(self.code[cur:cur+10])

        otherwise = col.Otherwise(switch, cur=cur)

        k += 9
        while self.code[k] in " \t\n;,":
            k += 1

        k = self.create_codeblock(otherwise, k)

    return k


def while_(self, parent, cur):

    if  self.code[cur:cur+5] != "while" and self.code[cur+5] not in c.k_end:
        self.syntaxerror(cur, "start of while-loop")
    start = cur

    k = cur+5
    while self.code[k] in " \t":
        k += 1

    end = findend.expression(self, k)

    if self.disp:
        print "%4d   While        " % cur,
        print repr(self.code[cur:end+1])

    while_ = col.While(parent, cur=cur)

    if self.code[k] == "(":
        k += 1
        while self.code[k] in " \t":
            k += 1

    cur = self.create_expression(while_, k)
    cur += 1

    cur += 1
    while self.code[cur] in " \t":
        cur += 1

    end = self.create_codeblock(while_, cur)

    while_.code = self.code[start:end+1]

    return end



def for_(self, parent, cur):

    if  self.code[cur:cur+3] != "for":
        self.syntaxerror(cur, "for loop start")

    start = cur

    if self.disp:
        print "%4d   For          " % cur,
        print repr(self.code[cur:self.code.find("\n", cur)])

    for_loop = col.For(parent, cur=cur)

    cur = cur+3
    while self.code[cur] in "( \t":
        cur += 1

    cur = self.create_variable(for_loop, cur)
    for_loop[0].create_declare()

    cur += 1
    while self.code[cur] in " \t":
        cur += 1

    if  self.code[cur] != "=":
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

    for_loop.code = self.code[start:end]

    return end


def create_if(self, parent, start):

    if  self.code[start:start+2] != "if" or self.code[start+2] not in c.k_end:
        self.syntaxerror(start, "if branch start")

    branch = col.Branch(parent, cur=start)

    cur = start

    cur += 2
    while self.code[cur] in " \t":
        cur += 1

    if  self.code[cur] not in c.e_start:
        self.syntaxerror(cur, "expression start")

    end = findend.expression(self, cur)

    if self.disp:
        print "%4d   If           " % (start),
        print repr(self.code[start:end+1])

    node = col.If(branch, cur=cur)

    if self.code[cur] == "(":
        cur += 1
        while self.code[cur] in " \t":
            cur += 1
    self.create_expression(node, cur)

    cur = end+1

    end = self.create_codeblock(node, cur)
    node.code = self.code[cur:end]
    cur = end

    while self.code[cur:cur+6] == "elseif" and self.code[cur+6] in c.k_end:

        node.code = self.code[start:cur]
        start = cur

        cur += 6
        while self.code[cur] in " \t":
            cur += 1

        end = findend.expression(self, cur)

        if self.disp:
            print "%4d   Else if      " % (start),
            print repr(self.code[start:end+1])

        node = col.Elif(branch, cur=start)

        if self.code[cur] == "(":
            cur += 1
            while self.code[cur] in " \t":
                cur += 1

        self.create_expression(node, cur)
        cur = end+1

        cur = end = self.create_codeblock(node, cur)


    cur = end
    node.code = self.code[start:cur]

    if self.code[cur:cur+4] == "else" and self.code[cur+4] in c.k_end:

        start = cur

        cur += 4

        if self.disp:
            print "%4d   Else         " % (start),
            print repr(self.code[start:start+5])

        node = col.Else(branch, cur=start)

        end = self.create_codeblock(node, cur)
        node.code = self.code[start:end+1]

    branch.code = self.code[start:end+1]

    return end

