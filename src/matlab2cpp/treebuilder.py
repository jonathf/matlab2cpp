#!/usr/bin/env python
# encoding: utf-8

import string
import utils
import translations
import collection as col
import supplement

# Some code constants

letters = string.letters
digits = string.digits

expression_start = letters + digits + "[({~-+:@.'"
expression_end = "%])},;\n"

list_start = "[({"
list_end = "]})"

key_end = " \t(,;\n%"

prefixes = "-+~"
postfix1 = "'"
postfix2 = ".'"
operator1 = r"^\/*+-:<>&|"
operator2 = (
    ".^", ".\\", "./", ".*",
    "<=", ">=", "==", "~=",
    "&&", "||")

string_prefix = " \t\n=><"

class Treebuilder(object):
    """Convert Matlab-code to Tokentree"""

    def __init__(self, folder, disp=False, comments=True, suggestion=True):
        """
Args:
    code (str): string-representation of code
    disp (bool): Display output
    comments (bool): Include comments
    suggestion (bool): Fill in suggestion
        """
        self.folder = folder
        self.disp = disp
        self.comments = comments
        self.suggestion = suggestion
        self.project = col.Project()
        col.Library(self.project)
        col.Errors(self.project)

    def __getitem__(self, i):
        return self.project[i]

    def load(self, filename):

        if self.disp:
            print "loading", filename

        f = open(self.folder + filename, "rU")
        code = f.read() + "\n\n\n"
        f.close()
        self.code = code

        index = len(self.project)
        self.create_program(filename)

        nodes = utils.flatten(self.project[index], False, True, False)
        if self.disp:
            print "configuring", filename

        # Find if some names should be reserved
        unassigned = {}
        for node in nodes[::-1]:

            if node.cls not in ("Var", "Fvar", "Cvar", "Set", "Cset", "Sset",
                    "Fset", "Nset", "Get", "Cget", "Fget", "Nget", "Sget"):
                continue

            if node.name not in unassigned:
                unassigned[node.name] = True

            if node.parent.cls in ("Params", "Declares"):
                unassigned[node.name] = False

        unassigned = [k for k,v in unassigned.items() if v]

        reserved = set([])
        for i in xrange(len(unassigned)-1, -1, -1):

            if "_"+unassigned[i] in translations.reserved.reserved:
                reserved.add(unassigned.pop(i))

        for node in nodes[::-1]:
            if node.name in reserved:
                node.backend = "reserved"

        return unassigned

    def configure(self):

        nodes = utils.flatten(self.project, False, True, False)
        while True:

            for node in nodes[::-1]:

                if node.cls in ("Get", "Var"):

                    if node.type == "func_lambda":
                        node.backend = "func_lambda"
                        node.reference = node.declare.reference

                    # lambda scope
                    if node.backend == "func_lambda":
                        func = node.reference

                    # local scope
                    elif node in node.program:
                        func = node.program[node]

                    # external file in same folder
                    elif node in self.project:
                        func = self.project[node][2]

                    # external file in same folder
                    elif node.name + ".m" in self.project:
                        func = self.project[self.project.names.index(
                            node.name+".m")][2]

                    else:
                        func = None
                        node.translate_node()
                        if node.cls == "Get" and node.backend != "reserved" and\
                                node.num and node.dim<len(node):
                            node.declare.dim = len(node)

                    if not (func is None):
                        if node.backend == "func_return":
                            node.backend = func.backend
                            node.declare.type = func[1][0].type
                            params = func[2]
                            for i in xrange(len(node)):
                                params[i].suggest = node[i].type

                        elif node.backend == "func_returns":
                            node.backend = func.backend
                            params = func[2]

                            for j in xrange(len(params)):
                                params[j].suggest = node[j].type
                                node[j].suggest = params[j].type

                            if node.parent.cls == "Assigns":
                                node.parent.backend = "func_returns"

                                returns = func[1]
                                for j in xrange(len(returns)):
                                    returns[j].suggest = node.parent[j].type
                                    node.parent[j].suggest = returns[j].type

                        elif node.backend == "func_lambda":

                            node.type = func[1][0].type
                            params = func[2]
                            for i in xrange(len(node)):
                                params[i].suggest = node[i].type

                elif node.cls in ("Fvar", "Cget", "Fget", "Nget",
                        "Assigns", "Colon"):
                    node.translate_node()
                elif node.cls in ("Vector", "Matrix"):
                    node.type = [n.type for n in node]
                    node.translate_node()

                elif node.cls in ("Assign", "Assigns"):
                    if node[-1].cls == "Matrix":
                        node.backend = "matrix"
                    elif node[-1].cls == "Cell":
                        node.backend = "cell"
                    elif node[-1].backend == "func_lambda":
                        node[0].declare.reference = node[-1].declare.reference

                    if node[-1].backend == "reserved":
                        node.backend = "reserved"

                if node.type == "TYPE":

                    if node.cls not in\
                            ("Set", "Cset", "Fset", "Nset", "Sset",
                            "Get", "Cget", "Fget", "Nget", "Sget",
                            "Assign", "Assigns"):
                        node.type = [n.type for n in node]

                    if node.cls in ("Div", "Eldiv", "Rdiv", "Elrdiv"):
                        if node.num and node.mem < 2:
                            node.mem = 2

                    elif node.cls == "Fvar":
                        node.declare.type = node.type

                elif node.backend == "unknown":
                    node.backend = node.type

                # Assign suggestion
                if node.cls == "For":
                    var, range = node[:2]
                    var.suggest = "int"

                elif node.cls == "Assign" and node[0].cls != "Set":
                    if node[1].type == "func_lambda" and node[1].cls == "Get":
                        type = node.declare.reference[1][0]
                    else:
                        type = node[1].type
                    if node[1].cls == "Matrix":
                        node[0].declare.type = type
                    else:
                        node[0].suggest = type


                elif node.cls == "Neg" and node[0].mem == 0:
                    node.mem = 1

            if self.suggestion:

                complete = True
                for program in self.project[2:]:
                    types, suggestions = supplement.get_variables(program)
                    if [c for c in suggestions.values() if any(c)]:
                        supplement.set_variables(program, suggestions)
                        complete = False

                if complete:
                    return

            else:
                return

    def create_program(self, filename):
    
        if self.disp:
            print "%4d %4d Program" % (0, 0)
    
        # Create intial nodes
        program = col.Program(self.project, name=filename, line=0, cur=0, code=self.code)
        includes = col.Includes(program)
        includes.include("armadillo")
    
        col.Structs(program)
    
        # Start processing
    
        mainblock = None
        line = 1
        cur = 0
    
        while True:
    
            if self.code[cur] == "\n":
                line += 1
    
            elif self.code[cur] in " \t;":
                pass
    
            elif self.code[cur:cur+8] == "function":
                cur, line = self.create_function(program, cur, line)
    
            else:
    
                if mainblock is None:
    
                    if self.disp:
                        print "%4d %4d Function (main)" %\
                            (cur, line)
    
                    mainblock = self.create_main(program, 0, 0)
    
                cur, line = self.fill_codeblock(mainblock, cur, line)
    
            if len(self.code)-cur<=2:
                break
            cur += 1
    
        return program
    
    
    def create_main(self, program, cur, line):
        "Create main function"
    
        func = col.Func(program, "main",
                cur=cur, line=line, backend="func_return")
    
        col.Declares(func, backend="func_return")
    
        returns = col.Returns(func, backend="func_return")
        params = col.Params(func, backend="func_return")
    
        col.Var(returns, "_retval", type="int", backend="int").create_declare()
        col.Var(params, "argc", type="int", backend="int")
        col.Var(params, "argv", type="char", pointer=2, backend="char")
    
        block = col.Block(func, cur=cur, line=line)
    
        assign = col.Assign(block)
        col.Var(assign, "_retval", type="int")
        col.Int(assign, "0")
    
        return block
    
    
    def create_function(self, program, cur, line):
    
        assert self.code[cur:cur+8] == "function"
        assert self.code[cur+8] in key_end+"["
    
        START = cur
        k = cur + 8
    
        while self.code[k] in " \t":
            k += 1
    
        assert self.code[k] in letters+"["
        start = k
    
        k = self.findend_expression(k)
        end = k
    
        k += 1
        while self.code[k] in " \t":
            k += 1
    
        # with return values
        if self.code[k] == "=":
    
            k += 1
            while self.code[k] in " \t.":
                if self.code[k:k+3] == "...":
                    k = self.findend_dots(k)+1
                else:
                    k += 1
    
            l = k
            assert self.code[l] in letters
            while self.code[l+1] in letters+digits+"_":
                l += 1
    
            m = l+1
    
            while self.code[m] in " \t":
                m += 1
    
            if self.code[m] == "(":
                m = self.findend_paren(m)
            else:
                m = l
    
            if self.disp:
                print "%4d %4d Function       " % (cur, line),
                print repr(self.code[START:m+1])
    
            name = self.code[k:l+1]
            func = col.Func(program, name, cur=cur, line=line)
            col.Declares(func)
            returns = col.Returns(func)
    
            # multi-return
            if self.code[start] == "[":
                L = self.iterate_list(start)
                end = START
                for array in L:
                    for s,e in array:
                        line += self.code.count("\n", end, s)
                        end = s
    
                        if self.disp:
                            print "%4d %4d   Return       " % (cur, line),
                            print repr(self.code[s:e+1])
                        assert all([a in letters+digits+"_@" \
                                for a in self.code[s:e+1]])
    
                        col.Var(returns, self.code[s:e+1], cur=s, line=line,
                                code=self.code[s:e+1])
    
            # single return
            else:
                end = self.findend_expression(start)
    
                if self.disp:
                    print "%4d %4d   Return       " % (cur, line),
                    print repr(self.code[start:end+1])
    
                col.Var(returns, self.code[start:end+1], cur=start, line=line,
                        code=self.code[start:end+1])
    
    
            cur = l+1
            while self.code[cur] in " \t":
                cur += 1
    
        # No returns
        else:
    
            m = k
            if self.code[m] == "(":
                m = self.findend_paren(m)
            else:
                m = end
    
    
            if self.disp:
                print "%4d %4d Function       " % (cur, line),
                print repr(self.code[START:m+1])
    
            end = start+1
            while self.code[end] in letters+"_":
                end += 1
    
            name = self.code[start:end]
            func = col.Func(program, name, cur=cur, line=line)
    
            col.Declares(func)
            returns = col.Returns(func)
    
            cur = end
    
        params = col.Params(func, cur=cur)
    
        if self.code[cur] == "(":
    
            end = self.findend_paren(cur)
            params.code = self.code[cur:end+1]
    
            L = self.iterate_comma_list(cur)
            for array in L:
                for s,e in array:
    
                    if self.disp:
                        print "%4d %4d   Param        " % (cur, line),
                        print repr(self.code[s:e+1])
    
                    var = col.Var(params, self.code[s:e+1], cur=s, line=line,
                            code=self.code[s:e+1])
    
            cur = end
    
        cur += 1
    
        block = col.Block(func, line=line, cur=cur)
    
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
    
        cur, line = self.fill_codeblock(block, cur, line)
    
        # Postfix
        for var in returns:
            var.create_declare()
    
        end = cur
        func.code = self.code[start:end+1]
    
        return cur, line
    
    
    def fill_codeblock(self, block, cur, line):
    
        assert block.cls == "Block"
    
        if self.disp:
            print "%4d %4d Codeblock" % (cur, line)
    
        while True:
    
            if self.code[cur] in " \t;":
                pass
    
            elif self.code[cur] == "\n":
                line += 1
                if len(self.code)-cur < 3:
                    return cur, line
    
            elif self.code[cur] == "%":
                cur, line = self.create_comment(block, cur, line)
    
            elif self.code[cur] == "[":
    
                # Divide beween statement and assignment
                eq_loc = self.findend_matrix(cur)+1
    
                while self.code[eq_loc] in " \t":
                    eq_loc += 1
    
                if self.code[eq_loc] == "=" and self.code[eq_loc+1] != "=":
    
                    cur, line = self.create_assigns(block, cur, line, eq_loc)
    
                else:
    
                    statement = col.Statement(block, cur=cur, line=line)
    
                    end = self.findend_expression(cur)
                    if self.disp:
                        print "%4d %4d   Statement    " % (cur, line),
                        print repr(self.code[cur:end+1])
    
                    statement.code = self.code[cur:end+1]
    
                    cur, line = self.create_expression(
                            statement, cur, line, end=end)
    
    
            elif self.code[cur] == "'":
    
                end = self.findend_string(cur)
                if self.disp:
                    print "%4d %4d   Statement    " % (cur, line),
                    print repr(self.code[cur:end+1])
    
                statement = col.Statement(block, cur=cur, line=line,
                        code=self.code[cur:end+1])
    
                cur, line = self.create_string(statement, cur, line)
    
            elif self.code[cur:cur+4] == "case" and self.code[cur+4] in key_end:
                return cur, line
    
            elif self.code[cur:cur+5] == "catch" and self.code[cur+5] in key_end:
                return cur, line
    
            elif self.code[cur:cur+3] == "end" and self.code[cur+3] in key_end:
                return cur+3, line
    
            elif self.code[cur:cur+4] == "else" and self.code[cur+4] in key_end:
                return cur, line
    
            elif self.code[cur:cur+6] == "elseif" and self.code[cur+6] in key_end:
                return cur, line
    
            elif self.code[cur:cur+3] == "for" and self.code[cur+3] in key_end:
                cur, line = self.create_for(block, cur, line)
    
            elif self.code[cur:cur+8] == "function" and\
                    self.code[cur+8] in key_end + "[":
                return cur-1, line
    
            elif self.code[cur:cur+2] == "if" and self.code[cur+2] in key_end:
                cur, line = self.create_if(block, cur, line)
    
            elif self.code[cur:cur+9] == "otherwise" and self.code[cur+9] in key_end:
                return cur, line
    
            elif self.code[cur:cur+6] == "switch" and self.code[cur+6] in key_end:
                cur, line = self.create_switch(block, cur, line)
    
            elif self.code[cur:cur+3] == "try" and self.code[cur+3] in key_end:
                cur, line = self.create_try(block, cur, line)
    
            elif self.code[cur:cur+5] == "while" and self.code[cur+5] in key_end:
                cur, line = self.create_while(block, cur, line)
    
            elif self.code[cur] in expression_start:
                j = self.findend_expression(cur)
    
                j += 1
                while self.code[j] in " \t":
                    j += 1
                eq_loc = j
    
                if self.code[eq_loc] == "=": # and self.code[eq_loc+1] != "=":
    
                    j = eq_loc +1
                    while self.code[j] in " \t":
                        j += 1
                    if self.code[j] == "@":
                        cur, line = self.create_lambda(block, cur, line, eq_loc)
                    else:
                        cur, line = self.create_assign(block, cur, line, eq_loc)
    
                else:
                    end = self.findend_expression(cur)
                    if self.disp:
                        print "%4d %4d   Statement    " % (cur, line),
                        print repr(self.code[cur:end+1])
    
                    statement = col.Statement(block, cur=cur, line=line,
                            code=self.code[cur:end+1])
    
                    cur, line = self.create_expression(statement,
                            cur, line, end=end)
    
            cur += 1
    
            if len(self.code)-cur<3:
                return cur, line
    
    
    def create_assigns(self, parent, cur, line, eq_loc):
    
        assert self.code[cur] == "["
        assert self.code[eq_loc] == "="
    
        j = eq_loc+1
        while self.code[j] in " \t.":
            if self.code[j] == ".":
                j = self.findend_dots(j)+1
            else:
                j += 1
        end = self.findend_expression(j)
    
        if self.disp:
            print "%4d %4d   Assigns      " %\
                    (cur, line),
            print repr(self.code[cur:end+1])
    
        l = self.iterate_list(cur)
    
        if len(l[0]) == 1:
            return self.create_assign(parent, l[0][0][0], line, eq_loc)
    
        assigns = col.Assigns(parent, cur=cur, line=line, code=self.code[cur:end+1])
    
        for vector in l:
            for start,stop in vector:
                self.create_assign_variable(assigns, start, line, end=stop)
    
        cur = eq_loc + 1
        while self.code[cur] in " \t":
            cur += 1
    
        cur_, line =  self.create_expression(assigns, cur, line)
    
        assigns["name"] = assigns[-1]["name"]
    
        return cur_, line
    
    
    def create_assign(self, parent, cur, line, eq_loc):
    
        assert self.code[cur] in letters
        assert self.code[eq_loc] == "="
    
        j = eq_loc+1
        while self.code[j] in " \t":
            j += 1
        end = self.findend_expression(j)
    
        if self.disp:
            print "%4d %4d   Assign       " %\
                    (cur, line),
            print repr(self.code[cur:end+1])
    
        assign = col.Assign(parent, cur=cur, line=line, code=self.code[cur:end+1])
    
        cur, line = self.create_assign_variable(assign, cur, line, eq_loc)
    
        cur += 1
        while self.code[cur] in " \t":
            cur += 1
        
        if self.code[cur] == "]":
            cur += 1
            while self.code[cur] in " \t":
                cur += 1
    
        assert self.code[cur] == "="
    
        k = cur+1
        while self.code[k] in " \t":
            k += 1
    
        cur_, line = self.create_expression(assign, k, line, end)
        assign["name"] = assign[-1]["name"]
    
        assert len(assign) == 2
    
        return end, line
    
    
    
    def create_assign_variable(self, node, cur, line, end=None):
    
        assert self.code[cur] in letters
    
        k = cur+1
        while self.code[k] in letters+digits+"_":
            k += 1
    
        name = self.code[cur:k]
        last = k
    
        while self.code[k] in " \t":
            k += 1
    
        # Get value of cell
        if self.code[k] == "{":
    
            end = self.findend_cell(k)
            end = end+1
            while self.code[end] in " \t":
                end += 1
    
            if self.code[end] == "(":
    
                end = self.findend_paren(end)
                node = col.Cset(node, name, cur=cur, line=line,
                        code=self.code[cur:end+1])
    
                if self.disp:
                    print "%4d %4d     Cset       " % (cur, line),
                    print repr(self.code[cur:end+1])
    
                n_fields = 0
                while self.code[k] == "{":
    
                    cur, line = self.fill_cell(node, k, line)
                    k = cur+1
                    while self.code[k] in " \t":
                        k += 1
                    n_fields += 1
    
                while self.code[k] in " \t":
                    k += 1
    
                assert self.code[k] == "("
    
                cur, line = self.create_list(node, k, line)
    
                node["n_fields"] = n_fields
                node["n_args"] = len(node) - n_fields
    
            else:
                end = self.findend_cell(k)
                node = col.Cvar(node, name, cur=cur, line=line,
                        code=self.code[cur:end+1])
    
                if self.disp:
                    print "%4d %4d     Cvar       " % (cur, line),
                    print repr(self.code[cur:end+1])
    
                num = 0
                while self.code[k] == "{":
    
                    cur, line = self.fill_cell(node, k, line)
                    k = cur+1
                    while self.code[k] in " \t":
                        k += 1
                    num += 1
    
    
        # Set value of array
        elif self.code[k] == "(":

            end = self.findend_paren(k)
            if self.code[end+1] == "." and self.code[end+2] in letters:

                start = end+2
                end += 2
                while self.code[end] in letters+digits+"_":
                    end += 1
                value = self.code[start:end]

                if self.disp:
                    print "%4d %4d     Sset        " %\
                            (cur, line),
                    print repr(self.code[cur:end])

                    node = col.Sset(node, name, value, cur=cur, line=line,
                            code=self.code[cur:end], pointer=1)

                last, line = self.create_list(node, k, line)
                cur = end

            else:
        
                if self.disp:
                    print "%4d %4d     Set        " %\
                            (cur, line),
                    print repr(self.code[cur:end+1])
        
                node = col.Set(node, name, cur=cur, line=line,
                        code=self.code[cur:end+1])
        
                last, line = self.create_list(node, k, line)
                cur = last
    
        elif self.code[k] == ".":
    
            k += 1
    
            # Fieldname of type "a.() = ..."
            if self.code[k] == "(":
    
                end = self.findend_paren(k)
    
                k += 1
    
                while self.code[k] in " \t":
                    k += 1
    
                if self.disp:
                    print "%4d %4d     Nset       " % (cur, line),
                    print repr(self.code[cur:end+1])
    
    
                node = col.Nset(node, name)
                node.cur = cur
                node.line = line
                node.code = self.code[cur:end+1]
    
                cur, line = self.create_expression(node, cur, line)
    
    
            elif self.code[k] in letters:
    
                j = k+1
                while self.code[j] in letters+digits+"_.":
                    j += 1
    
                value = self.code[k:j]
                last = j-1
    
                while self.code[j] in " \t":
                    j += 1
    
                # Fieldname of type "a.b(...) = ..."
                if self.code[j] == "(":
    
                    end = self.findend_paren(j)
                    if self.disp:
                        print "%4d %4d     Fset       " % (cur, line),
                        print repr(self.code[cur:end+1])
    
                    node = col.Fset(node, name, value=value, cur=cur, line=line,
                            code=self.code[cur:end+1])
    
                    cur, line = self.create_list(node, j, line)
    
                # Fieldname of type "a.b = ..."
                else:
    
                    if self.disp:
                        print "%4d %4d     Fvar       " % (cur, line),
                        print repr(self.code[cur:last+1])
    
                    node = col.Fvar(node, name, value=value, cur=cur, line=line,
                            code=self.code[cur:last+1])
    
                    cur = last
    
        # Simple variable assignment
        else:
            if self.disp:
                print "%4d %4d     Var        " % (cur, line),
                print repr(self.code[cur:last])
    
    
            node = col.Var(node, name, line=line, cur=cur,
                    code=self.code[cur:last])
    
            cur = last-1
    
        node.create_declare()
        return cur, line
    
    
    def fill_cell(self, cset, cur, line):
    
        assert self.code[cur] == "{"
    
        cur = cur+1
    
        while True:
    
            if self.code[cur] == "}":
                return cur, line
    
            elif self.code[cur] in expression_start:
    
                cur, line = self.create_expression(cset, cur, line)
    
                cur += 1
                while self.code[cur] in " \t":
                    cur += 1
    
                return cur, line
    
            elif self.code[cur] == " ":
                pass
    
            cur += 1
    
    
    def create_matrix(self, node, cur, line):
    
        assert self.code[cur] == "["
    
        end = self.findend_matrix(cur)
        if self.disp:
            print "%4s %4s     Matrix     " % (cur, line),
            print repr(self.code[cur:end+1])
    
        L = self.iterate_list(cur)
        matrix = col.Matrix(node, cur=cur, line=line, code=self.code[cur:end+1])
    
        inter = -1
        for array in L:
    
            if array:
                start = array[0][0]
                end = array[-1][-1]
            else:
                start = cur
    
            vector = col.Vector(matrix, cur=start, line=line,
                    code=self.code[start:end+1])
    
            if self.disp:
                print "%4s %4s     Vector     " % (start, line),
                print repr(self.code[start:end+1])
    
            for start,end in array:
    
                self.create_expression(vector, start, line, end)
    
                if inter != -1:
                    line += self.code.count("\n", inter, start)
    
                inter = end-1
    
        if not L:
    
            if self.disp:
                print "%4s %4s     Vector     " % (cur, line),
                print repr("")
            vector = col.Vector(matrix, cur=cur, line=line, code="")
    
    
        return self.findend_matrix(cur), line
    
    
    def create_for(self, parent, cur, line):
    
        assert self.code[cur:cur+3] == "for"
    
        start = cur
    
        if self.disp:
            print "%4d %4d   For          " % (cur, line),
            print repr(self.code[cur:self.code.find("\n", cur)])
    
        for_loop = col.For(parent, cur=cur, line=line)
    
        cur = cur+3
        while self.code[cur] in "( \t":
            cur += 1
    
        cur, line = self.create_variable(for_loop, cur, line)
    
        cur += 1
        while self.code[cur] in " \t":
            cur += 1
        assert self.code[cur] == "="
        cur += 1
    
        while self.code[cur] in " \t":
            cur += 1
    
        cur, line = self.create_expression(for_loop, cur, line)
        cur += 1
    
        while self.code[cur] in ") \t":
            cur += 1
    
        if self.code[cur] == ",":
            cur += 1
    
        while self.code[cur] in " \t\n;":
            if self.code[cur] == "\n":
                line += 1
            cur += 1
    
        block = col.Block(for_loop, cur=cur, line=line)
        end, line = self.fill_codeblock(block, cur, line)
    
        for_loop.code = self.code[start:end]
        block.code = self.code[cur:end]
    
        return end, line
    
    def create_if(self, parent, start, line):
    
        assert self.code[start:start+2] == "if" and self.code[start+2] in key_end
    
        branch = col.Branch(parent, cur=start, line=line)
    
        cur = start
    
        cur += 2
        while self.code[cur] in " \t":
            cur += 1
    
        assert self.code[cur] in expression_start
        end = self.findend_expression(cur)
    
        if self.disp:
            print "%4d %4d   If           " % (start, line),
            print repr(self.code[start:end+1])
    
        node = col.If(branch, cur=cur, line=line)
    
        if self.code[cur] == "(":
            cur += 1
            while self.code[cur] in " \t":
                cur += 1
        _, line = self.create_expression(node, cur, line)
    
        node.code = self.code[cur:end+1]
    
        cur = end + 1
        block = col.Block(node, cur=cur, line=line)
    
        end, line = self.fill_codeblock(block, cur, line)
        block.code = self.code[cur:end+1]
        cur = end
    
        while self.code[cur:cur+6] == "elseif" and self.code[cur+6] in key_end:
    
            node.code = self.code[start:cur]
            start = cur
    
            cur += 6
            while self.code[cur] in " \t":
                cur += 1
    
            end = self.findend_expression(cur)
    
            if self.disp:
                print "%4d %4d   Else if      " % (start, line),
                print repr(self.code[start:end+1])
    
            node = col.Elif(branch, cur=start, line=line)
    
            if self.code[cur] == "(":
                cur += 1
                while self.code[cur] in " \t":
                    cur += 1
    
            _, line = self.create_expression(node, cur, line)
            cur = end+1
    
            block = col.Block(node, cur=cur, line=line)
    
            end, line = self.fill_codeblock(block, cur, line)
            block.code = self.code[cur:end+1]
            cur = end
    
        node.code = self.code[start:cur]
    
        if self.code[cur:cur+4] == "else" and self.code[cur+4] in key_end:
    
            start = cur
    
            cur += 4
    
            if self.disp:
                print "%4d %4d   Else         " % (start, line),
                print repr(self.code[start:start+5])
    
            node = col.Else(branch, cur=start, line=line)
    
            block = col.Block(node, cur=cur, line=line)
    
            end, line = self.fill_codeblock(block, cur, line)
            node.code = self.code[start:end+1]
            block.code = self.code[cur:end+1]
    
        branch.code = self.code[start:end+1]
    
        return end, line
    
    
    def create_while(self, parent, cur, line):
    
        assert self.code[cur:cur+5] == "while" and self.code[cur+5] in key_end
        start = cur
    
        k = cur+5
        while self.code[k] in " \t":
            k += 1
    
        end = self.findend_expression(k)
    
        if self.disp:
            print "%4d %4d   While        " % (cur, line),
            print repr(self.code[cur:end+1])
    
        while_ = col.While(parent, cur=cur, line=line)
    
        if self.code[k] == "(":
            k += 1
            while self.code[k] in " \t":
                k += 1
    
        cur, line = self.create_expression(while_, k, line)
        cur += 1
    
        cur += 1
        while self.code[cur] in " \t":
            cur += 1
    
        block = col.Block(while_, cur=cur, line=line)
    
        end, line = self.fill_codeblock(block, cur, line)
    
        while_.code = self.code[start:end+1]
    
        return end, line
    
    
    def create_switch(self, parent, cur, line):
    
        assert self.code[cur:cur+6] == "switch" and\
                self.code[cur+6] in " \t("
    
        k = cur+6
        while self.code[k] in " \t":
            k += 1
    
        end = self.findend_expression(k)
    
        if self.disp:
            print "%4d %4d   Switch       " % (cur, line),
            print repr(self.code[cur:end+1])
    
        switch = col.Switch(parent, cur=cur, line=line)
    
        self.create_expression(switch, k, line, end)
    
        k = end+1
    
        while self.code[k] in " \t\n;,":
            if self.code[k] == "\n":
                line += 1
            k += 1
    
        while self.code[k:k+4] == "case" and self.code[k+4] in " \t(":
    
            cur = k
    
            k += 4
            while self.code[k] in " \t":
                k += 1
    
            end = self.findend_expression(k)
    
            if self.disp:
                print "%4d %4d   Case         " % (cur, line),
                print repr(self.code[cur:end+1])
    
            case = col.Case(switch, cur=cur, line=line)
    
            cur, line = self.create_expression(case, k, line, end)
    
            k = cur+1
            while self.code[k] in " \t;,\n":
                if self.code[k] == "\n":
                    line += 1
                k += 1
    
            block = col.Block(case, cur=k, line=line)
    
            k, line = self.fill_codeblock(block, k, line)
    
        if self.code[k:k+9] == "otherwise" and self.code[k+9] in " \t(,;\n":
    
            cur = k
    
            if self.disp:
                print "%4d %4d   Otherwise    " % (cur, line),
                print repr(self.code[cur:cur+10])
    
            otherwise = col.Otherwise(switch, cur=cur, line=line)
    
            k += 9
            while self.code[k] in " \t\n;,":
                if self.code[k] == "\n":
                    line += 1
                k += 1
    
            block = col.Block(otherwise, cur=k, line=line)
    
            k, line = self.fill_codeblock(block, k, line)
    
        return k, line
    
    
    
    def create_try(self, parent, cur, line):
        assert self.code[cur:cur+3] == "try" and self.code[cur+3] in key_end
    
        if self.disp:
            print "%4d %4d   Try          " % (cur, line),
            print repr(self.code[cur:cur+3])
    
        start = cur
    
        tryblock = col.Tryblock(parent, cur=cur, line=line)
    
        try_ = col.Try(tryblock)
    
        cur += 3
        while self.code[cur] in " \t\n,;":
            if self.code[cur] == "\n":
                line += 1
            cur += 1
    
        block = col.Block(try_, cur=cur, line=line)
        cur, line = self.fill_codeblock(block, cur, line)
    
        try_.code = self.code[start:cur]
    
        assert self.code[cur:cur+5] == "catch" and self.code[cur+5] in key_end
    
        catch_ = col.Catch(tryblock, cur=cur, line=line)
    
        start_ = cur
        cur += 5
        while self.code[cur] in " \t\n,;":
            if self.code[cur] == "\n":
                line += 1
            cur += 1
    
        block = col.Block(catch_, cur=cur, line=line)
        cur, line = self.fill_codeblock(block, cur, line)
    
        catch_.code = self.code[start_:cur]
        tryblock.code = self.code[start:cur]
    
        return cur, line
    
    
    
    def create_cell(self, node, cur, line):
        assert self.code[cur] == "{"
    
        end = self.findend_cell(cur)
        if self.disp:
            print "%4s %4s     Cell       " % (cur, line),
            print repr(self.code[cur:end+1])
    
        L = self.iterate_list(cur)
        cell = col.Cell(node, cur=cur, line=line, code=self.code[cur:end+1])
    
        inter = -1
        for array in L:
    
            if array:
                start = array[0][0]
                end = array[-1][-1]
            else:
                start = cur
    
            for start,end in array:
    
                self.create_expression(cell, start, line, end)
    
                if inter != -1:
                    line += self.code.count("\n", inter, start)
    
                inter = end-1
    
        return self.findend_cell(cur), line
    
    
    def create_variable(self, parent, cur, line):
    
        k = cur
        if self.code[k] == "@":
            k += 1
    
        assert self.code[k] in letters
    
        k += 1
        while self.code[k] in letters+digits+"_":
            k += 1
    
        name = self.code[cur:k]
        last = k
    
        while self.code[k] in " \t":
            k += 1
    
        # Get value of cell
        if self.code[k] == "{":
    
            end = self.findend_cell(k)
            end = end+1
            while self.code[end] in " \t":
                end += 1
    
            if self.code[end] == "(":
    
                end = self.findend_paren(end)
                node = col.Cget(parent, name, cur=cur, line=line,
                        code=self.code[cur:end+1])
    
                if self.disp:
                    print "%4d %4d     Cget       " % (cur, line),
                    print repr(self.code[cur:end+1])
    
                n_fields = 0
                while self.code[k] == "{":
    
                    cur, line = self.fill_cell(node, k, line)
                    k = cur+1
                    while self.code[k] in " \t":
                        k += 1
                    n_fields += 1
    
                while self.code[k] in " \t":
                    k += 1
    
                assert self.code[k] == "("
    
                cur, line = self.create_list(node, k, line)
    
                node["n_fields"] = n_fields
                node["n_args"] = len(node) - n_fields
    
            else:
                end = self.findend_cell(k)
                node = col.Cvar(parent, name, cur=cur, line=line,
                        code=self.code[cur:end+1])
    
                if self.disp:
                    print "%4d %4d     Cvar       " % (cur, line),
                    print repr(self.code[cur:end+1])
    
                num = 0
                while self.code[k] == "{":
    
                    cur, line = self.fill_cell(node, k, line)
                    k = cur+1
                    while self.code[k] in " \t":
                        k += 1
                    num += 1
    
    
        # Get value of array
        elif self.code[k] == "(":
    
            end = self.findend_paren(k)
            if self.code[end+1] == "." and self.code[end+2] in letters:

                start = end+2
                end += 2
                while self.code[end] in letters+digits+"_":
                    end += 1
                value = self.code[start:end]

                if self.disp:
                    print "%4d %4d     Sget        " %\
                            (cur, line),
                    print repr(self.code[cur:end])

                    node = col.Sget(parent, name, value, cur=cur, line=line,
                            code=self.code[cur:end], pointer=1)

                last, line = self.create_list(node, k, line)
                cur = end

            else:
        
                if self.disp:
                    print "%4d %4d     Get        " %\
                            (cur, line),
                    print repr(self.code[cur:end+1])
        
                node = col.Get(parent, name, cur=cur, line=line,
                        code=self.code[cur:end+1])
        
                last, line = self.create_list(node, k, line)
                cur = last
    
    
    
        elif self.code[k] == "." and self.code[k+1] not in "*/\\^'":
    
            k += 1
    
            # Fieldname of type "a.(..)"
            if self.code[k] == "(":
    
                end = self.findend_paren(k)
    
                if self.disp:
                    print "%4d %4d     Nget       " % (cur, line),
                    print repr(self.code[cur:end+1])
    
                k += 1
    
                while self.code[k] in " \t":
                    k += 1
    
                node = col.Nget(parent, name, cur=cur, line=line,
                        code=self.code[cur:end+1])
    
                cur, line = self.create_expression(node, k, line)
    
                node.create_declare()
    
    
            elif self.code[k] in letters:
    
                j = k+1
                while self.code[j] in letters+digits+"_":
                    j += 1
    
                value = self.code[k:j]
                last = j
    
                while self.code[j] in " \t":
                    j += 1
    
                # Fieldname of type "a.b(...)"
                if self.code[j] == "(":
    
                    end = self.findend_paren(j)
                    if self.disp:
                        print "%4d %4d     Fget       " % (cur, line),
                        print repr(self.code[cur:end+1])
    
    
                    node = col.Fget(parent, name, cur=cur,
                            line=line, value=value, code=self.code[cur:end+1])
    
                    j += 1
                    while self.code[j] in " \t":
                        j += 1
    
                    cur, line = self.create_expression(node, j, line)
    
                    node.create_declare()
    
                # Fieldname of type "a.b"
                else:
    
                    if self.disp:
                        print "%4d %4d     Fvar       " % (cur, line),
                        print repr(self.code[cur:last])
    
                    node = col.Fvar(parent, name, value=value,
                            cur=cur, line=line, code=self.code[cur:last])
    
                    cur = last-1
    
                    node.create_declare()
    
    
        # Simple variable
        else:
    
            if self.disp:
                print "%4d %4d     Var        " % (cur, line),
                print repr(self.code[cur:last])
    
            node = col.Var(parent, name, cur=cur, line=line,
                    code=self.code[cur:last])
    
            cur = last-1
    
        while self.code[cur] in " \t":
            cur += 1
    
        return cur, line
    
    
    def create_comment(self, parent, cur, line):
    
        assert parent.cls == "Block"
        assert self.code[cur] == "%"
    
        end = self.findend_comment(cur)
        line += self.code.count("\n", cur, end+1)
    
        if self.comments:
            return end, line
    
        if self.disp:
            print "%4d %4d   Comment      " % (cur, line),
            print repr(self.code[cur:end+1])
    
        if self.code[cur+1] == "{":
            comment = col.Bcomment(parent, self.code[cur+2:end-1], cur=cur, line=line)
        else:
            k = cur-1
            while self.code[k] in " \t":
                k -= 1
            if self.code[k] == "\n":
                comment = col.Lcomment(parent, self.code[cur+1:end], cur=cur, line=line)
            else:
                comment = col.Ecomment(parent, self.code[cur+1:end], cur=cur, line=line)
    
        comment.code = self.code[cur:end+1]
    
        return end, line
    
    
    def create_string(self, parent, cur, line):
    
        end = self.findend_string(cur)
        assert "\n" not in self.code[cur:end]
        col.String(parent, self.code[cur+1:end], cur=cur, line=line,
                code=self.code[cur:end+1])
    
        if self.disp:
            print "%4d %4d   String " % (cur, line),
            print repr(self.code[cur:end+1])
    
        return end, line
    
    
    def create_list(self, parent, cur, line):
    
        assert self.code[cur] in "({"
    
        end = cur
        for vector in self.iterate_comma_list(cur):
            for start,end in vector:
                _, line = self.create_expression(parent, start, line, end)
    
        end += 1
        while self.code[end] in " \t":
            end += 1
    
        assert self.code[end] in ")}"
    
        return end, line
    
    
    
    def create_number(self, node, start, line):
    
        assert self.code[start] in digits or\
                self.code[start] == "." and self.code[start+1] in digits
    
        k = start
    
        while self.code[k] in digits:
            k += 1
        last = k-1
    
        integer = True
        if self.code[k] == ".":
            integer = False
    
            k += 1
            while self.code[k] in digits:
                k += 1
            last = k-1
    
        if self.code[k] in "eEdD":
    
            exp = k
    
            k = k+1
            if self.code[k] in "+-":
                k += 1
    
            while self.code[k] in digits:
                k += 1
    
            number = self.code[start:exp] + "e" + self.code[exp+1:k]
    
            last = k-1
    
            if self.code[k] in "ij":
    
                k += 1
                node = col.Imag(node, number, cur=start, line=line,
                        code=self.code[start:last+1])
                if self.disp:
                    print "%4d %4d     Imag       " % (start, line),
                    print repr(self.code[start:last+1])
    
            else:
                node = col.Float(node, number, cur=start, line=line,
                        code=self.code[start:last+1])
                if self.disp:
                    print "%4d %4d     Float      " % (start, line),
                    print repr(self.code[start:last+1])
    
        elif integer:
    
            number = self.code[start:k]
    
            if self.code[k] in "ij":
    
                node = col.Imag(node, self.code[start:k], cur=start, line=line,
                        code=self.code[start:last+1])
                k += 1
                if self.disp:
                    print "%4d %4d     Imag       " % (start, line),
                    print repr(self.code[start:last+1])
    
            else:
                node = col.Int(node, self.code[start:k], cur=start, line=line,
                        code=self.code[start:last+1])
                if self.disp:
                    print "%4d %4d     Int        " % (start, line),
                    print repr(self.code[start:last+1])
    
        else:
    
            if self.code[k] in "ij":
    
                node = col.Imag(node, self.code[start:k], cur=start, line=line,
                        code=self.code[start:last+1])
                k += 1
                if self.disp:
                    print "%4d %4d     Imag       " % (start, line),
                    print repr(self.code[start:last+1])
    
            else:
                node = col.Float(node, self.code[start:k], cur=start, line=line,
                        code=self.code[start:k])
                if self.disp:
                    print "%4d %4d     Float      " % (start, line),
                    print repr(self.code[start:last+1])
    
        return k-1, line
    
    def create_lambda(self, node, cur, line, eq_loc):
    
        assert self.code[cur] in letters
        assert self.code[eq_loc] == "="
    
        if self.disp:
            print "%4d %4d   Assign       " %\
                    (cur, line),
            print repr(self.code[cur:self.code.find("\n", cur)])
    
        assign = col.Assign(node, cur=cur, line=line, backend="func_lambda")
    
        _, line = self.create_assign_variable(assign, cur, line, eq_loc)
        assign[0].declare.type = "func_lambda"
        assign[0].type = "func_lambda"
    
        k = eq_loc+1
        while self.code[k] in " \t":
            k += 1
    
        line, end = self.create_lambda_func(assign, k, line)
        assign.code = self.code[cur:end+1]
    
        assign[0].reference = assign[1].reference
        assign[0].declare.reference = assign[1].reference
    
        return line, end
    
    
    def create_lambda_func(self, node, cur, line):
    
        assert self.code[cur] == "@"
    
        end = cur +1
        while self.code[end] in " \t":
            end += 1
    
        assert self.code[end] == "("
        end = self.findend_paren(end)
    
        end += 1
        while self.code[end] in " \t":
            end += 1
    
        end = self.findend_expression(end)
    
        if self.disp:
            print "%4d %4d   Lambda       " %\
                    (cur, line),
            print repr(self.code[cur:end+1])
    
        if node.cls == "Assign":
            name = node[0].name
        else:
            name = "lambda"
    
        program = node.program
        name = "_%s_%d" % (name, len(program)-2)
    
        func = col.Func(program, name, cur=cur, line=line, code=self.code[cur:end+1])
    
        declares = col.Declares(func)
        returns = col.Returns(func)
        params = col.Params(func)
    
        k = cur+1
        while self.code[k] in " \t":
            k += 1
    
        assert self.code[k] == "("
    
        cur, line = self.create_list(params, k, line)
    
        cur += 1
        while self.code[cur] in " \t":
            cur += 1
    
        block = col.Block(func)
        assign = col.Assign(block)
        var = col.Var(assign, "_retval")
    
        cur, line = self.create_expression(assign, cur, line, end=end)

        for n in utils.flatten(assign[1]):
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

        return cur, line
    
    
    def create_expression(self, node, start, line, end=None, start_opr=None):
    
        if self.code[start:start+3] == "...":
            start = self.findend_dots(start)
            start += 1
            while self.code[start] in " \t":
                start += 1
    
        if self.code[start] == ":":
    
            if self.disp:
                print "%4s %4s     Expression " % (start, line),
                print repr(self.code[start:start+1])
                print "%4s %4s     All        " % (start, line),
                print repr(self.code[start:start+1])
    
            col.All(node, cur=start, line=line, code=self.code[start])
            return start, line
    
        if end is None:
            end = self.findend_expression(start)
    
        if self.disp:
            print "%4s %4s     Expression " % (start, line),
            print repr(self.code[start:end+1])
    
        assert self.code[start] in expression_start
    
    
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
            if opr not in self.code[start:end+1]:
                continue
    
            starts = [start]
            last = start
            ends = []
    
            k = start
            while True:
    
                if self.code[k] == "(":
                    k = last = self.findend_paren(k)
    
                elif self.code[k] == "[":
                    k = last = self.findend_matrix(k)
    
                elif self.code[k] == "{":
                    k = last = self.findend_cell(k)
    
                elif self.code[k] == "'":
                    if self.is_string(k):
                        k = last = self.findend_string(k)
                    else:
                        last = k
    
                elif opr == self.code[k:k+len(opr)]:
    
                    if opr in "+-":
                        # no prefixes and no (scientific) numbers
                        if self.code[last] not in letters+digits+")]}" or\
                                self.code[k-1] in "dDeE" and self.code[k-2] in\
                                digits+"." and self.code[k+1] in digits:
                            k += 1
                            continue
    
    
                    k += len(opr)-1
                    while self.code[k+1] in " \t":
                        k += 1
    
                    # no all-operator
                    if opr == ":" and self.code[k+1] in ",;\n)]}":
                        k += 1
                        continue
    
                    starts.append(k+1)
                    ends.append(last)
    
                elif self.code[k] in letters+digits+"_":
                    last = k
    
                k += 1
                if k >= end:
                    ends.append(end)
                    break
    
            if len(ends)>1:
    
                node = self.retrieve_operator(opr)(node)
                node.cur = start
                node.line = line
                node.code = self.code[starts[0]:ends[-1]+1]
    
                for s,e in zip(starts, ends):
                    self.create_expression(node, s, line, e, opr)
    
                return end, line
    
    
        # All operators removed at this point!
    
        END = end
    
        # Prefixes
        while self.code[start] in "-~":
    
            if self.code[start] == "-":
    
                node = col.Neg(node, cur=start, line=line, code=self.code[start:end+1])
                start += 1
    
            if self.code[start] == "~":
    
                node = col.Not(node, cur=start, line=line, code=self.code[start:end+1])
                start += 1
    
            while self.code[start] in " \t":
                start += 1
    
        # Postfixes
        if self.code[end] == "'" and not self.code[start] == "'":
            if self.code[end-1] == ".":
                node = col.Ctranspose(node, cur=start, line=line,
                        code=self.code[start:end+1])
                end -= 2
            else:
                node = col.Transpose(node, cur=start, line=line,
                        code=self.code[start:end+1])
                node.cur = start
                node.line = line
                node.code = self.code[start:end+1]
                end -= 1
    
            while self.code[end] in " \t":
                end -= 1
    
        # Parenthesis
        if self.code[start] == "(":
            assert self.code[end] == ")"
    
            node = col.Paren(node, cur=start, line=line, code=self.code[start:end+1])
    
            start += 1
            while self.code[start] in " \t":
                start += 1
    
            end -= 1
            while self.code[end] in " \t":
                end -= 1
    
            return self.create_expression(node, start, line, end)
    
        # Reserved keywords
        elif self.code[start:start+3] == "end" and\
                self.code[start+3] in " \t" + expression_end:
                    node = col.End(node, cur=start, line=line, code=self.code[start:start+3])
    
        elif self.code[start:start+6] == "return" and self.code[start+6] in " ,;\n":
            node = col.Return(node, cur=start, line=line, code=self.code[start:start+6])
    
        elif self.code[start:start+5] == "break" and self.code[start+5] in " ,;\n":
            node = col.Break(node, cur=start, line=line, code=self.code[start:start+5])
    
    
        # Rest
        elif self.code[start] == "'":
    #              assert self.is_string(start)
            assert self.code[end] == "'"
            assert "\n" not in self.code[start:end]
    
            col.String(node, self.code[start+1:end], cur=start, line=line,
                    code=self.code[start:end+1])
    
        elif self.code[start] in digits or\
                self.code[start] == "." and self.code[start+1] in digits:
            cur, line = self.create_number(node, start, line)
    
        elif self.code[start] == "[":
            cur, line = self.create_matrix(node, start, line)
    
        elif self.code[start] == "{":
            cur, line = self.create_cell(node, start, line)
    
        else:
            assert self.code[start] in letters+"@"
            cur, line = self.create_variable(node, start, line)
    
        return END, line
    
    
    def retrieve_operator(self, opr):
    
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
    
    
    def is_space_delimited(self, start):
        assert self.code[start] in list_start
    
        k = start+1
        while self.code[k] in " \t":
            k += 1
    
        if self.code[k] in list_end:
            return False
    
        assert self.code[k] in expression_start
    
        if self.code[k] == "'":
            k = self.findend_string(k)+1
    
            while self.code[k] in " \t":
                k += 1
    
        while True:
    
            if self.code[k] == "(":
                k = self.findend_paren(k)
    
            elif self.code[k] == "[":
                k = self.findend_matrix(k)
    
            elif self.code[k] == "{":
                k = self.findend_cell(k)
    
            elif self.code[k] == "'":
                if self.code[k-1] in string_prefix:
                    return True
    
            elif self.code[k:k+3] == "...":
                k = self.findend_dots(k)
    
            elif self.code[k] in " \t":
                if self.is_space_delimiter(k):
                    return True
                while self.code[k+1] in " \t":
                    k += 1
    
            elif self.code[k] in expression_end:
                if self.code[k] == ",":
                    return False
                elif self.code[k] in list_end:
                    return False
                elif self.code[k] != ";":
                    return True
    
                while self.code[k+1] in " \t":
                    k += 1
    
            elif self.code[k+1] in letters + digits + "_@":
                while self.code[k+1] in letters + digits + "_@":
                    k += 1
            k += 1
    
    def iterate_list(self, start):
    
        if self.is_space_delimited(start):
            return self.iterate_space_list(start)
        return self.iterate_comma_list(start)
    
    
    def iterate_comma_list(self, start):
    
        assert self.code[start] in list_start
        k = start+1
    
        while self.code[k] in " \t":
            k += 1
    
        if self.code[k] in "]}":
            return [[]]
    
        out = [[]]
        count = False
    
        while True:
    
            if self.code[k:k+3] == "...":
                k = self.findend_dots(k)
    
            elif self.code[k] in expression_start:
                assert not count
                count = True
                end = self.findend_expression(k)
                out[-1].append((k, end))
    
                k = end
    
            elif self.code[k] == ",":
                assert count
                count = False
    
            elif self.code[k] == ";":
    
                assert count
                count = False
                out.append([])
    
            elif self.code[k] in list_end:
                return out
    
            k += 1
    
    
    def iterate_space_list(self, start):
    
        assert self.code[start] in list_start
    
        k = start+1
        while self.code[k] in " \t":
            k += 1
    
        out = [[]]
        count = False
    
        while True:

            if self.code[k:k+3] == "...":
                k = self.findend_dots(k)
    
            elif self.code[k] in ";\n":
                out.append([])
    
            elif self.code[k] in expression_start:
                assert not count
                count = True
    
                end = self.findend_expression_space(k)
                out[-1].append((k, end))
                k = end
    
            elif self.code[k] in list_end:
                return out
    
            elif self.code[k] in " \t":
                count = False
    
            k += 1
    
    
    def findend_expression(self, start):
    
        assert self.code[start] in expression_start
        k = start
    
        while True:
    
            if self.code[k] == "(":
                k = self.findend_paren(k)
    
            elif self.code[k] == "[":
                k = self.findend_matrix(k)
    
            elif self.code[k] == "'" and self.is_string(k):
                k = self.findend_string(k)
    
            elif self.code[k] == "{":
                k = self.findend_cell(k)
    
            elif self.code[k:k+3] == "...":
                k = self.findend_dots(k)
    
            elif self.code[k] == "=":
    
                if self.code[k+1] == "=":
                    k += 1
                else:
                    break
    
            elif self.code[k] in "><~":
    
                if self.code[k+1] == "=":
                    k += 1
    
            elif self.code[k:k+3] == "...":
                k = self.findend_dots(k)
    
            elif self.code[k] in expression_end:
                break
    
            k += 1
    
        k -= 1
        while self.code[k] in " \t":
            k -= 1
    
        return k
    
    def findend_expression_space(self, start):

        assert self.code[start] in expression_start
        k = last = start
    
        while True:
    
            if self.code[k] == "(":
                k = last = self.findend_paren(k)
    
            elif self.code[k] == "[":
                k = last = self.findend_matrix(k)
    
            elif self.code[k] == "'":
                if self.is_string(k):
                    k = last = self.findend_string(k)
                else:
                    last = k
    
            elif self.code[k] == "{":
                k = last = self.findend_cell(k)
    
            elif self.code[k:k+3] == "...":
                k = self.findend_dots(k)
    
            elif self.code[k] == ";":
                return last
    
            elif self.code[k] == "=":
    
                if self.code[k+1] == "=":
                    k += 1
                else:
                    return last
    
            elif self.code[k] in "><~":
    
                if self.code[k+1] == "=":
                    k += 1
    
            elif self.code[k] in "+-":
                while self.code[k+1] in " \t":
                    k += 1
    
            elif self.code[k] in " \t":
    
                if self.is_space_delimiter(k):
                    return last
                while self.code[k+1] in " \t+-~":
                    k += 1
    
            elif self.code[k] in expression_end:
                return last
    
            elif self.code[k] in letters + digits + "_@":
                while self.code[k+1] in letters + digits + "_@":
                    k += 1
                last = k
    
            k += 1
    
    def is_space_delimiter(self, start):
    
        assert self.code[start] in " \t"
        k = start
    
        while True:
    
            if self.code[k:k+3] == "...":
                return False
    
            elif self.code[k] in " \t":
                pass
    
            elif self.code[k] in "+-~":
                if self.code[k+1] in " \t":
                    return False
    
            elif self.code[k:k+2] in operator2:
                return False
    
            elif self.code[k] in operator1:
                return False
    
            else:
                return True
    
            k += 1
    
    def findend_matrix(self, start):
        "find index to end of matrix"
    
        assert self.code[start] == "["
        k = start+1
    
        if self.is_space_delimited(start):
    
            # Ignore first string occurence
            while self.code[k] in " \t":
                k += 1
            if self.code[k] == "'":
                k = self.findend_string(k)+1
    
            while True:
    
                if self.code[k] == "[":
                    k = self.findend_matrix(k)
    
                elif self.code[k] == "]":
                    return k
    
                elif self.code[k] == "%":
                    k = self.findend_comment(k)
    
                elif self.code[k] == "'" and self.code[k-1] in string_prefix:
                    k = self.findend_string(k)
    
                k += 1
    
        else:
            while True:
    
                if self.code[k] == "[":
                    k = self.findend_matrix(k)
    
                elif self.code[k] == "]":
                    return k
    
                elif self.code[k] == "%":
                    k = self.findend_comment(k)
    
                elif self.code[k] == "'" and self.is_string(k):
                    k = self.findend_string(k)
    
                k += 1
    
    def findend_string(self, start):
        "find index to end of string"
    
        assert self.code[start] == "'"
    
        k = self.code.find("'", start+1)
        assert k != -1
    
    #          while self.code[k-1] == "\\" and self.code[k-2] != "\\":
    #              k = self.code.find("'", k+1)
    #              assert k != -1
    
        assert self.code.find("\n", start, k) == -1
        return k
    
    def findend_comment(self, start):
        "find index to end of comment"
    
        assert self.code[start] == "%"
    
        # blockcomment
        if self.code[start+1] == "{":
            eoc = self.code.find("%}", start+2)
            assert eoc>-1
            return eoc+1
    
        # Linecomment
        eoc = self.code.find("\n", start)
        assert eoc>-1
        return eoc
    
    def findend_dots(self, start):
    
        assert self.code[start:start+3] == "..."
        k = self.code.find("\n", start)
        assert k != -1
        return k
    
    def findend_paren(self, start):
    
        assert self.code[start] == "("
    
        k = start+1
        while True:
    
            if self.code[k] == "%":
                assert False
    
            elif self.code[k:k+3] == "...":
                k = self.findend_dots(k)
    
            elif self.code[k] == "'" and self.is_string(k):
                k = self.findend_string(k)
    
            elif self.code[k] == "[":
                k = self.findend_matrix(k)
    
            elif self.code[k] == "(":
                k = self.findend_paren(k)
    
            elif self.code[k] == ")":
                return k
    
            k += 1
    
    def findend_cell(self, start):
        assert self.code[start] == "{"
    
        k = start
        while True:
    
            if self.code[k] == "%":
                assert False
            elif self.code[k] == "'" and self.is_string(k):
                k = self.findend_string(k)
            elif self.code[k] == "(":
                k = self.findend_paren(k)
            elif self.code[k] == "[":
                k = self.findend_matrix(k)
            elif self.code[k] == "}":
                l = k+1
                while self.code[l] in " \t":
                    l += 1
                if self.code[l] != "{":
                    return k
                k = l
    
            k += 1
    
    def is_string(self, k):
    
        assert self.code[k] == "'"
    
        if self.code[k-1] == ".":
            return False
    
        j = k-1
        while self.code[j] in " \t":
            j -= 1
    
        if self.code[j] in letters+digits+")]}_":
    
            # special cases
            if self.code[j-3:j+1] == "case":
                return True
    
            return False
    
        return True


if __name__ == "__main__":
    code = """
% 123
    """
    tree = utils.build(code, True)

    print tree.summary()
    print tree.translate_tree()
    print code

