import translations
import collection
import datatype
import reference
import supplement

def flatten(node, ordered=False, reverse=False, inverse=False):
    r"""
Return a list of all nodes

Tree:
  A
  |\
  B C
 /| |\
D E F G

Sorted [o]rdered, [r]everse and [i]nverse:

ori :
    : A B D E C F G
o   : A B C D E F G
 r  : A C G F B E D
  i : D E B F G C A
or  : A C B G F E D
o i : D E F G B C A
 ri : E D B G F C A
ori : G F E D C B A

Parameters
----------
node : Node
    Root node to start from
ordered : bool
    If True, make sure the nodes are hierarcically ordered.
    If False, nodes are sorted for easy print.
reverse : bool
    If True, children are itterated in reverse order.
    """

    o = bool(ordered)
    r = bool(reverse)
    i = bool(inverse)

    out = []

    if o:

        nodes = [node]
        for node in nodes:
            nodes.extend(node.children[::1-2*(r^i)])
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




def node_summary(node, opt):

    nodes = flatten(node, False, False, False)
    if not (opt is None) and opt.disp:
        print "iterating %d nodes" % len(nodes)

    if not (opt is None) and not (opt.line is None):
        for node in nodes:
            if node.cls != "Block" and node.line == opt.line:
                node = node
                break

    indent = [node]
    out = ""
    for node in nodes:

        while indent and not (node.parent is indent[-1]):
            indent.pop()

        space = "| "*(len(indent)-1)
        out += "%3d %3d %s%-10s %-12s %-7s %-18s" % \
                (node.line, node.cur, space, node.cls,
                        node.backend, node.type, node.name)
        out += repr(node.ret) + "\n"
        indent.append(node)

    return out


def node_translate(node, opt):

    target = translations.__dict__["_"+node.backend]
    spesific_name = node.cls + "_" + node.name

    if spesific_name in target.__dict__:
        value = target.__dict__[spesific_name]

    elif node.cls in target.__dict__:
        value = target.__dict__[node.cls]

    else:
        print node.program.summary()
        raise KeyError("no %s in %s" % (node.cls, node.backend))


    if not isinstance(value, (unicode, str, list, tuple)):
        value = value(node)

    if isinstance(value, (unicode, Node)):
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
    # print repr(value)

    node.prop["str"] = value


def create_auxillary(node, type, convert):

    assert node.parent["class"] != "Assign",\
            ".auxiliary() must be triggered mid expression."

    type = type or node.type

    if not isinstance(type, str):
        if isinstance(type[0], int):
            type = datatype.get_name(*type)
        else:
            type = datatype.common_strict(type)

    if type == "TYPE":
        return node

    matrix_mode = False
    if node.cls == "Matrix":
        matrix_mode = True
        type = "uvec"

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
        assign = collection.Assign(block, type=type, backend="matrix")
    else:
        assign = collection.Assign(block, type=type)

    # Return value
    aux_var = collection.Var(assign, var, backend=type, type=type)
    aux_var.create_declare()

    if convert:
        rhs = collection.Get(assign, "_conv_to", type=type)
    else:
        rhs = assign

    swap_var = collection.Var(rhs, var, type=type)
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
    swap_var.translate_node()
    aux_var.translate_node()
    if convert:
        rhs.translate_node()
    assign.translate_node()

    if convert:
        assert node.type != swap_var.type

    return swap_var


def create_resize(node):

    if node["_resize"]:
        return
    node["_resize"] = True

    type = node.type
    node.dim = 3

    line = node
    while line.parent.cls != "Block":
        line = line.parent

    resize = collection.Resize(line.parent, name=node.name, type=type)

    i = line.parent.children.index(line)

    ps = line.parent.children
    line.parent.children = ps[:i] + ps[-1:] + ps[i:-1]

    resize.translate_node(False)


def create_error(node, msg, onlyw=False):

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

    name = "%010d" % cur + node.cls
    errors = node.program.parent[1]

    if name not in errors.names:
        if onlyw:
            collection.Warning(errors, name=name,
                    line=node.line, cur=pos, value=msg, code=code)
        else:
            collection.Error(errors, name=name,
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

        structs = node.program[1]
        assert structs.cls == "Structs"

        if node not in structs:
            struct = collection.Struct(structs, name=node.name)
        else:
            struct = structs[node]

        if value in struct.names:
            return struct[struct.names.index(value)]

        declares = node.func[0]

        if node.cls in ("Sset", "Sget"):
            sname = "_"+value+"_size"
            if sname not in struct.names:
                collection.Counter(struct, sname, value="100")

            collection.Var(declares, name=node.name, value=value, type="structs")
        else:
            collection.Var(declares, name=node.name, value=value, type="struct")

        return collection.Var(struct, name=value)
        parent = struct

    else:
        parent = node.func[0]

    if node in parent:
        declare = parent[node]
        declare.type = node.type
        declare.pointer = node.pointer
        return declare

    return collection.Var(parent, name=node.name,
            type=node.type, pointer=node.pointer, value=node.value)


def translate(node, opt=None):
    nodes = flatten(node, False, True, False)
    if not (opt is None) and opt.disp:
        print "iterating %d nodes" % len(nodes)

    for node in nodes[::-1]:
        node.translate_node(opt)

    return node.prop["str"]


def build(code, disp=False, retall=False, suggest=False, comments=False):

    code = code + "\n\n\n\n"
    tree = treebuilder.Treebuilder("", disp=disp, comments=comments)
    tree.code = code
    tree.create_program("unnamed")
    tree.configure(2*suggest)
    if retall:
        return tree
    if tree[2][2].name == "main":
        out = tree[2][2][3]
        del out.children[0]
        return out
    return tree[2]


def qtranslate(code, suggest=True):
    return translate(build(code, suggest=suggest))

def qsupplement(code, suggest=True):
    tree = build(code, suggest=suggest, retall=True)
    types, suggestions = supplement.get_variables(tree[2])
    return supplement.str_variables(types, suggestions, header=False)

def qlogging(code):
    pass


from node import Node
import treebuilder
