#!/usr/bin/env python
# encoding: utf-8

import os
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

    def __init__(self, disp=False, comments=True):
        """
   Kwargs:
        disp (bool):
            Verbose output while loading code.
        comments (bool):
            Include comments in the code interpretation.
        """

        self.disp = disp
        self.comments = comments
        self.project = col.Project()

    def __getitem__(self, i):
        return self.project[i]

    def load(self, name, code):
        """
    Load a Matlab code into the node tree.

    Will throw and exception if module loaded without the `folder` option.

    Args:
        name (str):
            Name of program (usually valid filename).
        code (str):
            Matlab code to be loaded
        """

        if self.disp:
            print "loading", name

        self.code = code + "\n\n\n"
        self.create_program(name)
        return self.project[-1]


    def get_unknowns(self, name):

        program = self.project[self.project.names.index(name)]

        nodes = utils.flatten(program, False, True, False)
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

            if unassigned[i] in translations._reserved.reserved:
                reserved.add(unassigned.pop(i))

        for node in nodes[::-1]:

            if node.name in reserved:
                node.backend = "reserved"

        return unassigned


    def configure(self, suggest=True):

        nodes = utils.flatten(self.project, False, True, False)
        while True:

            for node in nodes[::-1]:

                if node.cls in ("Get", "Var"):

                    if node.type == "func_lambda":
                        node.backend = "func_lambda"

                        if not (node.parent.cls in \
                                ("Declares", "Returns", "Params")) and\
                                hasattr(node.parent[-1].declare, "reference"):

                            if node.parent.cls == "Assign":
                                node.declare.reference = \
                                        node.parent[-1].declare.reference
                            node.reference = node.declare.reference

                    # lambda scope
                    if node.backend == "func_lambda":
                        if hasattr(node, "reference"):
                            func = node.reference
                        else:
                            func = None

                    # local scope
                    elif node in node.program[1]:
                        func = node.program[1][node]
                        node.backend = func.backend

                    # external file in same folder
                    else:

                        for program in self.project:

                            if os.path.isfile(program.name) and \
                                    os.path.basename(program.name) == node.name+".m":
                                func = program[1][0]
                                # self.project[self.project.names.index(
                                    # node.name+".m")][1][0]
                                node.backend = func.backend
                                break
                        else:
                            func = None
                            node.translate_node()

                    if not (func is None):
                        if node.backend == "func_return":
                            node.backend = func.backend
                            node.declare.type = func[1][0].type
                            params = func[2]
                            for i in xrange(len(node)):
                                params[i].suggest = node[i].type
                                node[i].suggest = params[i].type

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

                            ret = func[1][0]
                            if ret.type != "TYPE" and node.type == "TYPE":
                                node.type = ret.type
                            elif ret.type == "TYPE" and node.type != "TYPE":
                                ret.type = node.type

                            params = func[2]
                            for i in xrange(len(node)):
                                params[i].suggest = node[i].type

                elif node.cls in ("Fvar", "Cget", "Fget", "Nget", "Colon"):
                    node.translate_node()

                elif node.cls == "Vector":

                    if node and node[0].backend == "struct":
                        declare = node.func[0][
                                node.func[0].names.index(node[0].name)]
                        if declare.backend == "structs":
                            node.backend = "structs"

                    node.type = [n.type for n in node]
                    node.translate_node()

                elif node.cls == "Matrix":

                    if node[0] and node[0][0].backend == "struct":
                        declare = node.func[0][
                                node.func[0].names.index(node[0][0].name)]
                        if declare.backend == "structs":
                            node.backend = "structs"

                    node.type = [n.type for n in node]
                    node.translate_node()

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
                    node[0].suggest = node[1].type


                elif node.cls == "Neg" and node[0].mem == 0:
                    node.mem = 1

            if suggest:

                complete = True
                for program in self.project:
                    types_f, types_s, types_i, suggests =\
                            supplement.get_variables(program)

                    for s in suggests:

                        if not suggests[s]:
                            continue

                        if s in types_f:
                            types_f[s].update(suggests[s])
                        elif s in types_s:
                            types_s[s].update(suggests[s])
                        
                        complete = False

                    supplement.set_variables(program, types_f, types_s)

                if complete:
                    break

                if suggest == 1:
                    suggest = 0

            else:
                break


    def create_program(self, name):
    
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
                cur = self.findend_comment(cur)
   
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
                        assert all([a in letters+digits+"_@" \
                                for a in self.code[s:e+1]])
    
                        col.Var(returns, self.code[s:e+1], cur=s,
                                code=self.code[s:e+1])
    
            # single return
            else:
                end = self.findend_expression(start)
    
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
                m = self.findend_paren(m)
            else:
                m = end
    
    
            if self.disp:
                print "%4d Function       " % cur,
                print repr(self.code[START:m+1])
    
            end = start+1
            while self.code[end] in letters+"_":
                end += 1
    
            name = self.code[start:end]
            func = col.Func(parent, name, cur=cur)
    
            col.Declares(func)
            returns = col.Returns(func)
    
            cur = end
    
        # Parameters
        params = col.Params(func, cur=cur)
        if self.code[cur] == "(":
    
            end = self.findend_paren(cur)
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
    
                # Divide beween statement and assignment
                eq_loc = self.findend_matrix(cur)+1
    
                while self.code[eq_loc] in " \t":
                    eq_loc += 1
    
                if self.code[eq_loc] == "=" and self.code[eq_loc+1] != "=":
    
                    cur = self.create_assigns(block, cur, eq_loc)
    
                else:
    
                    statement = col.Statement(block, cur=cur)
    
                    end = self.findend_expression(cur)
                    if self.disp:
                        print "%4d   Statement    " % cur,
                        print repr(self.code[cur:end+1])
    
                    statement.code = self.code[cur:end+1]
    
                    cur = self.create_expression(
                            statement, cur, end=end)
    
    
            elif self.code[cur] == "'":
    
                end = self.findend_string(cur)
                if self.disp:
                    print "%4d   Statement    " % cur,
                    print repr(self.code[cur:end+1])
    
                statement = col.Statement(block, cur=cur,
                        code=self.code[cur:end+1])
    
                cur = self.create_string(statement, cur)
    
            elif self.code[cur:cur+4] == "case" and self.code[cur+4] in key_end:
                break
    
            elif self.code[cur:cur+5] == "catch" and self.code[cur+5] in key_end:
                break
    
            elif self.code[cur:cur+3] == "end" and self.code[cur+3] in key_end:
                cur += 3
                break
    
            elif self.code[cur:cur+4] == "else" and self.code[cur+4] in key_end:
                break
    
            elif self.code[cur:cur+6] == "elseif" and self.code[cur+6] in key_end:
                break
    
            elif self.code[cur:cur+3] == "for" and self.code[cur+3] in key_end:
                cur = self.create_for(block, cur)
    
            elif self.code[cur:cur+8] == "function" and\
                    self.code[cur+8] in key_end + "[":
                cur -= 1
                break
    
            elif self.code[cur:cur+2] == "if" and self.code[cur+2] in key_end:
                cur = self.create_if(block, cur)
    
            elif self.code[cur:cur+9] == "otherwise" and self.code[cur+9] in key_end:
                break
    
            elif self.code[cur:cur+6] == "switch" and self.code[cur+6] in key_end:
                cur = self.create_switch(block, cur)
    
            elif self.code[cur:cur+3] == "try" and self.code[cur+3] in key_end:
                cur = self.create_try(block, cur)
    
            elif self.code[cur:cur+5] == "while" and self.code[cur+5] in key_end:
                cur = self.create_while(block, cur)
    
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
                        cur = self.create_lambda(block, cur, eq_loc)
                    else:
                        cur = self.create_assign(block, cur, eq_loc)
    
                else:
                    end = self.findend_expression(cur)
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
    
    
    def create_assigns(self, parent, cur, eq_loc):
    
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
    
    
    def create_assign(self, parent, cur, eq_loc):
    
        assert self.code[cur] in letters
        assert self.code[eq_loc] == "="
    
        j = eq_loc+1
        while self.code[j] in " \t":
            j += 1
        end = self.findend_expression(j)
    
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
    
        assert self.code[cur] == "="
    
        k = cur+1
        while self.code[k] in " \t":
            k += 1
    
        self.create_expression(assign, k, end)
        assign.name = assign[-1].name
    
        assert len(assign) == 2
    
        return end
    
    
    
    def create_assign_variable(self, node, cur, end=None):
    
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
                node = col.Cset(node, name, cur=cur,
                        code=self.code[cur:end+1])
    
                if self.disp:
                    print "%4d     Cset       " % cur,
                    print repr(self.code[cur:end+1])
    
                n_fields = 0
                while self.code[k] == "{":
    
                    cur = self.fill_cell(node, k)
                    k = cur+1
                    while self.code[k] in " \t":
                        k += 1
                    n_fields += 1
    
                while self.code[k] in " \t":
                    k += 1
    
                assert self.code[k] == "("
    
                cur = self.create_list(node, k)
    
                node["n_fields"] = n_fields
                node["n_args"] = len(node) - n_fields
    
            else:
                end = self.findend_cell(k)
                node = col.Cvar(node, name, cur=cur,
                        code=self.code[cur:end+1])
    
                if self.disp:
                    print "%4d     Cvar       " % cur,
                    print repr(self.code[cur:end+1])
    
                num = 0
                while self.code[k] == "{":
    
                    cur = self.fill_cell(node, k)
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
    
                end = self.findend_paren(k)
    
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
    
    
    def fill_cell(self, cset, cur):
    
        assert self.code[cur] == "{"
    
        cur = cur+1
    
        while True:
    
            if self.code[cur] == "}":
                return cur
    
            elif self.code[cur] in expression_start:
    
                cur = self.create_expression(cset, cur)
    
                cur += 1
                while self.code[cur] in " \t":
                    cur += 1
    
                return cur
    
            elif self.code[cur] == " ":
                pass
    
            cur += 1
    
    
    def create_matrix(self, node, cur):
    
        assert self.code[cur] == "["
    
        end = self.findend_matrix(cur)
        if self.disp:
            print "%4d     Matrix     " % cur,
            print repr(self.code[cur:end+1])
    
        L = self.iterate_list(cur)
        matrix = col.Matrix(node, cur=cur, code=self.code[cur:end+1])
    
        for array in L:
    
            if array:
                start = array[0][0]
                end = array[-1][-1]
            else:
                start = cur
    
            vector = col.Vector(matrix, cur=start,
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
            vector = col.Vector(matrix, cur=cur, code="")
    
    
        return self.findend_matrix(cur)
    
    
    def create_for(self, parent, cur):
    
        assert self.code[cur:cur+3] == "for"
    
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
        assert self.code[cur] == "="
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
    
        assert self.code[start:start+2] == "if" and self.code[start+2] in key_end
    
        branch = col.Branch(parent, cur=start)
    
        cur = start
    
        cur += 2
        while self.code[cur] in " \t":
            cur += 1
    
        assert self.code[cur] in expression_start
        end = self.findend_expression(cur)
    
        if self.disp:
            print "%4d   If           " % (start),
            print repr(self.code[start:end+1])
    
        node = col.If(branch, cur=cur)
    
        if self.code[cur] == "(":
            cur += 1
            while self.code[cur] in " \t":
                cur += 1
        self.create_expression(node, cur)
    
        end = self.create_codeblock(node, end+1)
        node.code = self.code[cur:end+1]

        while self.code[cur:cur+6] == "elseif" and self.code[cur+6] in key_end:
    
            node.code = self.code[start:cur]
            start = cur
    
            cur += 6
            while self.code[cur] in " \t":
                cur += 1
    
            end = self.findend_expression(cur)
    
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
    
        if self.code[cur:cur+4] == "else" and self.code[cur+4] in key_end:
    
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
    
    
    def create_while(self, parent, cur):
    
        assert self.code[cur:cur+5] == "while" and self.code[cur+5] in key_end
        start = cur
    
        k = cur+5
        while self.code[k] in " \t":
            k += 1
    
        end = self.findend_expression(k)
    
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
    
    
    def create_switch(self, parent, cur):
    
        assert self.code[cur:cur+6] == "switch" and\
                self.code[cur+6] in " \t("
    
        k = cur+6
        while self.code[k] in " \t":
            k += 1
    
        end = self.findend_expression(k)
    
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
    
            end = self.findend_expression(k)
    
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
    
    
    
    def create_try(self, parent, cur):
        assert self.code[cur:cur+3] == "try" and self.code[cur+3] in key_end
    
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
    
        assert self.code[cur:cur+5] == "catch" and self.code[cur+5] in key_end
    
        catch_ = col.Catch(tryblock, cur=cur)
    
        start_ = cur
        cur += 5
        while self.code[cur] in " \t\n,;":
            cur += 1
    
        cur = self.create_codeblock(catch_, cur)
    
        catch_.code = self.code[start_:cur]
        tryblock.code = self.code[start:cur]
    
        return cur
    
    
    
    def create_cell(self, node, cur):
        assert self.code[cur] == "{"
    
        end = self.findend_cell(cur)
        if self.disp:
            print "%4d     Cell       " % cur,
            print repr(self.code[cur:end+1])
    
        L = self.iterate_list(cur)
        cell = col.Cell(node, cur=cur, code=self.code[cur:end+1])
    
        for array in L:
    
            if array:
                start = array[0][0]
                end = array[-1][-1]
            else:
                start = cur
    
            for start,end in array:
    
                self.create_expression(cell, start, end)
    
    
        return self.findend_cell(cur)
    
    
    def create_variable(self, parent, cur):
    
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
                node = col.Cget(parent, name, cur=cur,
                        code=self.code[cur:end+1])
    
                if self.disp:
                    print "%4d     Cget       " % cur,
                    print repr(self.code[cur:end+1])
    
                n_fields = 0
                while self.code[k] == "{":
    
                    cur = self.fill_cell(node, k)
                    k = cur+1
                    while self.code[k] in " \t":
                        k += 1
                    n_fields += 1
    
                while self.code[k] in " \t":
                    k += 1
    
                assert self.code[k] == "("
    
                cur = self.create_list(node, k)
    
                node["n_fields"] = n_fields
                node["n_args"] = len(node) - n_fields
    
            else:
                end = self.findend_cell(k)
                node = col.Cvar(parent, name, cur=cur,
                        code=self.code[cur:end+1])
    
                if self.disp:
                    print "%4d     Cvar       " % cur,
                    print repr(self.code[cur:end+1])
    
                num = 0
                while self.code[k] == "{":
    
                    cur = self.fill_cell(node, k)
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
    
                end = self.findend_paren(k)
    
                if self.disp:
                    print "%4d     Nget       " % cur,
                    print repr(self.code[cur:end+1])
    
                k += 1
    
                while self.code[k] in " \t":
                    k += 1
    
                node = col.Nget(parent, name, cur=cur,
                        code=self.code[cur:end+1])
    
                cur = self.create_expression(node, k)
    
    
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
    
    
    def create_comment(self, parent, cur):
    
        assert parent.cls == "Block"
        assert self.code[cur] == "%"
    
        end = self.findend_comment(cur)
    
        if self.comments:
            return end
    
        if self.disp:
            print "%4d   Comment      " % cur,
            print repr(self.code[cur:end+1])
    
        if self.code[cur+1] == "{":
            comment = col.Bcomment(parent, self.code[cur+2:end-1], cur=cur)
        else:
            k = cur-1
            while self.code[k] in " \t":
                k -= 1
            if self.code[k] == "\n":
                comment = col.Lcomment(parent, self.code[cur+1:end], cur=cur)
            else:
                comment = col.Ecomment(parent, self.code[cur+1:end], cur=cur)
    
        comment.code = self.code[cur:end+1]
    
        return end
    
    
    def create_string(self, parent, cur):
    
        end = self.findend_string(cur)
        assert "\n" not in self.code[cur:end]
        col.String(parent, self.code[cur+1:end], cur=cur,
                code=self.code[cur:end+1])
    
        if self.disp:
            print "%4d   String " % cur,
            print repr(self.code[cur:end+1])
    
        return end
    
    
    def create_list(self, parent, cur):
    
        assert self.code[cur] in "({"
    
        end = cur
        for vector in self.iterate_comma_list(cur):
            for start,end in vector:
                self.create_expression(parent, start, end)
    
        end += 1
        while self.code[end] in " \t":
            end += 1
    
        assert self.code[end] in ")}"
    
        return end
    
    
    
    def create_number(self, node, start):
    
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
                node = col.Imag(node, number, cur=start,
                        code=self.code[start:last+1])
                if self.disp:
                    print "%4d     Imag       " % (start),
                    print repr(self.code[start:last+1])
    
            else:
                node = col.Float(node, number, cur=start,
                        code=self.code[start:last+1])
                if self.disp:
                    print "%4d     Float      " % (start),
                    print repr(self.code[start:last+1])
    
        elif integer:
    
            number = self.code[start:k]
    
            if self.code[k] in "ij":
    
                node = col.Imag(node, self.code[start:k], cur=start,
                        code=self.code[start:last+1])
                k += 1
                if self.disp:
                    print "%4d     Imag       " % (start),
                    print repr(self.code[start:last+1])
    
            else:
                node = col.Int(node, self.code[start:k], cur=start,
                        code=self.code[start:last+1])
                if self.disp:
                    print "%4d     Int        " % (start),
                    print repr(self.code[start:last+1])
    
        else:
    
            if self.code[k] in "ij":
    
                node = col.Imag(node, self.code[start:k], cur=start,
                        code=self.code[start:last+1])
                k += 1
                if self.disp:
                    print "%4d     Imag       " % (start),
                    print repr(self.code[start:last+1])
    
            else:
                node = col.Float(node, self.code[start:k], cur=start,
                        code=self.code[start:k])
                if self.disp:
                    print "%4d     Float      " % (start),
                    print repr(self.code[start:last+1])
    
        return k-1
    
    def create_lambda(self, node, cur, eq_loc):
    
        assert self.code[cur] in letters
        assert self.code[eq_loc] == "="
    
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
    
        assert self.code[k] == "("
    
        cur = self.create_list(params, k)
    
        cur += 1
        while self.code[cur] in " \t":
            cur += 1
    
        block = col.Block(func)
        assign = col.Assign(block)
        var = col.Var(assign, "_retval")
    
        cur = self.create_expression(assign, cur, end=end)

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

        return cur
    
    
    def create_expression(self, node, start, end=None, start_opr=None):
    
        if self.code[start:start+3] == "...":
            start = self.findend_dots(start)
            start += 1
            while self.code[start] in " \t":
                start += 1
    
        if self.code[start] == ":":
    
            if self.disp:
                print "%4d     Expression " % (start),
                print repr(self.code[start:start+1])
                print "%4d     All        " % (start),
                print repr(self.code[start:start+1])
    
            col.All(node, cur=start, code=self.code[start])
            return start
    
        if end is None:
            end = self.findend_expression(start)
    
        if self.disp:
            print "%4d     Expression " % (start),
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
                node.code = self.code[starts[0]:ends[-1]+1]
    
                for s,e in zip(starts, ends):
                    self.create_expression(node, s, e, opr)
    
                return end
    
    
        # All operators removed at this point!
    
        END = end
    
        # Prefixes
        while self.code[start] in "-~":
    
            if self.code[start] == "-":
    
                node = col.Neg(node, cur=start, code=self.code[start:end+1])
                start += 1
    
            if self.code[start] == "~":
    
                node = col.Not(node, cur=start, code=self.code[start:end+1])
                start += 1
    
            while self.code[start] in " \t":
                start += 1
    
        # Postfixes
        if self.code[end] == "'" and not self.code[start] == "'":
            if self.code[end-1] == ".":
                node = col.Ctranspose(node, cur=start,
                        code=self.code[start:end+1])
                end -= 2
            else:
                node = col.Transpose(node, cur=start,
                        code=self.code[start:end+1])
                node.cur = start
                node.code = self.code[start:end+1]
                end -= 1
    
            while self.code[end] in " \t":
                end -= 1
    
        # Parenthesis
        if self.code[start] == "(":
            assert self.code[end] == ")"
    
            node = col.Paren(node, cur=start, code=self.code[start:end+1])
    
            start += 1
            while self.code[start] in " \t":
                start += 1
    
            end -= 1
            while self.code[end] in " \t":
                end -= 1
    
            return self.create_expression(node, start, end)
    
        # Reserved keywords
        elif self.code[start:start+3] == "end" and\
                self.code[start+3] in " \t" + expression_end:
                    node = col.End(node, cur=start, code=self.code[start:start+3])
    
        elif self.code[start:start+6] == "return" and self.code[start+6] in " ,;\n":
            node = col.Return(node, cur=start, code=self.code[start:start+6])
    
        elif self.code[start:start+5] == "break" and self.code[start+5] in " ,;\n":
            node = col.Break(node, cur=start, code=self.code[start:start+5])
    
    
        # Rest
        elif self.code[start] == "'":
    #              assert self.is_string(start)
            assert self.code[end] == "'"
            assert "\n" not in self.code[start:end]
    
            col.String(node, self.code[start+1:end], cur=start,
                    code=self.code[start:end+1])
    
        elif self.code[start] in digits or\
                self.code[start] == "." and self.code[start+1] in digits:
            cur = self.create_number(node, start)
    
        elif self.code[start] == "[":
            cur = self.create_matrix(node, start)
    
        elif self.code[start] == "{":
            cur = self.create_cell(node, start)
    
        else:
            assert self.code[start] in letters+"@"
            cur = self.create_variable(node, start)
    
        return END
    
    
    def retrieve_operator(self, opr):
    
        if opr == "^":      return col.Exp
        elif opr == ".^":   return col.Elexp
        elif opr == "\\":   return col.Leftmatrixdivision
        elif opr == ".\\":  return col.Leftelementdivision
        elif opr == "/":    return col.Matrixdivision
        elif opr == "./":   return col.Elementdivision
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
% comment
function x = cgsolve(A, b)
x = A(b);
end
    """
    program = utils.build(code, True)

    print program.summary()
    program.translate_tree()
    print program[1]
    print code

