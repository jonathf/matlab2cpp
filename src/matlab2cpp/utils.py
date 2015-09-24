#!/usr/bin/env python
# encoding: utf-8

"""
Not all translation is carried out successfully. There are many reasons for
this. The most basic is to provide the interpreter with invalid Matlab code.
For example if one provides invalid Matlab code to the interpreter, it will
create an error:

    >>> print mc.qcpp("a**b")
    Traceback (most recent call last):
        ...
    SyntaxError: line 1 in Matlab code:
    a**b
      ^
    Expected: expression start

The interpreter highlights the line it crashed on and explain as far as it can
why it crashed. In this example `**` is not a valid operator and the
interpreter expects an expression after the first `*`.

Beyond the invalid syntax, the interpreter is able to construct a full tree
representation of the code, which is then converted into C++ code.  The basic
translation will as far as possible make a full translation. For example:

    >>> print mc.qhpp("function f(x)")
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    void f(TYPE x)
    {
      // Empty block
    }

Without a context, the variable type of `x` in the function argument is unknown.
The default data type `TYPE` is therefore used. This obviously isn't correct,
but is a filler such that the data type can be defined later through for example
the `.py` file. In addition, the error is logged. The function `mc.qlog` can be
used to observe this log:

    >>> print mc.qlog("function f(x)")
    Error in class Var on line 1:
    function f(x)
               ^
    unknown data type

The error specifies the line number, the class of the node, points at the
location in the line and a short message about what the problem is. This allows
the user easy access to the problems that program had during translation.
"""

import translations
import collection
import datatype
import reference
import supplement
import re

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




def node_summary(node, opt):

    nodes = flatten(node, False, False, False)
    if not (opt is None) and opt.disp:
        print "iterating %d nodes" % len(nodes)

    
    if not (opt is None) and not (opt.line is None):
        for node in nodes:
            if node.cls != "Block" and node.line == opt.line:
                nodes = flatten(node, False, False, False)
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
        if node.parent.cls in ("Program", "Project", "Includes"):
            out += "\n"
        elif node.parent.cls == "Log":
            out += repr(node.code[:30]) + " -> " + repr(node.value) + "\n"
        else:
            out += repr(node.code[:30]) + " -> " + repr(node.ret[:30]) + "\n"

        indent.append(node)

    out = re.sub(r"(\\n){2,}", "", out)

    return out


def node_translate(node, opt):

    backend = node.backend
    if backend == "TYPE":
        backend = "unknown"

    target = translations.__dict__["_"+backend]
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
    errors = node.program[5]

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

        structs = node.program[3]
        assert structs.cls == "Structs"

        if node not in structs:
            struct = collection.Struct(structs, name=node.name)
        else:
            struct = structs[node]

        if value in struct.names:
            return struct[struct.names.index(value)]

        declares = node.func[0]

        if node.cls in ("Sset", "Sget"):
            sname = "_size"
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

    out = collection.Var(parent, name=node.name,
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
    nodes = flatten(node, False, True, False)
    if not (opt is None) and opt.disp:
        print "iterating %d nodes" % len(nodes)

    for node in nodes[::-1]:
        node.translate_node(opt)

    return node


def build(code, disp=False, retall=False, suggest=False, comments=False):

    code = code + "\n\n\n\n"
    tree = treebuilder.Treebuilder(disp=disp, comments=comments)
    tree.load("unamed", code)
    tree.configure(2*suggest)
    if retall:
        return tree
    if tree[0][1][0].name == "main":
        out = tree[0][1][0][3]
        return out
    return tree[0]


def qcpp(code, suggest=True):
    """
Quick code translation of matlab script to C++ executable.
It is the simplest way of translating code.

Args:
    code (str, Node): A string or tree representation of Matlab code.

Kwargs:
    suggest (bool): If true, use the suggest engine to guess data types.

Returns:
    str: Best estimate of script. If code is a module, return an empty string.

Example:

    >>> print mc.qcpp("a = 4; b = 5.; c = 'abc'", suggest=False)
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    int main(int argc, char* argv[])
    {
      TYPE a, b, c ;
      a = 4 ;
      b = 5. ;
      c = "abc" ;
      return 0 ;
    }
    >>> print mc.qcpp("a = 4; b = 5.; c = 'abc'", suggest=True)
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    int main(int argc, char* argv[])
    {
      int a ;
      double b ;
      string c ;
      a = 4 ;
      b = 5. ;
      c = "abc" ;
      return 0 ;
    }
    """

    if isinstance(code, str):
        tree = build(code, suggest=suggest, retall=True)[0]
        translate(tree)
    else:
        tree = code
        if isinstance(tree, treebuilder.Treebuilder):
            tree = tree[0]

    out = ""
    if tree[1] and tree[1][0].name == "main":
        out += tree[0].str
        if out:
            out += "\n\n"
        out += tree[1].str

        out = out.replace("__percent__", "%")

    return out


def qhpp(code, suggest=False):
    """
Quick module translation of matlab script to C++ executable.
It is the simplest way of translating code.

Args:
    code (str, Node): A string or tree representation of Matlab code.

Kwargs:
    suggest (bool): If true, use the suggest engine to guess data types.

Returns:
    str: Best estimate of script. If code is a module, return an empty string.

Example:

    """

    if isinstance(code, str):
        tree = build(code, suggest=suggest, retall=True)[0]
        translate(tree)

    else:
        tree = code
        if isinstance(tree, treebuilder.Treebuilder):
            tree = tree[0]

    out = ""
    if tree[1] and tree[1][0].name == "main":

        if len(tree[4]) > 1:
            out += tree[4].str + "\n\n"

        if tree[2].str:
            out += tree[2].str + "\n\n"

        if tree[3].str:
            out += tree[3].str + "\n\n"

        if out[-2:] == "\n\n":
            out = out[:-2]

    else:
        if tree[0]:
            out += tree[0].str + "\n\n"

        if tree[3].str:
            out += tree[3].str + "\n\n"

        if tree[2].str:
            out += tree[2].str + "\n\n"

        if len(tree[4]) > 1:
            out += tree[4].str + "\n\n"

        out += tree[1].str

    out = out.replace("__percent__", "%")

    return out


def qpy(code, suggest=True, prefix=False):

    if isinstance(code, str):
        tree = build(code, suggest=suggest, retall=True)[0]

    else:
        tree = code
        if isinstance(tree, treebuilder.Treebuilder):
            tree = tree[0]

    tf, ts, ti, sugs = supplement.get_variables(tree)
    out = supplement.str_variables(tf, ts, ti, sugs, prefix=prefix)
    out = out.replace("__percent__", "%")

    return out


def qlog(code, suggest=False):

    if isinstance(code, str):
        tree = build(code, suggest=suggest, retall=True)[0]
        translate(tree)

    else:
        tree = code
        if isinstance(tree, treebuilder.Treebuilder):
            tree = tree[0]

    out = tree[5].str
    out = out.replace("__percent__", "%")

    return out

def qtree(code, suggest=False):

    if isinstance(code, str):
        tree = build(code, suggest=suggest, retall=True)[0]
        translate(tree)

    else:
        tree = code
        if isinstance(tree, treebuilder.Treebuilder):
            tree = tree[0]

    return tree.summary()


from node import Node
import treebuilder

if __name__ == "__main__":
    import matlab2cpp as mc
    import doctest
    doctest.testmod()
