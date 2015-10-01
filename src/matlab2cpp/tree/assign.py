from matlab2cpp.node import collection as col

import findend
import constants as c

def multi(self, parent, cur, eq_loc):

    if  self.code[cur] != "[":
        self.syntaxerror(cur, "multi-assign start")
    if  self.code[eq_loc] == "=":
        self.syntaxerror(cur, "assignment sign (=)")

    j = eq_loc+1
    while self.code[j] in " \t.":
        if self.code[j] == ".":
            j = findend.dots(self, j)+1
        else:
            j += 1
    end = findend.expression(self, j)

    if self.disp:
        print "%4d   Assigns      " %\
                cur,
        print repr(self.code[cur:end+1])

    l = self.iterate_list(cur)

    if len(l[0]) == 1:
        return self.create_assign(parent, l[0][0][0], eq_loc)

    assigns = col.Assigns(parent, cur=cur, code=self.code[cur:end+1])

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

    if  self.code[cur] not in c.letters:
        self.syntaxerror(cur, "assignment start")
    if  self.code[eq_loc] != "=":
        self.syntaxerror(cur, "assignment indicator (=)")

    j = eq_loc+1
    while self.code[j] in " \t":
        j += 1
    end = findend.expression(self, j)

    if self.disp:
        print "%4d   Assign       " %\
                cur,
        print repr(self.code[cur:end+1])

    assign = col.Assign(parent, cur=cur, code=self.code[cur:end+1])

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

