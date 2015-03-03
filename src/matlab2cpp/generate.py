import targets

def code(tree, includes, cfg):

    tree.index = 0
    tree["includes"] = includes
    for node in tree.children:
        node.cfg = cfg[node["name"]]
        codegen(node)

    return targets.program.Program(tree)

def process(node):

    value = node
    while isinstance(value, inode.Node):
        node = value
        value = node.call()
    node["str_"] = str(value)

    backend = node["backend"]
    cls = node["class"]
    name = node["name"]

    # Defining the parameters
    params = {"name":name, "class":cls,
            "value":node.prop.get("value", "")}
    I = len(node)
    for i in xrange(I):
        params["%d" % i] = params["-%d" % (I-i)] = node[i]["str"]

    if value is None:
        raise ValueError, "missing return in %s.%s" % (backend, cls)

    if not isinstance(value, str):

        value = list(value)
        children = ["%("+str(i)+")s" for i in xrange(len(node))]

        if len(value)==2:
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
        value = value % params
    except:
        raise SyntaxError, "interpolation in "+backend+"."+\
            cls+" is misbehaving\n"+ value+"\n"+str(params)

    return value

def codegen(node):

    for n in node.children:
        codegen(n)

    if node["stop"]:
        node["stop"] = None
    elif node.prop.has_key("str"):
        return

    node["str"] = process(node)

    if node.type() == "TYPE" and node["backend"] != "unknown":
        node.type([n.type() for n in node[:]])


import node as inode
