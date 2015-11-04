import re
import math

import reference
import matlab2cpp

def flatten(node, ordered=False, reverse=False, inverse=False):

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

    indent = [node]
    outl = []

    nl = int(math.log10(nodes[-1].line+1))
    nc = int(math.log10(len(nodes[0].code) or 1))

    for node in nodes:

        out = ""


        if node.line:
            nl_ = int(math.log10(node.line))+1
            out += " "*(nl-nl_) + str(node.line) + " "
            nc_ = int(math.log10(node.cur or 1))+1
            out += " "*(nc-nc_) + str(node.cur+1)
        else:
            out += " "*(nl+nc+2)

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

    assert node.parent["class"] != "Assign",\
            ".auxiliary() must be triggered mid expression."

    type = type or node.type

    if not isinstance(type, str):
        if isinstance(type[0], int):
            type = matlab2cpp.datatype.get_name(*type)
        else:
            type = matlab2cpp.datatype.common_strict(type)

    # if type == "TYPE":
    #     return node

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
    var = "_aux_" + type + "_"
    if var not in line.prop:
        line.prop[var] = 1
    else:
        line.prop[var] += 1
    var = var + str(line.prop[var])

    # Create Assign
    if matrix_mode:
        assign = matlab2cpp.collection.Assign(block, type=type, backend="matrix")
    else:
        assign = matlab2cpp.collection.Assign(block, type=type)

    # Return value
    aux_var = matlab2cpp.collection.Var(assign, var, backend=type, type=type)
    aux_var.create_declare()

    if convert:
        rhs = matlab2cpp.collection.Get(assign, "_conv_to", type=type)
    else:
        rhs = assign

    swap_var = matlab2cpp.collection.Var(rhs, var, type=type)
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
    swap_var.translate(only=True)
    aux_var.translate(only=True)
    if convert:
        rhs.translate(only=True)
    assign.translate(only=True)

    if convert:
        assert node.type != swap_var.type

    return swap_var



def resize(node):

    if node["_resize"]:
        return
    node["_resize"] = True

    type = node.type
    node.dim = 3

    line = node
    while line.parent.cls != "Block":
        line = line.parent

    resize = matlab2cpp.collection.Resize(line.parent, name=node.name, type=type)

    i = line.parent.children.index(line)

    ps = line.parent.children
    line.parent.children = ps[:i] + ps[-1:] + ps[i:-1]

    resize.translate_one(False)


def error(node, msg, onlyw=False):

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
        matlab2cpp.collection.Warning(errors, name=name,
                line=node.line, cur=pos, value=msg, code=code)
    else:
        matlab2cpp.collection.Error(errors, name=name,
                line=node.line, cur=pos, value=msg, code=code)


def create_declare(node):

    if not (node is node.declare):
        return node

    if node.cls in reference.structvars:
        if node.cls in ("Nget", "Nset"):
            if node[0].cls == "String":
                return None
            value = node[0]["value"]
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

            matlab2cpp.collection.Var(declares, name=node.name, value=value, type="structs")
        else:
            matlab2cpp.collection.Var(declares, name=node.name, value=value, type="struct")

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
            type=node.type, pointer=node.pointer, value=node.value)
    return out


def suggest_datatype(node):

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

        elif len(node.group) == 1:

            if len(node.group[0]) == 1:
                return None, None

            dim = 1

            for elem in node.group[0]:
                if elem.num:
                    mems.add(elem.mem)
                    if elem.dim > 1:
                        dim = 3

            if not mems:
                return None, None

        elif len(node.group[0]) == 1:

            dim = 2

            for vec in node.group:
                if vec.num:
                    mems.add(vec.mem)
                    if vec.dim not in (0, 2):
                        dim = 3

        if len(mems) == 1:
            return dim, mems.pop()

        elif len(mems) > 1:
            return dim, max(*mems)

    return None, None


def translate(node, opt=None):

    if node.cls == "Project":
        map(translate, node)
        return node

    log = node.program[5]
    log.children = []

    nodes = flatten(node, False, True, False)
    if not (opt is None) and opt.disp:
        print "iterating %d nodes" % len(nodes)

    for node in nodes[::-1]:
        translate_one(node, opt)

    logs = flatten(log, False, True, False)
    for node in logs[::-1]:
        translate_one(node, opt)

    return node


def translate_one(node, opt):

    if node.program.parent.kws.get(node.cls, None):

        value = node.program.parent.kws.get(node.cls, None)

    else:

        backend = node.backend
        if backend == "TYPE":
            backend = "unknown"

        target = matlab2cpp.rules.__dict__["_"+backend]
        spesific_name = node.cls + "_" + node.name

        if spesific_name in target.__dict__:
            value = target.__dict__[spesific_name]

        elif node.cls in target.__dict__:
            value = target.__dict__[node.cls]

        else:
            print node.program.summary()
            raise KeyError(
                    "Expected to find rule for '%s' in the file '_%s.py'" %\
                            (node.cls, node.backend))


    if not isinstance(value, (unicode, str, list, tuple)):
        value = value(node)

    if isinstance(value, (unicode, matlab2cpp.node.frontend.Node)):
        value = str(value)

    elif value is None:
        raise ValueError(
"missing return in function %s in file %s" % (node.cls, node.backend))

    node.ret = repr(value)

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

    try:
        value = value % node.properties()
    except:
        raise SyntaxError("interpolation in " + node.backend + "." +\
                node.cls + " is misbehaving\n'" + value + "'\n"+str(node.prop))

    node.str = value


def include(node, name, **kws):

    include_code, library_code = matlab2cpp.inlines.retrieve(node, name, **kws)

    includes = node.program[0]
    if include_code and include_code not in includes.names:
        matlab2cpp.collection.Include(includes, include_code, value=includes.value)

    inlines_ = node.program[2]
    if library_code and library_code not in inlines_.names:
        matlab2cpp.collection.Inline(inlines_, library_code)


def wall_clock(node):
    declares = node.func[0]
    if "_timer" not in declares:
        matlab2cpp.collection.Var(declares, name="_timer", type="wall_clock")
