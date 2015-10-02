
from matlab2cpp.node import collection as col

import constants as c
import findend


def program(self, name):

    if self.disp:
        print "     Program"

    # Create intial nodes
    program = col.Program(self.project, name=name, cur=0, code=self.code)
    includes = col.Includes(program, value=name)
    funcs = col.Funcs(program, name=name)

    col.Inlines(program, name=name)
    col.Structs(program, name=name)
    col.Headers(program, name=name)
    col.Log(program, name=name)

    includes.include("armadillo")
    # Start processing

    cur = 0

    while True:

        if self.code[cur] in " \t;\n":
            pass

        elif self.code[cur] == "%":
            cur = findend.comment(self, cur)

        elif self.code[cur:cur+8] == "function":
            cur = self.create_function(funcs, cur)

        else:
            if self.disp:
                print "%4d Script" % cur

            self.create_main(funcs, cur)
            break

        if len(self.code)-cur<=2:
            break
        cur += 1

    includes.include("namespace_arma")

    return program


def create_function(self, parent, cur):

    if self.code[cur:cur+8] != "function":
        self.syntaxerror(cur, "function start")
    if self.code[cur+8] not in c.key_end+"[":
        self.syntaxerror(cur, "function name or return values")

    START = cur
    k = cur + 8

    while self.code[k] in " \t":
        k += 1

    if  self.code[k] not in c.letters+"[":
        self.syntaxerror(k, "function name or return values")
    start = k

    k = findend.expression(self, k)
    end = k

    k += 1
    while self.code[k] in " \t":
        k += 1

    # with return values
    if self.code[k] == "=":

        k += 1
        while self.code[k] in " \t.":
            if self.code[k:k+3] == "...":
                k = findend.dots(self, k)+1
            else:
                k += 1

        l = k
        if  self.code[l] not in c.letters:
            self.syntaxerror(l, "function name")

        while self.code[l+1] in c.letters+c.digits+"_":
            l += 1

        m = l+1

        while self.code[m] in " \t":
            m += 1

        if self.code[m] == "(":
            m = findend.paren(self, m)
        else:
            m = l

        if self.disp:
            print "%4d Function       " % cur,
            print repr(self.code[START:m+1])

        name = self.code[k:l+1]
        func = col.Func(parent, name, cur=cur)
        col.Declares(func, code="")
        returns = col.Returns(func, code=self.code[start:end+1])

        # multi-return
        if self.code[start] == "[":
            L = self.iterate_list(start)
            end = START
            for array in L:
                for s,e in array:
                    end = s

                    if self.disp:
                        print "%4d   Return       " % cur,
                        print repr(self.code[s:e+1])

                    if not any([a in c.letters+c.digits+"_@" \
                            for a in self.code[s:e+1]]):
                        self.syntaxerror(s, "return value")

                    col.Var(returns, self.code[s:e+1], cur=s,
                            code=self.code[s:e+1])

        # single return
        else:
            end = findend.expression(self, start)

            if self.disp:
                print "%4d   Return       " % cur,
                print repr(self.code[start:end+1])

            col.Var(returns, self.code[start:end+1], cur=start,
                    code=self.code[start:end+1])


        cur = l+1
        while self.code[cur] in " \t":
            cur += 1

    # No returns
    else:
        m = k
        if self.code[m] == "(":
            m = findend.paren(self, m)
        else:
            m = end


        if self.disp:
            print "%4d Function       " % cur,
            print repr(self.code[START:m+1])

        end = start+1
        while self.code[end] in c.letters+"_":
            end += 1

        name = self.code[start:end]
        func = col.Func(parent, name, cur=cur)

        col.Declares(func)
        returns = col.Returns(func)

        cur = end

    # Parameters
    params = col.Params(func, cur=cur)
    if self.code[cur] == "(":

        end = findend.paren(self, cur)
        params.code = self.code[cur+1:end]

        L = self.iterate_comma_list(cur)
        for array in L:
            for s,e in array:

                if self.disp:
                    print "%4d   Param        " % cur,
                    print repr(self.code[s:e+1])

                var = col.Var(params, self.code[s:e+1], cur=s,
                        code=self.code[s:e+1])

        cur = end

    cur += 1

    cur = self.create_codeblock(func, cur)

    if len(returns) == 1:
        func.backend = "func_return"
        func[0].backend = "func_return"
        func[1].backend = "func_return"
        func[2].backend = "func_return"
    else:
        func.backend = "func_returns"
        func[0].backend = "func_returns"
        func[1].backend = "func_returns"
        func[2].backend = "func_returns"

    # Postfix
    for var in returns:
        var.create_declare()

    end = cur
    func.code = self.code[START:end+1]

    col.Header(func.program[4], func.name)

    return cur


def create_main(self, parent, cur):
    "Create main function"

    func = col.Main(parent)

    col.Declares(func, backend="func_return")
    col.Returns(func, backend="func_return")
    col.Params(func, backend="func_return")

    return self.create_codeblock(func, cur)


def lambda_(self, node, cur, eq_loc):

    if  self.code[cur] not in c.letters:
        self.syntaxerror(cur, "anonymous function name")

    if  self.code[eq_loc] != "=":
        self.syntaxerror(cur, "anonymous function assignment (=)")

    if self.disp:
        print "%4d   Assign       " %\
                cur,
        print repr(self.code[cur:self.code.find("\n", cur)])

    assign = col.Assign(node, cur=cur, backend="func_lambda")

    self.create_assign_variable(assign, cur, eq_loc)
    assign[0].declare.type = "func_lambda"
    assign[0].type = "func_lambda"

    k = eq_loc+1
    while self.code[k] in " \t":
        k += 1

    end = self.create_lambda_func(assign, k)
    assign.code = self.code[cur:end+1]

    return end

def create_lambda_func(self, node, cur):

    if  self.code[cur] != "@":
        self.syntaxerror(cur, "anonymous function indicator (@)")

    end = cur +1
    while self.code[end] in " \t":
        end += 1

    if  self.code[end] != "(":
        self.syntaxerror(end, "anonymous function argument list")

    end = findend.paren(self, end)

    end += 1
    while self.code[end] in " \t":
        end += 1

    end = findend.expression(self, end)

    if self.disp:
        print "%4d   Lambda       " % cur,
        print repr(self.code[cur:end+1])

    if node.cls == "Assign":
        name = node[0].name
    else:
        name = "lambda"

    funcs = node.program[1]
    name = "_%s" % (name)
    if name in funcs.names:
        i = 0
        while name+"%d" % i in funcs.names:
            i += 1
        name = name + "%d" % i

    func = col.Func(funcs, name, cur=cur, code=self.code[cur:end+1])

    declares = col.Declares(func)
    returns = col.Returns(func)
    params = col.Params(func)

    k = cur+1
    while self.code[k] in " \t":
        k += 1

    if  self.code[k] != "(":
        self.syntaxerror(k, "anonymous function argument list")

    cur = self.create_list(params, k)

    cur += 1
    while self.code[cur] in " \t":
        cur += 1

    block = col.Block(func)
    assign = col.Assign(block)
    var = col.Var(assign, "_retval")

    cur = self.create_expression(assign, cur, end=end)

    for n in assign[1].flatten():
        if (n.cls in ("Get", "Cget", "Var", "Fvar", "Fget",
            "Sget")) and n.name in node.func[0].names + node.func[2].names:

            n.create_declare()


    func.backend = "func_lambda"
    returns.backend = "func_lambda"
    params.backend = "func_lambda"
    declares.backend = "func_lambda"

    var = col.Var(returns, "_retval")
    var.create_declare()

    lamb = col.Lambda(node, name)
    lamb.type = "func_lambda"

    lamb.reference = func

    return cur
