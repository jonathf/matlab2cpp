import re
import os
from os.path import sep

import reference
import matlab2cpp
import matlab2cpp.m2cpp
import matlab2cpp.pyplot

def flatten(node, ordered=False, reverse=False, inverse=False):
    """
Backend for the :py:func:`~matlab2cpp.Node.flatten` function.

Args:
    node (Node): Root node to start from
    ordered (bool): If True, make sure the nodes are hierarcically ordered.
    reverse (bool): If True, children are itterated in reverse order.
    inverse (bool): If True, tree is itterated in reverse order.

See also:
    :py:func:`~matlab2cpp.Node.flatten`
    """

    o = bool(ordered)
    r = bool(reverse)
    i = bool(inverse)

    out = []

    if o:

        nodes = [node]
        for node in nodes:
            nodes.extend(node.children[::1-2*(r ^ i)])
        out.extend(nodes[::1-2*i])

    else:

        if i:
            def foo(node):
                for child in node[::1-2*r]:
                    foo(child)
                out.append(node)

        else:
            def foo(node):
                out.append(node)
                for child in node[::1-2*r]:
                    foo(child)

        foo(node)

    return out


def summary(node, opt):
    """
Backend for creating summary of the node tree.
See :py:func:`~matlab2cpp.qtree` for behavior.

Args:
    node (Node): Relative root of the tree

Returns:
    str: string representation of the node

See also:
    :py:func:`~matlab2cpp.qtree`
    """
    
    nodes = flatten(node, False, False, False)

    if not (opt is None) and opt.disp:
        print "iterating over %d nodes" % len(nodes)

    
    if not (opt is None) and not (opt.line is None):
        for node in nodes:
            if node.cls != "Block" and node.line == opt.line:
                nodes = flatten(node, False, False, False)
                break

    indent = []
    outl = []

    nl = len(str(nodes[-1].line))+1
    nc = len(str(nodes[-1].cur+1))+1

    for node in nodes:

        out = ""

        if node.line:
            nl_ = len(str(node.line))
            out += " "*(nl-nl_) + str(node.line) + " "
            nc_ = len(str(node.cur+1))
            out += " "*(nc-nc_) + str(node.cur+1)
        else:
            out += " "*(nl+nc+1)

        # indentation
        while indent and not (node.parent is indent[-1]):
            indent.pop()
        out += "| "*(len(indent))
        indent.append(node)

        out += node.cls.ljust(11)
        out += node.backend.ljust(13)
        
        # define type
        if node.type == "TYPE":
            type = node.declare.prop.get("suggest", "TYPE")
            if type != "TYPE":
                type = "(" + type + ")"
        else:
            type = node.type
        out += type.ljust(8)
        out += node.name

        outl.append(out)

    out = "\n".join(outl)

    out = re.sub(r"(\\n){2,}", "", out)

    return out


def auxillary(node, type, convert):
    """
Backend for the :py:func:`~matlab2cpp.Node.auxillary` function.

Args:
    node (Node):
        Root of the tree where split into new line will occour.
    type (str, None):
        If provided, auxiliary variable type will be converted
    convert (bool):
        If true, add an extra function call ``conv_to`` to convert datatype in
        Armadillo.

See also:
    :py:func:`~matlab2cpp.Node.auxiliary`
    """

    assert node.parent.cls != "Assign",\
            ".auxiliary() must be triggered mid expression."

    type = type or node.type

    if not isinstance(type, str):
        if isinstance(type[0], int):
            type = matlab2cpp.datatype.get_name(*type)
        else:
            type = matlab2cpp.datatype.common_strict(type)

    matrix_mode = False
    if node.cls == "Matrix":
        matrix_mode = True

    if matrix_mode and type == "int" and node.group.cls in ("Get", "Set"):
        type = "uword"

    line = node
    while line.parent.cls != "Block":
        line = line.parent
    block = line.parent

    # Create new var
    i = 1
    declares = node.func[0]
    while "_aux_" + type + "_" + str(i) in declares:
        i += 1
    var = "_aux_" + type + "_" + str(i)

    # Create Assign
    assign = matlab2cpp.collection.Assign(block, code=node.code)
    assign.type = type
    if matrix_mode:
        assign.backend = "matrix"

    # Return value
    aux_var = matlab2cpp.collection.Var(assign, var)
    aux_var.type = type
    aux_var.backend = type
    aux_var.create_declare()

    if convert:
        rhs = matlab2cpp.collection.Get(assign, "_conv_to")
        rhs.type = type
    else:
        rhs = assign

    swap_var = matlab2cpp.collection.Var(rhs, var)
    swap_var.declare.type = type

    # Place Assign correctly in Block
    i = block.children.index(line)
    block.children = block[:i] + block[-1:] + block[i:-1]

    # Swap node and Var
    index = node.parent.children.index(node)
    node.parent.children[index] = swap_var
    rhs.children[-1] = node

    swap_var.parent, node.parent = node.parent, swap_var.parent

    # generate code
    node.translate()
    swap_var.translate(only=True)
    aux_var.translate(only=True)
    if convert:
        rhs.translate(only=True)
    assign.translate(only=True)

    if convert:
        assert node.type != swap_var.type

    return swap_var



def resize(node):
    """
Backend for the :py:func:`~matlab2cpp.Node.resize` function.

Args:
    node (Node): node to be resized

See also:
    :py:func:`~matlab2cpp.Node.resize`
    """

    if node["_resize"]:
        return
    node["_resize"] = True

    type = node.type
    node.dim = 3

    line = node
    while line.parent.cls != "Block":
        line = line.parent

    resize = matlab2cpp.collection.Resize(line.parent, name=node.name)
    resize.type = type

    i = line.parent.children.index(line)

    ps = line.parent.children
    line.parent.children = ps[:i] + ps[-1:] + ps[i:-1]

    resize.translate(False, only=True)


def error(node, msg, onlyw=False):
    """
Add an error or warning to the log subtree.

Args:
    node (Node): node where error occoured
    msg (str): error message content
    onlyw (bool): if true, use warning instead of error

See also:
    :py:func:`~matlab2cpp.Node.error`
    :py:func:`~matlab2cpp.Node.warning`
    """

    msg = msg % node.properties()

    code = node.program.code
    cur = node.cur
    end = cur+len(node.code)

    start = cur
    while code[start] != "\n" and start != 0:
        start -= 1

    if end >= len(code):
        end = len(code)-1
    finish = end
    while code[finish] != "\n" and finish != len(code)-1:
        finish += 1
    code = code[start:finish]

    pos = cur-start

    name = node.cls + ":" + str(cur)

    errors = node.program[5]

    if name in errors.names:
        return

    if onlyw:
        err = matlab2cpp.collection.Warning(errors, name=name, line=node.line,
                cur=pos, value=msg, code=code)
    else:
        err = matlab2cpp.collection.Error(errors, name=name, line=node.line,
                cur=pos, value=msg, code=code)
    err.backend="program"


def create_declare(node):
    """
Backend for the :py:func:`~matlab2cpp.Node.create_declare` function.

Args:
    node (Node): Node to create declare from

Returns:
    Node : the (newly) declared node
    """

    if not (node is node.declare):
        return node

    if node.cls in reference.structvars:
        if node.cls in ("Nget", "Nset"):
            if node[0].cls == "String":
                return None
            value = node[0].value
        else:
            value = node.value

        structs = node.program[3]
        assert structs.cls == "Structs"

        if node not in structs:
            struct = matlab2cpp.collection.Struct(structs, name=node.name)
        else:
            struct = structs[node]

        if value in struct.names:
            return struct[struct.names.index(value)]

        declares = node.func[0]

        if node.cls in ("Sset", "Sget"):
            sname = "_size"
            if sname not in struct.names:
                matlab2cpp.collection.Counter(struct, sname, value="100")

            if node.name not in declares.names:
                var = matlab2cpp.collection.Var(declares, name=node.name, value=value)
                var.type="structs"
        else:
            if node.name not in declares.names:
                var = matlab2cpp.collection.Var(declares, name=node.name, value=value)
                var.type="struct"

        return matlab2cpp.collection.Var(struct, name=value)
        parent = struct

    else:
        parent = node.func[0]

    if node in parent:
        declare = parent[node]
        declare.type = node.type
        declare.pointer = node.pointer
        return declare

    out = matlab2cpp.collection.Var(parent, name=node.name,
            pointer=node.pointer, value=node.value)
    out.type = node.type
    return out


def suggest_datatype(node):
    """
Backend for the :py:func:`~matlab2cpp.Node.suggest_datatype` function.

Args:
    node (Node): Node to suggest datatype for.

Returns:
    (tuple): Suggestion on the form ``(dim, mem)``

See also:
    :py:func:`~matlab2cpp.Node.suggest_datatype`
    """

    if node.group.cls in ("Transpose", "Ctranspose"):

        dim, mem = suggest_datatype(node.group)
        if dim == 1:
            dim = 2
        elif dim == 2:
            dim = 2
        return dim, mem

    elif node.group.cls == "Assign":

        if node.group[0].num:
            return node.group[0].dim, node.group[0].mem

    elif node.group.cls == "Matrix":

        mems = set([])
        if node.group.value: # decomposed

            ax0, ax1 = len(node.group), len(node.group[0])
            if ax0 > 1:
                if ax1 > 1:
                    dim = 3
                else:
                    dim = 1
            else:
                if ax1 > 1:
                    dim = 2
                else:
                    dim = 0

            for vec in node.group:
                for elem in vec:
                    if elem.num:
                        mems.add(elem.mem)

        # rowvec definition
        elif len(node.group) == 1:

            if len(node.group[0]) == 1:
                return None, None

            for elem in node.group[0]:
                if elem.num:
                    mems.add(elem.mem)
            dim = 3
            
        # colvec definition
        elif len(node.group[0]) == 1:

            for vec in node.group:
                if vec[0].num:
                    mems.add(vec[0].mem)

            dim = 3

        else:

            for vec in node.group:
                for elem in vec:
                    if elem.num:
                        mems.add(elem.mem)

            dim = 3

        if len(mems) == 1:
            return dim, mems.pop()

        elif len(mems) > 1:
            return dim, max(*mems)

        else:
            return None, None


    return None, None


def modify(node, nargin = False):
    # Modify the abstract syntax tree (AST), also try to overload funtions
    # node is project node
    project = node.project
    nodes = flatten(project, False, False, False)

    # remove the nodes for clear, close and clc so they are not included
    # in the translation
    for n in nodes:
        if n.name in ("clear", "close", "clc"):
            index = n.parent.parent.children.index(n.parent)
            del n.parent.parent.children[index]

    # Change right hand side variable to uvec if assigned with find, b = find(a==3)
    for n in nodes:
        if n.cls == "Assign":
            lhs, rhs = n
            if rhs.name == "find":
                declares = n.func[0]
                #print declares.cls
                for var in declares:
                    if var.name == lhs.name:
                        var.type = "uvec"

    # move the "using namespace arma ;" node last in the includes list
    for program in project:
        includes = program[0]
        index = 0

        for include in includes:
            if include != includes[-1] and \
              include.name == "using namespace arma ;":
                includes += [includes.pop(index)] # remove and append arma include node

            index += 1

    # remove nargin if args.nargin == False
    # print args.nargin
    if nargin == False:
        # Remove if statements with nargin
        # node is project
        for program in project:
            # for func in funcs
            funcs = program[1]
            for func in funcs:
                block = func[3]
                
                # find node.name == nargin
                found_nargin = True
                while found_nargin:
                    found_nargin = False
                    nodes = flatten(block, False, False, False)
                    
                    # remove if node.group is branch
                    for n in nodes:
                        if n.name == "nargin":
                            # remove branch
                            if n.group.cls in ("Branch", "Switch"):
                                parent = n.group.parent
                                # print parent.summary()
                                del parent.children[parent.children.index(n.group)]
                                # node.group.parent.children.index(node.group)
                                found_nargin = True
                                break
                            else: # node.group is not a branch
                                found_nargin = False
                                break

    # add temporary variables for multiple return function
    nodes = flatten(project, False, False, False)
    for n in nodes:
        if n.cls == "Get" and n.backend == "func_returns":
            func_name = n.name

            func_ret_num = 0
            if n.parent.cls in ("Assign", "Assigns"):

                for sub_node in n.parent:
                    if sub_node.cls != "Get":
                        func_ret_num += 1
                    else:
                        break
            #print n.summary()

            # find the multiple return function
            # Check if function is in the same program

            # Look first for function in current file
            funcs = n.program[1]
            found_func = False
            func = []
            for f in funcs:
                if f.name == n.name:
                    func_found = True
                    #programs = n.program
                    func = f

            # Look for function in external file
            if found_func == False:
                for program in n.project:
                    f = program[1][0]
                    if f.name == n.name:
                        func = f
                        break
                #programs  = [p[1][0] for p in project if p[1][0]= n.program]


            # add needed temporary variables to params
            if func:
                return_params = func[1]
                # dictionary which is used as a counter
                type_counter = {"int" : 0, "float" : 0, "double" : 0, "uword" : 0, "cx_double" : 0,
                "ivec" : 0, "fvec" : 0, "uvec" : 0, "vec" : 0, "cx_vec" : 0,
                "irowvec" : 0, "frowvec" : 0, "urowvec" : 0, "rowvec" : 0, "cx_rowvec" : 0,
                "imat" : 0, "fmat" : 0, "umat" : 0, "mat" : 0, "cx_mat" : 0,
                "icube" : 0, "fcube" : 0, "ucube" : 0, "cube" : 0, "cx_cube" : 0}

                # add or reuse variables, also add change
                while func_ret_num < len(return_params):
                    if return_params[func_ret_num].type not in ("TYPE", "string"):
                        type_counter[return_params[func_ret_num].type] += 1
                        name = "_tmp_" + return_params[func_ret_num].type + \
                               str(type_counter[return_params[func_ret_num].type])

                        # Allocate Var node. n.parent is the assign node
                        swap_var = matlab2cpp.collection.Var(n.parent, name)
                        swap_var.type = return_params[func_ret_num].type
                        swap_var.backend = return_params[func_ret_num].backend
                        swap_var.create_declare()

                        # swap Var and Get (function_returns)
                        n.parent.children[func_ret_num] = swap_var
                        n.parent.children[-1] = n

                    #index += 1
                    func_ret_num += 1

    
# small hack to ensure that log isn't cleaned mid translation
mid_translation = [0]
def translate(node, opt=None):
    """
Backend for performing translation of subtree

Args:
    node (Node): Root of the translation
    opt (argparse.Namespace, optional): optional arguments from frontend

See also:
    :py:func:`~matlab2cpp.Node.translate`
    """

    # translate for every program
    if node.cls == "Project":
        map(translate, node)
        return node

    if mid_translation[0] == 0:
        log = node.program[5]
        log.children = []

    mid_translation[0] += 1

    nodes = flatten(node, False, True, False)
    if not (opt is None) and opt.disp:
        print "iterating %d nodes" % len(nodes)

    for node in nodes[::-1]:
        translate_one(node, opt)

    mid_translation[0] -= 1

    if not mid_translation[0]:
        logs = flatten(log, False, True, False)
        for node in logs[::-1]:
            translate_one(node, opt)
    
    return node


def translate_one(node, opt):
    """
Backend for performing translation of single node

Args:
    node (Node): Node to perform translation on
    opt (argparse.Namespace, optional): optional arguments from frontend

See also:
    :py:func:`~matlab2cpp.Node.translate`
    """

    # e.g. Get_a from user
    value = node.program.parent.kws.get(node.cls+"_"+node.name, None)

    # e.g. Get from user
    if value is None:
        value = node.program.parent.kws.get(node.cls, None)

    if value is None:
        
        backend = node.backend
        if backend == "TYPE":
            backend = "unknown"

        target = matlab2cpp.rules.__dict__["_"+backend]
        spesific_name = node.cls + "_" + node.name

        # e.g. Get_a (reserved typically)
        if spesific_name in target.__dict__:
            value = target.__dict__[spesific_name]

        # e.g. Get (normal behavior)
        elif node.cls in target.__dict__:
            value = target.__dict__[node.cls]

        else:
            print node.program.summary()
            raise KeyError(
                    "Expected to find rule for '%s' in the file '_%s.py'" %\
                            (node.cls, node.backend))


    # let rule create a translation
    if not isinstance(value, (unicode, str, list, tuple)):
        value = value(node)

    # not quite right format
    if isinstance(value, (unicode, matlab2cpp.node.frontend.Node)):
        value = str(value)

    elif value is None:
        raise ValueError(
"missing return in function %s in file %s" % (node.cls, node.backend))

    node.ret = repr(value)

    # interpolate tuples/lists
    if not isinstance(value, str):

        value = list(value)
        children = ["%("+str(i)+")s" for i in xrange(len(node))]

        if len(value) == 2:
            value.insert(1, "")

        value = value[:-1] + [value[-2]] *\
            (len(children)-len(value)+1) + value[-1:]

        if len(children) == 0:
            value = value[0] + value[-1]

        elif len(children) == 1:
            value = value[0] + children[0] + value[-1]

        else:

            out = value[0]
            for i in xrange(len(children)):
                out += children[i] + value[i+1]
            value = out

    # interperlate string
    try:
        value = value % node.properties()
    except:
        raise SyntaxError("interpolation in " + node.backend + "." +\
                node.cls + " is misbehaving\n'" + value + "'\n" +\
                str(node.prop)  + "\nCrash on line " + str(node.line) +\
                ":\n" + node.code)

    if node.cls in ("Assign", "Assigns", "Statement") and node.project.builder.original:
        value = "// " + node.code + "\n" + value
        value = value.replace("%", "__percent__")
    node.str = value


def include(node, name, **kws):
    """
Backend for the :py:func:`~matlab2cpp.Node.include` function.

Args:
    node (Node): node in program where to where the header is placed
    name (str): name of header
    **kws (str, optional): Optional args for header. Mostly not in use.

See also:
    :py:func:`~matlab2cpp.Node.include`
    """

    if os.path.isfile(name):

        name = os.path.relpath(name, os.path.dirname(node.program.name))
        include_code = '#include "%s.hpp"' % name
        library_code = ""

        if node.name == name:
            include_code = ""

    else:

        library_code = ""
        if name == "SPlot":
            include_code = '#include "SPlot.h"'

            #check if file in directory
            try:
                file_path = node.program[1].name
                index = file_path.rindex(sep)
                output_file_path = file_path[:index] + sep + "SPlot.h"

                #if mconvert.h not found in directory, create the file
                if not os.path.isfile(output_file_path):
                    f = open(output_file_path, "w")
                    f.write(matlab2cpp.pyplot.code)
                    f.close()
            except:
                pass
                

        elif name == "m2cpp":
            include_code = '#include "mconvert.h"'

            #check if file in directory
            try:
                file_path = node.program[1].name
                index = file_path.rindex(sep)
                output_file_path = file_path[:index] + sep + "mconvert.h"

                #if mconvert.h not found in directory, create the file
                if not os.path.isfile(output_file_path):
                    f = open(output_file_path, "w")
                    f.write(matlab2cpp.m2cpp.code)
                    f.close()
            except:
                pass
                
        elif name == "arma":
            include_code = "#include <armadillo>"
        elif name == "iostream":
            include_code = "#include <iostream>"
        elif name == "cmath":
            include_code = "#include <cmath>"
        elif name == "algorithm":
            include_code = "#include <algorithm>"
        elif name == "omp":
            include_code = "#include <omp.h>"
        elif name == "tbb":
            include_code = "#include <tbb/parallel_for.h>"
        else:
            include_code = ""

    includes = node.program[0]
    if include_code and include_code not in includes.names:
        include = matlab2cpp.collection.Include(includes, include_code,
                value=includes.value)
        include.backend="program"

    inlines_ = node.program[2]
    if library_code and library_code not in inlines_.names:
        inline = matlab2cpp.collection.Inline(inlines_, library_code)
        inline.backend="program"


def wall_clock(node):
    """
Backend for the :py:func:`~matlab2cpp.Node.wall_clock` function.

Args:
    node (Node):
        node in function where ``wall_clock _timer`` should be declared.

See also:
    :py:func:`~matlab2cpp.Node.wall_clock`
    """
    declares = node.func[0]
    if "_timer" not in declares:
        clock = matlab2cpp.collection.Var(declares, name="_timer")
        clock.type="wall_clock"


def plotting(node):
    """
Backend of the :py:func:`~matlab2cpp.Node.plotting` function.

Args:
    node (Node): node in the function where plotting should be implemented.

See also:
    :py:func:`~matlab2cpp.Node.plotting`
    """

    declares = node.func[0]

    # only do this once
    if "_plot" in declares:
        return

    # add splot to header
    node.include("SPlot")

    # add a variable for Splot in declare
    var = matlab2cpp.collection.Var(declares, name="_plot")
    var.type = "SPlot"

    # get function variable
    func = node.func
    
    # get function block
    block = func[3]

    # create new statement
    statement = matlab2cpp.collection.Statement(block, code="")
    statement.backend="code_block"
    # fill it with new Get _splot
    get = matlab2cpp.collection.Get(statement, name="_splot")
    get.backend="reserved"

    # translate the new nodes
    statement.translate()

    # swap with last statement, if it is a return-statement
    if len(block)>1 and block[-2] and block[-2][0].cls == "Return":
        block.children[-1], block.children[-2] = \
                block.children[-2], block.children[-1]

