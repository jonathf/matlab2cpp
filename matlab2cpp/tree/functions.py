"""
Functions, programs and meta-nodes

Functions
~~~~~~~~~
program         The outer shell of the program
function        Explicit functions
main            Main script
lambda_         Anonymous function constructor
lambda_func     Anonymous function content
"""

import matlab2cpp
import constants as c
import findend


def program(self, name):
    """
The outer shell of the program

Args:
    self (Builder): Code constructor
    name (str): Name of the program

Returns:
	Node: The root node of the constructed node tree

Example:
    >>> builder = mc.Builder(True)
    >>> builder.load("unamed", "a")
    loading unamed
         Program     functions.program
       0 Main        functions.main
       0 Codeblock   codeblock.codeblock 
       0   Statement     codeblock.codeblock  'a'
       0     Expression  expression.create    'a'
       0     Var         variables.variable   'a'
    >>> print mc.qtree(builder)
            Program    program      TYPE    unamed
            Includes   program      TYPE    
            | Include    program      TYPE    #include <armadillo>
            | Include    program      TYPE    using namespace arma ;
      1   1 Funcs      program      TYPE    unamed
      1   1 | Main       func_common  TYPE    main
      1   1 | | Declares   func_return  TYPE    
      1   1 | | Returns    func_return  TYPE    
      1   1 | | Params     func_return  TYPE    
      1   1 | | Block      code_block   TYPE    
      1   1 | | | Statement  code_block   TYPE    
      1   1 | | | | Var        unknown      TYPE    a
            Inlines    program      TYPE    unamed
            Structs    program      TYPE    unamed
            Headers    program      TYPE    unamed
            Log        program      TYPE    unamed
    """

    if self.disp:
        print "     Program    ",
        print "functions.program"

    # Create intial nodes
    program = matlab2cpp.collection.Program(self.project, name=name, cur=0, code=self.code)
    includes = matlab2cpp.collection.Includes(program, value=name)
    funcs = matlab2cpp.collection.Funcs(program, name=name)

    matlab2cpp.collection.Inlines(program, name=name)
    matlab2cpp.collection.Structs(program, name=name)
    matlab2cpp.collection.Headers(program, name=name)
    matlab2cpp.collection.Log(program, name=name)

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
            self.create_main(funcs, cur)
            break

        if len(self.code)-cur<=2:
            break
        cur += 1

    includes.include("namespace_arma")

    return program


def function(self, parent, cur):
    """
Explicit functions

Args:
    self (Builder): Code constructor
    parent (Node): Parent node
    cur (int): Current position in code

Returns:
	int : Index to end of function

Example:
    >>> builder = mc.Builder(True)
    >>> builder.load("unnamed", "function f(); end")
    loading unnamed
         Program     functions.program
       0 Function        functions.function   'function f()'
      12 Codeblock   codeblock.codeblock 
    >>> print mc.qtree(builder, core=True)
      1   1 Funcs      program      TYPE    unnamed
      1   1 Func       func_returns TYPE    f
      1   1 | Declares   func_returns TYPE    
      1   1 | Returns    func_returns TYPE    
      1  11 | Params     func_returns TYPE    
      1  13 | Block      code_block   TYPE    
    """

    if self.code[cur:cur+8] != "function":
        self.syntaxerror(cur, "function start")
    if self.code[cur+8] not in c.k_end+"[":
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
            print "%-20s" % "functions.function",
            print repr(self.code[START:m+1])

        name = self.code[k:l+1]
        func = matlab2cpp.collection.Func(parent, name, cur=cur)
        matlab2cpp.collection.Declares(func, code="")
        returns = matlab2cpp.collection.Returns(func, code=self.code[start:end+1])

        # multi-return
        if self.code[start] == "[":
            L = self.iterate_list(start)
            end = START
            for array in L:
                for s,e in array:
                    end = s

                    if self.disp:
                        print "%4d   Return       " % cur,
                        print "%-20s" % "functions.function",
                        print repr(self.code[s:e+1])

                    if not any([a in c.letters+c.digits+"_@" \
                            for a in self.code[s:e+1]]):
                        self.syntaxerror(s, "return value")

                    matlab2cpp.collection.Var(returns, self.code[s:e+1], cur=s,
                            code=self.code[s:e+1])

        # single return
        else:
            end = findend.expression(self, start)

            if self.disp:
                print "%4d   Return       " % cur,
                print repr(self.code[start:end+1])

            matlab2cpp.collection.Var(returns, self.code[start:end+1], cur=start,
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
            print "%-20s" % "functions.function",
            print repr(self.code[START:m+1])

        end = start+1
        while self.code[end] in c.letters+"_":
            end += 1

        name = self.code[start:end]
        func = matlab2cpp.collection.Func(parent, name, cur=cur)

        matlab2cpp.collection.Declares(func)
        returns = matlab2cpp.collection.Returns(func)

        cur = end

    # Parameters
    params = matlab2cpp.collection.Params(func, cur=cur)
    if self.code[cur] == "(":

        end = findend.paren(self, cur)
        params.code = self.code[cur+1:end]

        L = self.iterate_comma_list(cur)
        for array in L:
            for s,e in array:

                if self.disp:
                    print "%4d   Param        " % cur,
                    print "%-20s" % "functions.function",
                    print repr(self.code[s:e+1])

                var = matlab2cpp.collection.Var(params, self.code[s:e+1], cur=s,
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

    matlab2cpp.collection.Header(func.program[4], func.name)

    return cur


def main(self, parent, cur):
    """
Main script

Args:
    self (Builder): Code constructor
    parent (Node): Parent node
    cur (int): Current position in code

Returns:
	int : Index to end of script

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
    >>> print mc.qtree(builder)
            Program    program      TYPE    unnamed
            Includes   program      TYPE    
            | Include    program      TYPE    #include <armadillo>
            | Include    program      TYPE    using namespace arma ;
      1   1 Funcs      program      TYPE    unnamed
      1   1 | Main       func_common  TYPE    main
      1   1 | | Declares   func_return  TYPE    
      1   1 | | Returns    func_return  TYPE    
      1   1 | | Params     func_return  TYPE    
      1   1 | | Block      code_block   TYPE    
      1   1 | | | Statement  code_block   TYPE    
      1   1 | | | | Var        unknown      TYPE    a
            Inlines    program      TYPE    unnamed
            Structs    program      TYPE    unnamed
            Headers    program      TYPE    unnamed
            Log        program      TYPE    unnamed
    """

    if self.disp:
        print "%4d Main       " % cur,
        print "functions.main"

    func = matlab2cpp.collection.Main(parent)

    matlab2cpp.collection.Declares(func, backend="func_return")
    matlab2cpp.collection.Returns(func, backend="func_return")
    matlab2cpp.collection.Params(func, backend="func_return")

    return self.create_codeblock(func, cur)


def lambda_(self, node, cur, eq_loc):
    """
Anonymous function constructor

Args:
    self (Builder): Code constructor
    parent (Node): Parent node
    cur (int): Current position in code
    eq_loc (int): location of assignment sign ('=')

Returns:
	int : Index to end of function line

Example:
    >>> builder = mc.Builder(True)
    >>> builder.load("unnamed", "f = @(x) 2*x")
    loading unnamed
         Program     functions.program
       0 Main        functions.main
       0 Codeblock   codeblock.codeblock 
       0   Assign        'f = @(x) 2*x' functions.lambda_
       0     Var         variables.assign     'f'
       4   Lambda        functions.lambda_func '@(x) 2*x'
       6     Expression  expression.create    'x'
       6     Var         variables.variable   'x'
       9     Expression  expression.create    '2*x'
       9     Expression  expression.create    '2'
       9     Int         misc.number          '2'
      11     Expression  expression.create    'x'
      11     Var         variables.variable   'x'
    >>> print mc.qtree(builder)
            Program    program      TYPE    unnamed
            Includes   program      TYPE    
            | Include    program      TYPE    #include <armadillo>
            | Include    program      TYPE    using namespace arma ;
      1   1 Funcs      program      TYPE    unnamed
      1   1 | Main       func_common  TYPE    main
      1   1 | | Declares   func_return  TYPE    
      1   1 | | | Var        unknown      func_lambda f
      1   1 | | Returns    func_return  TYPE    
      1   1 | | Params     func_return  TYPE    
      1   1 | | Block      code_block   TYPE    
      1   1 | | | Assign     func_lambda  TYPE    
      1   1 | | | | Var        unknown      func_lambda f
      1   1 | | | | Lambda     func_lambda  func_lambda _f
      1   5 | Func       func_lambda  TYPE    _f
      1   5 | | Declares   func_lambda  TYPE    
      1   5 | | | Var        unknown      TYPE    _retval
      1   5 | | Returns    func_lambda  TYPE    
      1   5 | | | Var        unknown      TYPE    _retval
      1   5 | | Params     func_lambda  TYPE    
      1   7 | | | Var        unknown      TYPE    x
      1   5 | | Block      code_block   TYPE    
      1   5 | | | Assign     unknown      TYPE    
      1   5 | | | | Var        unknown      TYPE    _retval
      1  10 | | | | Mul        expression   TYPE    
      1  10 | | | | | Int        int          int     
      1  12 | | | | | Var        unknown      TYPE    x
            Inlines    program      TYPE    unnamed
            Structs    program      TYPE    unnamed
            Headers    program      TYPE    unnamed
            Log        program      TYPE    unnamed
    """

    if  self.code[cur] not in c.letters:
        self.syntaxerror(cur, "anonymous function name")

    if  self.code[eq_loc] != "=":
        self.syntaxerror(cur, "anonymous function assignment (=)")

    if self.disp:
        print "%4d   Assign       " %\
                cur,
        print repr(self.code[cur:self.code.find("\n", cur)]),
        print "functions.lambda_"

    assign = matlab2cpp.collection.Assign(node, cur=cur, backend="func_lambda")

    self.create_assign_variable(assign, cur, eq_loc)
    assign[0].declare.type = "func_lambda"
    assign[0].type = "func_lambda"

    k = eq_loc+1
    while self.code[k] in " \t":
        k += 1

    end = self.create_lambda_func(assign, k)
    assign.code = self.code[cur:end+1]

    return end

def lambda_func(self, node, cur):
    """
Anonymous function content. Support function of `lambda_`.

Args:
    self (Builder): Code constructor
    parent (Node): Parent node
    cur (int): Current position in code

Returns:
	int : Index to end of function line
    """

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
        print "%-20s" % "functions.lambda_func",
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

    func = matlab2cpp.collection.Func(funcs, name, cur=cur, code=self.code[cur:end+1])

    declares = matlab2cpp.collection.Declares(func)
    returns = matlab2cpp.collection.Returns(func)
    params = matlab2cpp.collection.Params(func)

    k = cur+1
    while self.code[k] in " \t":
        k += 1

    if  self.code[k] != "(":
        self.syntaxerror(k, "anonymous function argument list")

    cur = self.create_list(params, k)

    cur += 1
    while self.code[cur] in " \t":
        cur += 1

    block = matlab2cpp.collection.Block(func)
    assign = matlab2cpp.collection.Assign(block)
    var = matlab2cpp.collection.Var(assign, "_retval")

    cur = self.create_expression(assign, cur, end=end)

    for n in assign[1].flatten():
        if (n.cls in ("Get", "Cget", "Var", "Fvar", "Fget",
            "Sget")) and n.name in node.func[0].names + node.func[2].names:

            n.create_declare()


    func.backend = "func_lambda"
    returns.backend = "func_lambda"
    params.backend = "func_lambda"
    declares.backend = "func_lambda"

    var = matlab2cpp.collection.Var(returns, "_retval")
    var.create_declare()

    lamb = matlab2cpp.collection.Lambda(node, name)
    lamb.type = "func_lambda"

    lamb.reference = func

    return cur

if __name__ == "__main__":
    import matlab2cpp as mc
    import doctest
    doctest.testmod()
