Paren = "(%(0)s)"

def End(node):

    pnode = node
    while pnode.parent.cls not in \
            ("Get", "Cget", "Nget", "Fget", "Sget",
            "Set", "Cset", "Nset", "Fset", "Sset", "Block"):
        pnode = pnode.parent

    if pnode.cls == "Block":
        node.error("Superfluous end-statement")
        return "end"

    index = pnode.parent.children.index(pnode)
    name = pnode = pnode.parent.name

    if index == 0:
        return name + ".n_rows"
    elif index == 1:
        return name + ".n_cols"
    elif index == 2:
        return name + ".n_slices"
    else:
        node.error("end statement in arg>3")

Break = "break"

def Return(node):
    func = node.func
    if func["backend"] == "func_returns":
        return "return"

    if func["backend"] == "func_lambda":
        return "return _retval"

    return "return " + func[1][0]["name"]


# simple operators
def Mul(node):

    if node.type == "TYPE":
        return "", "*", ""

    if not node.num:
        node.error("non-numerical multiplication %s" % str([n.type for n in node]))
        return "", "*", ""

    dim = node[0].dim
    for child in node[1:]:

        if dim == 0:
            dim = child.dim

        if dim == 1:
            if child.dim == 0:
                dim = 1
            elif child.dim == 1:
                child.error("multiplication shape mismatch, colvec*colvec")
            elif child.dim == 2:
                dim = 3
            elif child.dim == 3:
                child.error("multiplication shape mismatch, colvec*matrix")
            elif child.dim == 4:
                child.error("multiplication shape mismatch, colvec*cube")

        elif dim == 2:
            if child.dim == 0:
                dim = 2
            elif child.dim == 1:
                dim = 0
            elif child.dim == 2:
                child.error("multiplication shape mismatch, rowvec*rowvec")
            elif child.dim == 3:
                dim = 3

        elif dim == 3:
            if child.dim == 0:
                dim = 3
            elif child.dim == 1:
                dim = 1
            elif child.dim == 2:
                child.error("multiplication shape mismatch, matrix*rowvec")
            elif child.dim == 3:
                dim = 3

    node.dim = dim

    return "", "*", ""

def Elmul(node):
    if node.type == "TYPE":
        return "", ".*", ""

    if not node.num:
        node.error("non-numerical multiplication %s" % str([n.type for n in node]))
        return "", ".*", ""

    if node.dim == 0:
        return "", "*", ""

    return "", "__percent__", ""

def Plus(node):
    if not node.num:
        node.error("non-numerical addition %s" % str([n.type for n in node]))
    return "", "+", ""

def Minus(node):
    return "", "-", ""

Gt      = "", ">", ""
Ge      = "", ">=", ""
Lt      = "", "<", ""
Le      = "", "<=", ""
Ne      = "", "~=", ""
Eq      = "", "==", ""
Band    = "", "&&", ""
Land    = "", "&", ""
Bor     = "", "||", ""
Lor     = "", "|", ""

def Elementdivision(node):

    if node.type == "TYPE":
        return "", "/", ""

    out = str(node[0])
    mem = node[0].mem

    for child in node:
        if child.mem < 2 and mem < 2:
            out = out + "*1./" + str(child)
            mem = 2
        else:
            out = out + "/" + str(child)
        mem = max(mem, child.mem)

    return out

def Leftelementdivision(node):

    if node.type == "TYPE":
        return "", "/", ""

    out = str(node[-1])
    mem = node[-1].mem

    for child in node[-2::-1]:
        if child.mem < 2 and mem < 2:
            out = str(child) + "*1./" + out
            mem = 2
        else:
            out = str(child) + "/" + out
    
    return out


def Matrixdivision(node):

    if node.type == "TYPE":
        return "", "/", ""

    out = str(node[0])
    mem = node[0].mem
    dim = node[0].dim

    if {n.dim for n in node} == {0}:

        for child in node[1:]:
            if child.mem < 2 and mem < 2:
                out = out + "*1./" + str(child)
                mem = 2
            else:
                out = out + "/" + str(child)
            mem = max(mem, child.mem)

    else:

        for child in node[1:]:

            if child.dim == 3:
                out = "arma::solve(" + str(child) + ".t(), " + out + ".t()).t()"

            elif child.mem < 2 and mem < 2:
                out = out + "*1./" + str(child)
                mem = 2

            else:
                out = out + "/" + str(child)
            mem = max(mem, child.mem)

            if dim == 0:
                dim = child.dim

            elif dim == 1:
                if child.dim == 0:
                    dim = 1
                elif child.dim == 1:
                    node.error("Matrix division error 'colvec\\colvec'")
                elif child.dim == 2:
                    dim = 3
                elif child.dim == 3:
                    node.error("Matrix division error 'colvec\\matrix'")
                elif child.dim == 3:
                    node.error("Matrix division error 'colvec\\cube'")

            elif dim == 2:
                if child.dim == 0:
                    dim = 2
                elif child.dim == 1:
                    dim = 0
                elif child.dim == 2:
                    node.error("Matrix division error 'rowvec\\rowvec'")
                elif child.dim == 3:
                    dim = 2
                elif child.dim == 4:
                    dim = 3

            elif dim == 3:
                if child.dim == 0:
                    dim = 3
                elif child.dim == 1:
                    dim = 1
                elif child.dim == 2:
                    node.error("Matrix division error 'matrix\\rowvec'")
                elif child.dim == 3:
                    dim = 3
                elif child.dim == 4:
                    dim = 4

    node.type = (dim, mem)

    return out

def Leftmatrixdivision(node):

    if node.type == "TYPE":
        return "", "/", ""

    out = str(node[0])
    mem = node[0].mem
    dim = node[0].dim

    if {n.dim for n in node} == {0}:

        for child in node[1:]:
            if child.mem < 2 and mem < 2:
                out = str(child) + "*1./" + out
                mem = 2
            else:
                out = out + "/" + str(child)
            mem = max(mem, child.mem)

    else:

        for child in node[1:]:

            if child.dim == 3:
                out = "arma::solve(" + out + ", " + str(child) + ")"

            elif child.mem < 2 and mem < 2:
                out = str(child) + "*1./" + out
                mem = 2

            else:
                out = str(child) + "/" + out

            mem = max(mem, child.mem)

            if dim == 0:
                dim = node.dim

            elif dim == 1:
                if node.dim == 0:
                    dim = 1
                elif node.dim == 1:
                    node.error("Matrix division error 'colvec\\colvec'")
                elif node.dim == 2:
                    dim = 3
                elif node.dim == 3:
                    node.error("Matrix division error 'colvec\\matrix'")
                elif node.dim == 3:
                    node.error("Matrix division error 'colvec\\cube'")

            elif dim == 2:
                if node.dim == 0:
                    dim = 2
                elif node.dim == 1:
                    dim = 0
                elif node.dim == 2:
                    node.error("Matrix division error 'rowvec\\rowvec'")
                elif node.dim == 3:
                    dim = 2
                elif node.dim == 4:
                    dim = 3

            elif dim == 3:
                if node.dim == 0:
                    dim = 3
                elif node.dim == 1:
                    dim = 1
                elif node.dim == 2:
                    node.error("Matrix division error 'matrix\\rowvec'")
                elif node.dim == 3:
                    dim = 3
                elif node.dim == 4:
                    dim = 4

    node.type = (dim, mem)

    return out



def Exp(node):
    out = str(node[0])
    for child in node[1:]:
        out = "pow(" + str(out) + "," + str(child) + ")"
    return out

def Elexp(node):
    out = str(node[0])
    for child in node[1:]:
        out = "pow(" + str(out) + "," + str(child) + ")"
    return out


def All(node):
    arg = node.parent.name

    if len(node.parent) > 0 and node.parent[0] is node:
        arg += ".n_rows"
    elif len(node.parent) > 1 and node.parent[1] is node:
        arg += ".n_cols"
    elif len(node.parent) > 2 and node.parent[2] is node:
        arg += ".n_slices"
    else:
        return "span::all"

    return "m2cpp::uspan(0, " + arg + "-1)"

Neg = "-(", "", ")"
Not = "not ", "", ""

def Transpose(node):
    if not node.num:
        return "arma::trans(%(0)s)"
    if node[0].dim == 1:
        node.dim = 2
    elif node[0].dim == 2:
        node.dim = 1
    return "arma::trans(", "", ")"

def Ctranspose(node):
    if not node.num:
        return "arma::strans(", "", ")"
    if node.dim == 2:
        node.dim = 3
    elif node.dim == 3:
        node.dim = 2
    return "arma::strans(", "", ")"

def Colon(node):

    if node.parent.cls in ("Get", "Cget", "Nget", "Fget", "Sget",
                "Set", "Cset", "Nset", "Fset", "Sset") and node.parent.num:
        node.type = "uvec"

        if len(node) == 2:
            return "span(%(0)s-1, %(1)s-1)"

        elif len(node) == 3:
            node.include("uspan")
            return "m2cpp::uspan(%(0)s-1, %(1)s, %(2)s-1)"

        else:
            return "", ":", ""

    else:

        node.include("span")

        if node.group.cls in ("Matrix",) and node.group.num:
            node.type = "urowvec"
            node.mem = node.group.mem

        elif node.parent.cls in ("Get", "Cget", "Nget", "Fget", "Sget",
                "Set", "Cset", "Nset", "Fset", "Sset"):
            if node.parent.cls == "Get" and\
                    node.parent.backend == node.parent.type:
                node.type = "irowvec"

            else:
                node.type = "uvec"

        elif node.group.cls in ("Assign",) and node.group[0].num:
            if node.group[0].dim == 1:
                node.type = "uvec"
            else:
                node.type = "urowvec"
            node.mem = node.group[0].mem

        else:
            node.type = "irowvec"

        if len(node) == 2:
            args = "(%(0)s, 1, %(1)s)"
        elif len(node) == 3:
            args = "(%(0)s, %(1)s, %(2)s)"
        else:
            return "", ":", ""


        return "m2cpp::span<%(type)s>"+args
