import collection

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


def set_cfg(program, cfg):

    structs = program[1]
    for name in cfg.keys():

        if name in program.names[2:]:

            cfg_ = cfg[name]
            func = program[program.names.index(name)]
            declares, returns, params = func[0], func[1], func[2]

            for key in cfg_.keys():

                if key in declares.names:
                    var = declares[declares.names.index(key)]
                    var.type = cfg_[key]

                if key in params.names:
                    var = params[params.names.index(key)]
                    var.type = cfg_[key]

                elif key in returns.names:
                    var = returns[returns.names.index(key)]
                    var.type = cfg_[key]

        elif name in structs.names:

            cfg_ = cfg[name]
            struct = structs[structs.names.index(name)]

            for key in cfg_.keys():

                if key in struct.names:
                    var = struct[struct.names.index(key)]
                    var.type = cfg_[key]

                else:
                    var = collection.Declare(struct, key)
                    var.backend = "struct"
                    var.type = cfg_[key]


def get_cfg(program):
    "Retrieve datatype and suggestions from tokentree"
    cfg = {}
    scfg = {}
    for func in program[2:]:

        cfg[func["name"]] = cfg_ = {}
        scfg[func["name"]] = scfg_ = {}

        declares, params = func[0], func[2]
        for var in declares[:]+params[:]:

            if var["name"][:1] == "_":
                continue

            type = var.prop["type"]
            if type == "TYPE":
                type = ""
            cfg_[var["name"]] = type

            if not type:

                type = var.prop["suggest"]
                if type == "TYPE":
                    type = ""
                if type:
                    scfg_[var["name"]] = type

    for struct in program[1]:

        cfg[struct["name"]] = cfg_ = {}
        scfg[struct["name"]] = scfg_ = {}

        for var in struct:

            type = var.prop["type"]
            if type == "TYPE":
                type = ""
            cfg_[var["name"]] = type

            if not type:

                type = var.prop["suggest"]
                if type == "TYPE":
                    type = ""
                if type:
                    scfg_[var["name"]] = type

    return cfg, scfg



def str_cfg(cfg, scfg={}, struct_cfg={}):

    out = "scope = {}\n\n"

    keys = cfg.keys()
    keys.sort()

    for name in keys:
        out += '%s = scope["%s"] = {}\n' % (name, name)
        cfg_ = cfg[name]

        for key, val in cfg_.items():
            if val:
                out += '%s["%s"] = "%s"\n' % (name, key, val)
            else:
                suggest = scfg.get(name, {}).get(key, "")
                if suggest:
                    out += '%s["%s"] = "" # %s\n' % (name, key, suggest)
                else:
                    out += '%s["%s"] = ""\n' % (name, key)
        out += "\n"

    return out



def summary(node, opt):

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

