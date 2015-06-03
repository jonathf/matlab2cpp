def configure_arg(node, index):

    out = "%(" + str(index) + ")s"

    if node.cls == "All":
        return "span::all", 1
    elif node.type == "TYPE":
        return out, -1

    if node.dim == 0:
        out = out + "-1"
        dim = 0
    else:
        dim = 1
        if node.cls != "Colon":
            out = out + "-1"

    if node.mem != 0 and node.dim != 0:
        node.auxiliary((node.dim, 0), convert=True)

    if node.dim == 2:
        out = out + ".t()"

    elif node.dim > 2:
        out = "vectorise(" + out + ")"

    return out, dim

