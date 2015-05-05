import string
import collection as col

letters = string.letters
digits = string.digits

expression_start = letters + digits + "[(~-+:@.'"
expression_end = "%])},;\n"

list_start = "[({"
list_end = "]})"

key_end = " \t(,;\n%"

prefixes = "-+~"
postfix1 = "'"
postfix2 = ".'"
operator1 = r"^\/*+:<>&|"
operator2 = (
    ".^", ".\\", "./", ".*",
    "<=", ">=", "==", "~=",
    "&&", "||")

string_prefix = " \t\n=><"

def process(text, disp=True):
    """Process raw Matlab-code and create a token tree
representation of the code.

Parameters
----------
text : str
    String of Matlab code. Unformated.
disp : bool
    Print progress to screen if True.

Returns
-------
tree : Node
    Token-tree representation of code
    """

    # Preamble

    A = text+"\n\n\n"   # Padding to avoid eol-read-errors

    def create_program():
        """Create program

Returns
-------
tree : Node
    Node representation of tree
        """

        if disp:
            print "%4d %4d Program" % (0, 0)

        # Create intial nodes
        program = col.Program()
        program.line = 0
        program.cur = 0

        program.code = A

        includes = col.Includes(program)

#          inc1 = col.Include(includes, "armadillo")
#          inc1.value = "#include <armadillo>"
#          inc1.code = ""
#  
#          inc2 = col.Include(includes, "usingarma")
#          inc2.value = "using namespace arma ;"
#          inc2.code = ""

        includes.include("armadillo")

        # Start processing

        mainblock = None
        line = 1
        cur = 0

        while True:

            if A[cur] == "\n":
                line += 1

            elif A[cur] in " \t;":
                pass

            elif A[cur] == "%":
                cur = findend_comment(cur)

            elif A[cur:cur+8] == "function":
                cur, line = create_function(program, cur, line)

            else:

                if mainblock is None:

                    if disp:
                        print "%4d %4d Function (main)" %\
                            (cur, line)

                    mainblock = create_main(program, 0, 0)

                cur, line = fill_codeblock(mainblock, cur, line)

            if len(A)-cur<=2:
                break
            cur += 1

        return program


    def create_main(program, cur, line):
        "Create main function"

        func = col.Func(program, "main")
        func.cur = cur
        func.line = line

        declares = col.Declares(func)
        returns = col.Returns(func)
        params = col.Params(func)

        func["backend"] = "func_return"
        declares["backend"] = "func_return"
        returns["backend"] = "func_return"
        params["backend"] = "func_return"

        var = col.Var(returns, "_retval")
        var.type = "int"
        var.declare()

        argc = col.Var(params, "argc")
        argc.type = "int"

        argv = col.Var(params, "argv")
        argv.type = "char"
        argv["backend"] = "char"
        argv.pointer(2)

        block = col.Block(func)
        block.cur = cur
        block.line = line

        assign = col.Assign(block)
        col.Var(assign, "_retval")
        col.Int(assign, "0")

        return block


    def create_function(program, cur, line):

        assert A[cur:cur+8] == "function"
        assert A[cur+8] in key_end+"["

        START = cur
        k = cur + 8

        while A[k] in " \t":
            k += 1

        assert A[k] in letters+"["
        start = k

        k = findend_expression(k)
        end = k

        k += 1
        while A[k] in " \t":
            k += 1

        # with return values
        if A[k] == "=":

            k += 1
            while A[k] in " \t.":
                if A[k:k+3] == "...":
                    k = findend_dots(k)+1
                else:
                    k += 1

            l = k
            assert A[l] in letters
            while A[l+1] in letters+digits+"_":
                l += 1

            m = l+1

            while A[m] in " \t":
                m += 1

            if A[m] == "(":
                m = findend_paren(m)
            else:
                m = l

            if disp:
                print "%4d %4d Function       " % (cur, line),
                print repr(A[START:m+1])

            name = A[k:l+1]
            func = col.Func(program, name)
            func.cur = cur
            func.line = line

            col.Declares(func)
            returns = col.Returns(func)

            # multi-return
            if A[start] == "[":
                L = iterate_list(start)
                end = START
                for array in L:
                    for s,e in array:
                        line += A.count("\n", end, s)
                        end = s

                        if disp:
                            print "%4d %4d   Return       " % (cur, line),
                            print repr(A[s:e+1])
                        assert all([a in letters+digits+"_@" \
                                for a in A[s:e+1]])

                        var = col.Var(returns, A[s:e+1])
                        var.cur = start
                        var.line = line
                        var.code = A[s:e+1]

            # single return
            else:
                end = findend_expression(start)

                if disp:
                    print "%4d %4d   Return       " % (cur, line),
                    print repr(A[start:end+1])

                var = col.Var(returns, A[start:end+1])
                var.cur = start
                var.line = line
                var.code = A[start:end+1]


            cur = l+1
            while A[cur] in " \t":
                cur += 1

        # No returns
        else:

            m = k
            if A[m] == "(":
                m = findend_paren(m)
            else:
                m = end


            if disp:
                print "%4d %4d Function       " % (cur, line),
                print repr(A[START:m+1])

            end = start+1
            while A[end] in letters+"_":
                end += 1

            name = A[start:end]
            func = col.Func(program, name)
            func.cur = cur
            func.line = line

            col.Declares(func)
            returns = col.Returns(func)

            cur = end

        params = col.Params(func)

        if A[cur] == "(":

            end = findend_paren(cur)
            params.cur = cur
            params.code = A[cur:end+1]

            L = iterate_comma_list(cur)
            for array in L:
                for s,e in array:

                    if disp:
                        print "%4d %4d   Param        " % (cur, line),
                        print repr(A[s:e+1])

                    var = col.Var(params, A[s:e+1])
                    var.cur = s
                    var.line = line
                    var.code = A[s:e+1]

            cur = end

        cur += 1

        block = col.Block(func)
        block.line = line+1
        block.cur = cur

        if len(returns) == 1:
            func["backend"] = "func_return"
            func[0]["backend"] = "func_return"
            func[1]["backend"] = "func_return"
            func[2]["backend"] = "func_return"
        else:
            func["backend"] = "func_returns"
            func[0]["backend"] = "func_returns"
            func[1]["backend"] = "func_returns"
            func[2]["backend"] = "func_returns"

        cur, line = fill_codeblock(block, cur, line)

        # Postfix
        for var in returns:
            var.declare()

        end = cur
        func.code = A[start:end+1]

        return cur, line


    def fill_codeblock(block, cur, line):

        assert block.parent["class"] != "Block"

        if disp:
            print "%4d %4d Codeblock" % (cur, line)

        while True:

            if A[cur] in " \t;":
                pass

            elif A[cur] == "\n":
                line += 1
                if len(A)-cur < 3:
                    return cur, line

            elif A[cur] == "%":
                cur, line = create_comment(block, cur, line)

            elif A[cur] == "[":

                # Divide beween statement and assignment
                eq_loc = findend_matrix(cur)

                while A[eq_loc] in " \t":
                    eq_loc += 1

                if A[eq_loc] == "=" and A[eq_loc+1] != "=":

                    cur, line = create_assigns(block, cur, line, eq_loc)

                else:

                    statement = col.Statement(block)
                    statement.cur = cur
                    statement.line = line

                    end = findend_expression(cur)
                    if disp:
                        print "%4d %4d   Statement    " % (cur, line),
                        print repr(A[cur:end+1])

                    statement.code = A[cur:end+1]

                    cur, line = create_expression(
                            statement, cur, line, end=end)


            elif A[cur] == "'":

                end = findend_string(cur)
                if disp:
                    print "%4d %4d   Statement    " % (cur, line),
                    print repr(A[cur:end+1])

                statement = col.Statement(block)
                statement.cur = cur
                statement.line = line
                statement.code = A[cur:end+1]

                cur, line = create_string(statement, cur, line)

            elif A[cur:cur+4] == "case" and A[cur+4] in key_end:
                return cur, line

            elif A[cur:cur+5] == "catch" and A[cur+5] in key_end:
                return cur, line

            elif A[cur:cur+3] == "end" and A[cur+3] in key_end:
                return cur+3, line

            elif A[cur:cur+4] == "else" and A[cur+4] in key_end:
                return cur, line

            elif A[cur:cur+6] == "elseif" and A[cur+6] in key_end:
                return cur, line

            elif A[cur:cur+3] == "for" and A[cur+3] in key_end:
                cur, line = create_for(block, cur, line)

            elif A[cur:cur+8] == "function" and\
                    A[cur+8] in key_end + "[":
                return cur-1, line

            elif A[cur:cur+2] == "if" and A[cur+2] in key_end:
                cur, line = create_if(block, cur, line)

            elif A[cur:cur+9] == "otherwise" and A[cur+9] in key_end:
                return cur, line

            elif A[cur:cur+6] == "switch" and A[cur+6] in key_end:
                cur, line = create_switch(block, cur, line)

            elif A[cur:cur+3] == "try" and A[cur+3] in key_end:
                cur, line = create_try(block, cur, line)

            elif A[cur:cur+5] == "while" and A[cur+5] in key_end:
                cur, line = create_while(block, cur, line)

            elif A[cur] in expression_start:
                j = findend_expression(cur)

                j += 1
                while A[j] == " ":
                    j += 1
                eq_loc = j

                if A[eq_loc] == "=": # and A[eq_loc+1] != "=":

                    j = eq_loc +1
                    while A[j] in " \t":
                        j += 1
                    if A[j] == "@":
                        cur, line = create_lambda(block, cur, line, eq_loc)
                    else:
                        cur, line = create_assign(block, cur, line, eq_loc)

                else:
                    end = findend_expression(cur)
                    if disp:
                        print "%4d %4d   Statement    " % (cur, line),
                        print repr(A[cur:end+1])

                    statement = col.Statement(block)
                    statement.cur = cur
                    statement.line = line
                    statement.code = A[cur:end+1]

                    cur, line = create_expression(statement,
                            cur, line, end=end)

            cur += 1

            if len(A)-cur<3:
                return cur, line


    def create_assigns(parent, cur, line, eq_loc):

        assert A[cur] == "["
        assert A[eq_loc] == "="

        j = eq_loc+1
        while A[j] in " \t.":
            if A[j] == ".":
                j = findend_dots(j)+1
            else:
                j += 1
        end = findend_expression(j)

        if disp:
            print "%4d %4d   Assigns      " %\
                    (cur, line),
            print repr(A[cur:end+1])

        l = iterate_list(cur)

        if len(l[0]) == 1:
            return create_assign(parent, cur, line, eq_loc)

        assigns = col.Assigns(parent)
        assigns.cur = cur
        assigns.line = line
        assigns.code = A[cur:end+1]

        for vector in l:
            for start,stop in vector:
                create_assign_variable(assigns, start, line, end=stop)

        cur = eq_loc + 1
        while A[cur] in " \t":
            cur += 1

        cur_, line =  create_expression(assigns, cur, line)

        return cur_, line


    def create_assign(parent, cur, line, eq_loc):

        assert A[cur] in letters
        assert A[eq_loc] == "="

        j = eq_loc+1
        while A[j] in " \t":
            j += 1
        end = findend_expression(j)

        if disp:
            print "%4d %4d   Assign       " %\
                    (cur, line),
            print repr(A[cur:end+1])

        assign = col.Assign(parent)
        assign.cur = cur
        assign.line = line
        assign.code = A[cur:end+1]

        cur, line = create_assign_variable(assign, cur, line, eq_loc)

        cur += 1
        while A[cur] in " \t":
            cur += 1

        assert A[cur] == "="

        k = cur+1
        while A[k] in " \t":
            k += 1

        cur_, line = create_expression(assign, k, line, end)

        assert len(assign) == 2

        return end, line



    def create_assign_variable(node, cur, line, end=None):

        assert A[cur] in letters

        k = cur+1
        while A[k] in letters+digits+"_":
            k += 1

        name = A[cur:k]
        last = k

        while A[k] in " \t":
            k += 1

        # Get value of cell
        if A[k] == "{":

            end = findend_cell(k)
            end = end+1
            while A[end] in " \t":
                end += 1

            if A[end] == "(":

                end = findend_paren(end)
                node = col.Cset(node, name)
                node.cur = cur
                node.line = line
                node.code = A[cur:end+1]

                if disp:
                    print "%4d %4d     Cset       " % (cur, line),
                    print repr(A[cur:end+1])

                n_fields = 0
                while A[k] == "{":

                    cur, line = fill_cell(node, k, line)
                    k = cur+1
                    while A[k] in " \t":
                        k += 1
                    n_fields += 1

                while A[k] in " \t":
                    k += 1

                assert A[k] == "("

                cur, line = create_list(node, k, line)

                node["n_fields"] = n_fields
                node["n_args"] = len(node) - n_fields

            else:
                end = findend_cell(k)
                node = col.Cvar(node, name)
                node.cur = cur
                node.line = line
                node.code = A[cur:end+1]

                if disp:
                    print "%4d %4d     Cvar       " % (cur, line),
                    print repr(A[cur:end+1])

                num = 0
                while A[k] == "{":

                    cur, line = fill_cell(node, k, line)
                    k = cur+1
                    while A[k] in " \t":
                        k += 1
                    num += 1


        # Set value of array
        elif A[k] == "(":

            node = col.Set(node, name)
            node.cur = cur
            node.line = line

            end = findend_paren(k)

            if disp:
                print "%4d %4d     Set        " %\
                        (cur, line),
                print repr(A[cur:end+1])

            node.code = A[cur:end+1]

            last, line = create_list(node, k, line)
            cur = last

        # Simple variable assignment
        elif A[k] == "=":

            if disp:
                print "%4d %4d     Var        " % (cur, line),
                print repr(A[cur:last])


            node = col.Var(node, name)
            node.cur = cur
            node.line = line
            node.code = A[cur:last]

            node.declare()

            cur = last-1

        elif A[k] == ".":

            k += 1

            # Fieldname of type "a.() = ..."
            if A[k] == "(":

                end = findend_paren(k)

                k += 1

                while A[k] in " \t":
                    k += 1

                if disp:
                    print "%4d %4d     Nset       " % (cur, line),
                    print repr(A[cur:end+1])


                node = col.Nset(node, name)
                node.cur = cur
                node.line = line
                node.code = A[cur:end+1]

                cur, line = create_expression(node, cur, line)


            elif A[k] in letters:

                j = k+1
                while A[j] in letters+digits+"_.":
                    j += 1

                sname = A[k:j]
                last = j-1

                while A[j] in " \t":
                    j += 1

                # Fieldname of type "a.b(...) = ..."
                if A[j] == "(":

                    end = findend_paren(j)
                    if disp:
                        print "%4d %4d     Fset       " % (cur, line),
                        print repr(A[cur:end+1])

                    node = col.Fset(node, name, sname)
                    node.cur = cur
                    node.line = line
                    node.code = A[cur:end+1]

                    cur, line = create_list(node, j, line)
#                      cur, line = create_expression(node, j+1, line,
#                              end=end)

                # Fieldname of type "a.b = ..."
                else:

                    if disp:
                        print "%4d %4d     Fvar       " % (cur, line),
                        print repr(A[cur:last+1])

                    node = col.Fvar(node, name, sname)
                    node.cur = cur
                    node.line = line
                    node.code = A[cur:last+1]

                    node.declare()

                    cur = last

        else:
            assert False, A[cur:k+10]

        return cur, line


    def fill_cell(cset, cur, line):

        assert A[cur] == "{"

        cur = cur+1

        while True:

            if A[cur] == "}":
                return cur, line

            elif A[cur] in expression_start:

                cur, line = create_expression(cset, cur, line)

                cur += 1
                while A[cur] in " \t":
                    cur += 1

                return cur, line

            elif A[cur] == " ":
                pass

            cur += 1


    def create_matrix(node, cur, line):

        assert A[cur] == "["

        end = findend_matrix(cur)
        if disp:
            print "%4s %4s     Matrix     " % (cur, line),
            print repr(A[cur:end+1])

        L = iterate_list(cur)
        matrix = col.Matrix(node)
        matrix.cur = cur
        matrix.line = line
        matrix.code = A[cur:end+1]

        inter = -1
        for array in L:

            if array:
                start = array[0][0]
                end = array[-1][-1]
            else:
                start = cur

            vector = col.Vector(matrix)
            vector.cur = start
            vector.line = line
            vector.code = A[start:end+1]

            if disp:
                print "%4s %4s     Vector     " % (start, line),
                print repr(A[start:end+1])

            for start,end in array:

                create_expression(vector, start, line, end)

                if inter != -1:
                    line += A.count("\n", inter, start)

                inter = end-1

        if not L:

            if disp:
                print "%4s %4s     Vector     " % (cur, line),
                print repr("")
            vector = col.Vector(matrix)
            vector.cur = cur
            vector.line = line
            vector.code = ""


        return findend_matrix(cur), line


    def create_for(parent, cur, line):

        assert A[cur:cur+3] == "for"

        start = cur

        if disp:
            print "%4d %4d   For          " % (cur, line),
            print repr(A[cur:A.find("\n", cur)])

        for_loop = col.For(parent)
        for_loop.cur = cur
        for_loop.line = line

        cur = cur+3
        while A[cur] in "( \t":
            cur += 1

        cur, line = create_variable(for_loop, cur, line)

        cur += 1
        while A[cur] in " \t":
            cur += 1
        assert A[cur] == "="
        cur += 1

        while A[cur] in " \t":
            cur += 1

        cur, line = create_expression(for_loop, cur, line)
        cur += 1

        while A[cur] in ") \t":
            cur += 1

        if A[cur] == ",":
            cur += 1

        while A[cur] in " \t\n;":
            if A[cur] == "\n":
                line += 1
            cur += 1

        block = col.Block(for_loop)
        block.cur = cur
        block.line = line
        end, line = fill_codeblock(block, cur, line)

        for_loop.code = A[start:end]
        block.code = A[cur:end]

        return end, line

    def create_if(parent, start, line):

        assert A[start:start+2] == "if" and A[start+2] in key_end

        branch = col.Branch(parent)
        branch.cur = start
        branch.line = line

        cur = start

        cur += 2
        while A[cur] in " \t":
            cur += 1

        assert A[cur] in expression_start
        end = findend_expression(cur)

        if disp:
            print "%4d %4d   If           " % (start, line),
            print repr(A[start:end+1])

        node = col.If(branch)
        branch.cur = start
        branch.line = line

        if A[cur] == "(":
            cur += 1
            while A[cur] in " \t":
                cur += 1
        _, line = create_expression(node, cur, line)

        node.code = A[cur:end+1]

        cur = end + 1
        block = col.Block(node)
        block.cur = cur
        block.line = line

        end, line = fill_codeblock(block, cur, line)
        block.code = A[cur:end+1]
        cur = end

        while A[cur:cur+6] == "elseif" and A[cur+6] in key_end:

            node.code = A[start:cur]
            start = cur

            cur += 6
            while A[cur] in " \t":
                cur += 1

            end = findend_expression(cur)

            if disp:
                print "%4d %4d   Else if      " % (start, line),
                print repr(A[start:end+1])

            node = col.Elif(branch)
            node.cur = start
            node.line = line

            if A[cur] == "(":
                cur += 1
                while A[cur] in " \t":
                    cur += 1

            _, line = create_expression(node, cur, line)
            cur = end+1

            block = col.Block(node)
            block.cur = cur
            block.line = line

            end, line = fill_codeblock(block, cur, line)
            block.code = A[cur:end+1]
            cur = end

        node.code = A[start:cur]

        if A[cur:cur+4] == "else" and A[cur+4] in key_end:

            start = cur

            cur += 4

            if disp:
                print "%4d %4d   Else         " % (start, line),
                print repr(A[start:start+5])

            node = col.Else(branch)
            node.cur = start
            node.line = line

            block = col.Block(node)
            block.cur = cur
            block.line = line

            end, line = fill_codeblock(block, cur, line)
            node.code = A[start:end+1]
            block.code = A[cur:end+1]

        branch.code = A[start:end+1]

        return end, line


    def create_while(parent, cur, line):

        assert A[cur:cur+5] == "while" and A[cur+5] in key_end
        start = cur

        k = cur+5
        while A[k] in " \t":
            k += 1

        end = findend_expression(k)

        if disp:
            print "%4d %4d   While        " % (cur, line),
            print repr(A[cur:end+1])

        while_ = col.While(parent)
        while_.cur = cur
        while_.line = line

        if A[k] == "(":
            k += 1
            while A[k] in " \t":
                k += 1

        cur, line = create_expression(while_, k, line)
        cur += 1

        cur += 1
        while A[cur] in " \t":
            cur += 1

        block = col.Block(while_)
        block.cur = cur
        block.line = line

        end, line = fill_codeblock(block, cur, line)

        while_.code = A[start:end+1]

        return end, line


    def create_switch(parent, cur, line):

        assert A[cur:cur+6] == "switch" and\
                A[cur+6] in " \t("

        k = cur+6
        while A[k] in " \t":
            k += 1

        end = findend_expression(k)

        if disp:
            print "%4d %4d   Switch       " % (cur, line),
            print repr(A[cur:end+1])

        switch = col.Switch(parent)
        switch.cur = cur
        switch.line = line

        create_expression(switch, k, line, end)

        k = end+1

        while A[k] in " \t\n;,":
            if A[k] == "\n":
                line += 1
            k += 1

        while A[k:k+4] == "case" and A[k+4] in " \t(":

            cur = k

            k += 4
            while A[k] in " \t":
                k += 1

            end = findend_expression(k)

            if disp:
                print "%4d %4d   Case         " % (cur, line),
                print repr(A[cur:end+1])

            case = col.Case(switch)
            case.cur = cur
            case.line = line

            cur, line = create_expression(case, k, line, end)

            k = cur+1
            while A[k] in " \t;,\n":
                if A[k] == "\n":
                    line += 1
                k += 1

            block = col.Block(case)
            block.cur = k
            block.line = line

            k, line = fill_codeblock(block, k, line)

        if A[k:k+9] == "otherwise" and A[k+9] in " \t(,;\n":

            cur = k

            if disp:
                print "%4d %4d   Otherwise    " % (cur, line),
                print repr(A[cur:cur+10])

            otherwise = col.Otherwise(switch)
            otherwise.cur = cur
            otherwise.line = line

            k += 9
            while A[k] in " \t\n;,":
                if A[k] == "\n":
                    line += 1
                k += 1

            block = col.Block(otherwise)
            block.cur = k
            block.line = line

            k, line = fill_codeblock(block, k, line)

        return k, line



    def create_try(parent, cur, line):
        assert A[cur:cur+3] == "try" and A[cur+3] in key_end

        if disp:
            print "%4d %4d   Try          " % (cur, line),
            print repr(A[cur:cur+3])

        start = cur

        tryblock = col.Tryblock(parent)
        tryblock.cur = cur
        tryblock.line = line

        try_ = col.Try(tryblock)

        cur += 3
        while A[cur] in " \t\n,;":
            if A[cur] == "\n":
                line += 1
            cur += 1

        block = col.Block(try_)
        block.cur = cur
        block.line = line
        cur, line = fill_codeblock(block, cur, line)

        try_.code = A[start:cur]

        assert A[cur:cur+5] == "catch" and A[cur+5] in key_end

        catch_ = col.Catch(tryblock)
        catch_.cur = cur
        catch_.line = line

        start_ = cur
        cur += 5
        while A[cur] in " \t\n,;":
            if A[cur] == "\n":
                line += 1
            cur += 1

        block = col.Block(catch_)
        block.cur = cur
        block.line = line
        cur, line = fill_codeblock(block, cur, line)

        catch_.code = A[start_:cur]
        tryblock.code = A[start:cur]

        return cur, line



    def create_cell(parent, cur, line):
        raise NotImplementedError

    def create_variable(parent, cur, line):

        k = cur
        if A[k] == "@":
            k += 1

        assert A[k] in letters

        k += 1
        while A[k] in letters+digits+"_":
            k += 1

        name = A[cur:k]
        last = k

        while A[k] in " \t":
            k += 1

        # Get value of cell
        if A[k] == "{":

            end = findend_cell(k)
            end = end+1
            while A[end] in " \t":
                end += 1

            if A[end] == "(":

                end = findend_paren(end)
                node = col.Cget(parent, name)
                node.cur = cur
                node.line = line
                node.code = A[cur:end+1]

                if disp:
                    print "%4d %4d     Cget       " % (cur, line),
                    print repr(A[cur:end+1])

                n_fields = 0
                while A[k] == "{":

                    cur, line = fill_cell(node, k, line)
                    k = cur+1
                    while A[k] in " \t":
                        k += 1
                    n_fields += 1

                while A[k] in " \t":
                    k += 1

                assert A[k] == "("

                cur, line = create_list(node, k, line)

                node["n_fields"] = n_fields
                node["n_args"] = len(node) - n_fields

            else:
                end = findend_cell(k)
                node = col.Cvar(parent, name)
                node.cur = cur
                node.line = line
                node.code = A[cur:end+1]

                if disp:
                    print "%4d %4d     Cvar       " % (cur, line),
                    print repr(A[cur:end+1])

                num = 0
                while A[k] == "{":

                    cur, line = fill_cell(node, k, line)
                    k = cur+1
                    while A[k] in " \t":
                        k += 1
                    num += 1


        # Get value of array
        elif A[k] == "(":

            end = findend_paren(k)

            if disp:
                print "%4d %4d     Get        " % (cur, line),
                print repr(A[cur:end+1])

            node = col.Get(parent, name)
            node.cur = cur
            node.line = line
            node.code = A[cur:end+1]

            cur, line = create_list(node, k, line)


        elif A[k] == "." and A[k+1] not in "*/\\^'":

            k += 1

            # Fieldname of type "a.(..)"
            if A[k] == "(":

                end = findend_paren(k)

                if disp:
                    print "%4d %4d     Nget       " % (cur, line),
                    print repr(A[cur:end+1])

                k += 1

                while A[k] in " \t":
                    k += 1

                node = col.Nget(parent, name)
                node.cur = cur
                node.line = line
                node.code = A[cur:end+1]

                cur, line = create_expression(node, k, line)


            elif A[k] in letters:

                j = k+1
                while A[j] in letters+digits+"_":
                    j += 1

                sname = A[k:j]
                last = j

                while A[j] in " \t":
                    j += 1

                # Fieldname of type "a.b(...)"
                if A[j] == "(":

                    end = findend_paren(j)
                    if disp:
                        print "%4d %4d     Fget       " % (cur, line),
                        print repr(A[cur:end+1])


                    node = col.Fget(parent, name, sname)
                    node.cur = cur
                    node.line = line
                    node.code = A[cur:end+1]

                    j += 1
                    while A[j] in " \t":
                        j += 1

                    cur, line = create_expression(node, j, line)

                # Fieldname of type "a.b"
                else:

                    if disp:
                        print "%4d %4d     Fvar       " % (cur, line),
                        print repr(A[cur:last])

                    node = col.Fvar(parent, name, sname)
                    node.cur = cur
                    node.line = line
                    node.code = A[cur:last]

                    cur = last-1


        # Simple variable
        else:

            if disp:
                print "%4d %4d     Var        " % (cur, line),
                print repr(A[cur:last])

            node = col.Var(parent, name)
            node.cur = cur
            node.line = line
            node.code = A[cur:last]

            cur = last-1

        while A[cur] in " \t":
            cur += 1

        return cur, line


    def create_comment(parent, cur, line):

        assert parent.cls == "Block"
        assert A[cur] == "%"

        end = findend_comment(cur)

        if disp:
            print "%4d %4d   Comment      " % (cur, line),
            print repr(A[cur:end+1])

        if A[cur+1] == "{":
            comment = col.Bcomment(parent, A[cur+2:end-1])
        else:
            k = cur-1
            while A[k] in " \t":
                k -= 1
            if A[k] == "\n":
                comment = col.Lcomment(parent, A[cur+1:end])
            else:
                comment = col.Ecomment(parent, A[cur+1:end])

        comment.cur = cur
        comment.line = line
        comment.code = A[cur:end+1]

        line += A.count("\n", cur, end+1)

        return end, line


    def create_string(parent, cur, line):

        end = findend_string(cur)
        assert "\n" not in A[cur:end]
        string = col.String(parent, A[cur+1:end])
        string.code = A[cur:end+1]

        if disp:
            print "%4d %4d   String " % (cur, line),
            print repr(A[cur:end+1])

        return end, line


    def create_list(parent, cur, line):

        assert A[cur] == "("

        end = cur+1
        for vector in iterate_comma_list(cur):
            for start,end in vector:
                _, line = create_expression(parent, start, line, end)

        end += 1
        while A[end] in " \t":
            end += 1

        assert A[end] == ")"

        return end, line



    def create_number(node, start, line):

        assert A[start] in digits or\
                A[start] == "." and A[start+1] in digits

        k = start

        while A[k] in digits:
            k += 1
        last = k-1

        integer = True
        if A[k] == ".":
            integer = False

            k += 1
            while A[k] in digits:
                k += 1
            last = k-1

        if A[k] in "eEdD":

            exp = k

            k = k+1
            if A[k] in "+-":
                k += 1

            while A[k] in digits:
                k += 1

            number = A[start:exp] + "e" + A[exp+1:k]

            last = k-1

            if A[k] in "ij":

                k += 1
                node = col.Imag(node, number)
                if disp:
                    print "%4d %4d     Imag       " % (start, line),
                    print repr(A[start:last+1])

            else:
                node = col.Float(node, number)
                if disp:
                    print "%4d %4d     Float      " % (start, line),
                    print repr(A[start:last+1])

        elif integer:

            number = A[start:k]

            if A[k] in "ij":

                k += 1
                node = col.Imag(node, A[start:k])
                if disp:
                    print "%4d %4d     Imag       " % (start, line),
                    print repr(A[start:last+1])

            else:
                node = col.Int(node, A[start:k])
                if disp:
                    print "%4d %4d     Int        " % (start, line),
                    print repr(A[start:last+1])

        else:

            if A[k] in "ij":

                node = col.Imag(node, A[start:k])
                k += 1
                if disp:
                    print "%4d %4d     Imag       " % (start, line),
                    print repr(A[start:last+1])

            else:
                node = col.Float(node, A[start:k])
                if disp:
                    print "%4d %4d     Float      " % (start, line),
                    print repr(A[start:last+1])

        node.cur = start
        node.code = A[start:last+1]
        node.line = line

        return k-1, line

    def create_lambda(node, cur, line, eq_loc):

        assert A[cur] in letters
        assert A[eq_loc] == "="

        if disp:
            print "%4d %4d   Assign       " %\
                    (cur, line),
            print repr(A[cur:A.find("\n", cur)])

        assign = col.Assign(node)
        assign.cur = cur
        assign.line = line

        _, line = create_assign_variable(assign, cur, line, eq_loc)
        assign[0].set_global_type("func_lambda")

        k = eq_loc+1
        while A[k] in " \t":
            k += 1

        line, end = create_lambda_func(assign, k, line)
        assign.code = A[cur:end+1]

        assign[0].reference = assign[1].reference

        return line, end


    def create_lambda_func(node, cur, line):

        assert A[cur] == "@"

        end = cur +1
        while A[end] in " \t":
            end += 1

        assert A[end] == "("
        end = findend_paren(end)

        end += 1
        while A[end] in " \t":
            end += 1

        end = findend_expression(end)

        if disp:
            print "%4d %4d   Lambda       " %\
                    (cur, line),
            print repr(A[cur:end+1])

        parent = node.parent
        if parent["class"] == "Assign" and parent[1] is node:
            name = parent[0]["name"]
        else:
            name = "lambda"

        program = node.program
        name = "_%s_%03d" % (name, len(program))

        func = col.Func(program, name)
        func.cur = cur
        func.line = line
        func.code = A[cur:end+1]

        declares = col.Declares(func)
        returns = col.Returns(func)
        params = col.Params(func)

        k = cur+1
        while A[k] in " \t":
            k += 1

        assert A[k] == "("

        cur, line = create_list(params, k, line)

        cur += 1
        while A[cur] in " \t":
            cur += 1

        block = col.Block(func)
        assign = col.Assign(block)
        var = col.Var(assign, "_retval")

        cur, line = create_expression(assign, cur, line, end=end)

        func["backend"] = "func_lambda"
        returns["backend"] = "func_lambda"
        params["backend"] = "func_lambda"
        declares["backend"] = "func_lambda"

        var = col.Var(returns, "_retval")
        var.declare()

        lamb = col.Lambda(node, name)
        lamb.type = "func_lambda"
#          lamb.declare()

        lamb.reference = func

        return cur, line


    def create_expression(node, start, line, end=None, start_opr=None):

        if A[start:start+3] == "...":
            start = findend_dots(start)
            start += 1
            while A[start] in " \t":
                start += 1

        if A[start] == ":":

            if disp:
                print "%4s %4s     Expression " % (start, line),
                print repr(A[start:start+1])
                print "%4s %4s     All        " % (start, line),
                print repr(A[start:start+1])

            col.All(node)
            return start, line

        if end is None:
            end = findend_expression(start)

        if disp:
            print "%4s %4s     Expression " % (start, line),
            print repr(A[start:end+1])

        assert A[start] in expression_start


        operators = [
            "||", "&&", "|", "&",
            "~=", "==", ">=", ">", "<=", "<",
            ":", "+", "-",
            ".*", "*", "./", "/", ".\\", "\\",
            ".^", "^"]

        if not (start_opr is None):
            operators = operators[operators.index(start_opr)+1:]

        for opr in operators:

            # Pre-screen
            if opr not in A[start:end+1]:
                continue

            starts = [start]
            last = start
            ends = []

            k = start
            while True:

                if A[k] == "(":
                    k = last = findend_paren(k)

                elif A[k] == "[":
                    k = last = findend_matrix(k)

                elif A[k] == "'" and is_string(k):
                    k = last = findend_string(k)

                elif opr == A[k:k+len(opr)]:

                    # no prefixes and no (scientific) numbers
                    if opr in "+-" and\
                            (A[k-1] not in letters+digits+")]}" or\
                             A[k-1] in "dDeE" and A[k+1] in digits):
                        k += 1
                        continue


                    k += len(opr)-1
                    while A[k+1] in " \t":
                        k += 1

                    # no all-operator
                    if opr == ":" and A[k+1] in ",;\n)]}":
                        k += 1
                        continue

                    starts.append(k+1)
                    ends.append(last)

                elif A[k] in letters+digits+"_":
                    last = k

                k += 1
                if k >= end:
                    ends.append(end)
                    break

            if len(ends)>1:

                node = retrieve_operator(opr)(node)
                node.cur = start
                node.line = line
                node.code = A[starts[0]:ends[-1]+1]

                for s,e in zip(starts, ends):
                    create_expression(node, s, line, e, opr)

                return end, line


        # All operators removed at this point!

        END = end

        # Prefixes
        while A[start] in "-~":

            if A[start] == "-":

                node = col.Neg(node)
                node.cur = start
                node.line = line
                node.code = A[start:end+1]

                start += 1

            if A[start] == "~":

                node = col.Not(node)
                node.cur = start
                node.line = line
                node.code = A[start:end+1]
                start += 1

            while A[start] in " \t":
                start += 1

        # Postfixes
        if A[end] == "'" and not A[start] == "'":
            if A[end-1] == ".":
                node = col.Transpose(node)
                node.cur = start
                node.line = line
                node.code = A[start:end+1]
                end -= 2
            else:
                node = col.Ctranspose(node)
                node.cur = start
                node.line = line
                node.code = A[start:end+1]
                end -= 1

            while A[end] in " \t":
                end -= 1

        # Parenthesis
        if A[start] == "(":
            assert A[end] == ")"

            node = col.Paren(node)
            node.cur = start
            node.line = line
            node.code = A[start:end+1]

            start += 1
            while A[start] in " \t":
                start += 1

            end -= 1
            while A[end] in " \t":
                end -= 1

            return create_expression(node, start, line, end)

        # Reserved keywords
        elif A[start:start+3] == "end" and\
                A[start+3] in " \t" + expression_end:
            node = col.End(node)
            node.cur = start
            node.line = line
            node.code = A[start:start+3]

        elif A[start:start+6] == "return" and A[start+6] in " ,;\n":
            node = col.Return(node)
            node.cur = start
            node.line = line
            node.code = A[start:start+6]

        elif A[start:start+5] == "break" and A[start+5] in " ,;\n":
            node = col.Break(node)
            node.cur = start
            node.line = line
            node.code = A[start:start+5]


        # Rest
        elif A[start] == "'":
#              assert is_string(start)
            assert A[end] == "'"
            assert "\n" not in A[start:end]

            string = col.String(node, A[start+1:end])
            string.cur = start
            string.line = line
            string.code = A[start:end+1]

        elif A[start] in digits or\
                A[start] == "." and A[start+1] in digits:
            cur, line = create_number(node, start, line)

        elif A[start] == "[":
            cur, line = create_matrix(node, start, line)

        elif A[start] == "{":
            cur, line = create_cell(node, start, line)

        else:
            assert A[start] in letters+"@"
            cur, line = create_variable(node, start, line)

        return END, line


    def retrieve_operator(opr):

        if opr == "^":      return col.Exp
        elif opr == ".^":   return col.Elexp
        elif opr == "\\":   return col.Rdiv
        elif opr == ".\\":  return col.Elrdiv
        elif opr == "/":    return col.Div
        elif opr == "./":   return col.Rdiv
        elif opr == "*":    return col.Mul
        elif opr == ".*":   return col.Elmul
        elif opr == "+":    return col.Plus
        elif opr == "-":    return col.Minus
        elif opr == ":":    return col.Colon
        elif opr == "<":    return col.Lt
        elif opr == "<=":   return col.Le
        elif opr == ">":    return col.Gt
        elif opr == ">=":   return col.Ge
        elif opr == "==":   return col.Eq
        elif opr == "~=":   return col.Ne
        elif opr == "&":    return col.Band
        elif opr == "|":    return col.Bor
        elif opr == "&&":   return col.Land
        elif opr == "||":   return col.Lor


    def is_space_delimited(start):
        assert A[start] == "["

        k = start+1

        k = start+1
        while A[k] in " \t":
            k += 1

        if A[k] in list_end:
            return False

        assert A[k] in expression_start

        if A[k] == "'":
            k = findend_string(k)+1

            while A[k] in " \t":
                k += 1

        while True:

            if A[k] == "(":
                k = findend_paren(k)

            elif A[k] == "[":
                k = findend_matrix(k)

            elif A[k] == "'":
                if A[k-1] in string_prefix:
                    return True

            elif A[k:k+3] == "...":
                k = findend_dots(k)

            elif A[k] in expression_end:
                if A[k] in ",;":
                    return False
                else:
                    return True


            k += 1

    def iterate_list(start):

        if is_space_delimited(start):
            return iterate_space_list(start)
        return iterate_comma_list(start)


    def iterate_comma_list(start):

        assert A[start] in list_start
        k = start+1

        while A[k] in " \t":
            k += 1

        if A[k] == "]":
            return [[]]

        starts = [[]]
        ends = [[]]
        count = False

        while True:

            if A[k:k+3] == "...":
                k = findend_dots(k)

            elif A[k] in expression_start:
                assert not count
                count = True
                end = findend_expression(k)
                starts[-1].append(k)
                ends[-1].append(end)

                k = end

            elif A[k] == ",":
                assert count
                count = False

            elif A[k] == ";":
                assert count
                starts.append([])
                ends.append([])
                count = False

            elif A[k] in list_end:
                return [zip(starts[i], ends[i])\
                        for i in xrange(len(ends))]

            k += 1

    def iterate_space_list(start):

        assert A[start] in list_start

        k = start+1

        last = start

        # Address first string occurence
        while A[k] in " \t":
            k += 1

        starts = [[k]]
        ends = [[]]

        if A[k] == "'":
            end = findend_string(k)
            ends[-1].append(end)
            k = end+1

            while A[k] in " \t":
                k += 1

            starts[-1].append(k)

        while True:

            if A[k] == "(":
                k = last = findend_paren(k)

            elif A[k] == "[":
                k = last = findend_matrix(k)

            elif A[k] == "'":
                if A[k-1] in string_prefix:
                    k = findend_string(k)
                last = k

            elif A[k:k+3] == "...":
                k = findend_dots(k)

            elif A[k] in " \t":

                while A[k] in " \t":
                    k += 1

                if A[k:k+2] in operator2:
                    k += 1

                elif A[k] in "+-":

                    if A[k+1] in expression_start:
                        ends[-1].append(last)
                        starts[-1].append(k)

                    elif A[k+1] in " \t":
                        while A[k+1] in " \t":
                            k += 1

                elif A[k] in operator1:
                    while A[k+1] in " \t":
                        k += 1

                else:
                    ends[-1].append(last)
                    starts[-1].append(k)
                continue

            elif A[k] == "\n":

                ends[-1].append(k-1)
                while A[k+1] in " \t":
                    k += 1
                starts.append([k+1])
                ends.append([])


            elif A[k] in expression_end:

                ends[-1].append(last)
                if A[k] == ",":

                    while A[k+1] in " \t":
                        k += 1
                    starts[-1].append(k+1)

                elif A[k] == ";":

                    while A[k+1] in " \t":
                        k += 1
                    ends.append([])
                    starts.append([k+1])

                else:
                    out = [zip(starts[i], ends[i])\
                            for i in xrange(len(ends))]
                    return out

            else:
                last = k

            k += 1



    def findend_expression(start):

        assert A[start] in expression_start
        k = start

        while True:

            if A[k] == "(":
                k = findend_paren(k)

            elif A[k] == "[":
                k = findend_matrix(k)

            elif A[k] == "'" and is_string(k):
                k = findend_string(k)

            elif A[k] == "{":
                k = findend_cell(k)

            elif A[k] == "=":

                if A[k+1] == "=":
                    k += 1
                else:
                    break

            elif A[k] in "><~":

                if A[k+1] == "=":
                    k += 1

            elif A[k:k+3] == "...":
                k = findend_dots(k)

            elif A[k] in expression_end:
                break

            k += 1

        k -= 1
        while A[k] in " \t":
            k -= 1

        return k


    def findend_matrix(start):
        "find index to end of matrix"

        assert A[start] == "["
        k = start+1

        if is_space_delimited(start):

            # Ignore first string occurence
            while A[k] in " \t":
                k += 1
            if A[k] == "'":
                k = findend_string(k)+1

            while True:

                if A[k] == "[":
                    k = findend_matrix(k)

                elif A[k] == "]":
                    return k

                elif A[k] == "%":
                    k = findend_comment(k)

                elif A[k] == "'" and A[k-1] in string_prefix:
                    k = findend_string(k)

                k += 1

        else:
            while True:

                if A[k] == "[":
                    k = findend_matrix(k)

                elif A[k] == "]":
                    return k

                elif A[k] == "%":
                    k = findend_comment(k)

                elif A[k] == "'" and is_string(k):
                    k = findend_string(k)

                k += 1

    def findend_string(start):
        "find index to end of string"

        assert A[start] == "'"

        k = A.find("'", start+1)
        assert k != -1

#          while A[k-1] == "\\" and A[k-2] != "\\":
#              k = A.find("'", k+1)
#              assert k != -1

        assert A.find("\n", start, k) == -1
        return k

    def findend_comment(start):
        "find index to end of comment"

        assert A[start] == "%"

        # blockcomment
        if A[start+1] == "{":
            eoc = A.find("%}", start+2)
            assert eoc>-1
            return eoc+1

        # Linecomment
        eoc = A.find("\n", start)
        assert eoc>-1
        return eoc

    def findend_dots(start):

        assert A[start:start+3] == "..."
        k = A.find("\n", start)
        assert k != -1
        return k

    def findend_paren(start):

        assert A[start] == "("

        k = start+1
        while True:

            if A[k] == "%":
                assert False

            elif A[k] == "'" and is_string(k):
                k_ = findend_string(k)
                k = k_

            elif A[k] == "[":
                k = findend_matrix(k)

            elif A[k] == "(":
                k = findend_paren(k)

            elif A[k] == ")":
                return k

            k += 1

    def findend_cell(start):
        assert A[start] == "{"

        k = start
        while True:

            if A[k] == "%":
                assert False
            elif A[k] == "'" and is_string(k):
                k = findend_string(k)
            elif A[k] == "(":
                k = findend_paren(k)
            elif A[k] == "[":
                k = findend_matrix(k)
            elif A[k] == "}":
                l = k+1
                while A[l] in " \t":
                    l += 1
                if A[l] != "{":
                    return k
                k = l

            k += 1

    def is_string(k):

        assert A[k] == "'"

        if A[k-1] == ".":
            return False

        j = k-1
        while A[j] in " \t":
            j -= 1

        if A[j] in letters+digits+")]}_":

            # special cases
            if A[j-3:j+1] == "case":
                return True

            return False

        return True


    prog = create_program()

    return prog


if __name__ == "__main__":

    test_code = """
if A
   x = a
else
   if B
      x = b
   else
       if C
          x = c
       else
          x = d
       end
   end
end

if A
    x = a
elseif B
    x = b
elseif C
    x = c
else
    x = d
end
            """
    tree = process(test_code)

#      print
#      tree.generate(False)
#      tree.configure()
#      print tree.summary()
    print tree.generate(False)
#      print test_code

