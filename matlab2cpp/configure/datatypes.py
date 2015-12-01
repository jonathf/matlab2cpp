from funcs import funcs
import matlab2cpp as mc

Counter = "structs"

def Var(node):

    if funcs(node):
        return
    
    if node.declare.type != "TYPE":
        node.type = node.declare.type


def Get(node):

    if funcs(node):
        return

    if node.declare.type != "TYPE":
        node.type = node.declare.type
        return


def Assign(node):
    if node[1].type == "TYPE":
        return

    node.type = node[1].type
    node[0].declare.suggest = node[1].type
    

def Vector(node):

    # default to common denominator
    node.type = [n.type for n in node]

    # dimensionality in vector
    dims = {n.dim for n in node}

    # non-numerical elements in vector isn't addresed
    if None in dims or [n for n in node if not n.num]:

        # keep it simple of single elements
        if len(node) == 1:
            node.type = node[0].type
        return

    # single element in vector
    if len(node) == 1:

        if dims == {0}:
            # holder value to determine if vector is in decomposed state
            node.value = "scalarsonly"
        else:
            node.value = ""

        node.dim = list(dims)[0]
        return

    # only colvecs
    elif dims == {1}:
        node.dim = 1
        nodes = [str(n) for n in node]

    # Decomposed row
    if dims == {0}:
        node.value = "scalarsonly"
        node.dim = 2

    # only rowvecs
    elif dims == {2}:
        node.dim = 2

    # mix of scalars and rowvecs
    elif dims == {0,2}:
        node.dim = 2

    # mix of matrices and colvecs
    elif dims in ({3}, {1,3}):
        node.dim = 3


def Matrix(node):

    # matrix surround struct converts it to array
    if node[0] and node[0][0].backend == "struct":
        declare = node.func[0][
                node.func[0].names.index(node[0][0].name)]
        if declare.backend == "structs":
            node.backend = "structs"
        return

    node.type = [n.type for n in node]

    dims = {n.dim for n in node}

    # single vector with no content
    if len(node) == 1 and len(node[0]) == 0:
        node.num = False
        return

    # everything on scalarsonly form
    elif all([n.value for n in node]):
        node.value = "scalarsonly"

        # set dimensions
        ax0, ax1 = len(node), len(node[0])
        if ax0 > 1:
            if ax1 > 1:
                node.dim = 3#matrix
            else:
                node.dim = 1#rowvec
        else:
            if ax1 > 1:
                node.dim = 2#colvec
            else:
                node.dim = 0#scalar

        if node.parent.cls == "Assign":
            node.parent.backend = "matrix"

    elif dims in ({0,1}, {1}):

        # configure dimensions
        if len(node[0])>1:
            node.dim = 3#matrix
        else:
            node.dim = 1#colvec

    # mix of rowvecs and matrices
    elif dims in ({2}, {3}, {2,3}):

        # configure dimensiosn
        if dims == {2} and len(node)==1:
            node.dim = 2#rowvec
        else:
            node.dim = 3#matrix



def Transpose(node):

    node.type = node[0].type
    if node[0].num:
        if node[0].dim == 1:
            node.dim = 2
            return
        elif node[0].dim == 2:
            node.dim = 1
            return

Ctranspose = Transpose

def For(node):
    node[0].suggest = "int"

def Neg(node):
    node.type = node[0].type
    if node[0].mem == 0:
        node.mem = 1


def opr(node):
    node.type = [n.type for n in node]

Plus = opr
Elmul = opr

Int = "int"
Float = "double"
String = "string"
Imag = "cx_double"

def Lambda(node):

    # lambda function are created as full functions, but referenced to be
    # written inline
    lfunc = node.program[1][node.name]
    ldeclares, lreturns, lparams, lblock = lfunc
    lnames = lparams.names + ldeclares.names
    expr = lblock[0][1]

    # location for where lambda is created
    func = node.func
    declares, returns, params, block = func

    # Lambda creates a local scope
    # e.g. in expressions like '@(x) x*y'
    # 'x' is in one scope and 'y' is in another.
    # This little hack iterates the expression of the function in
    # search for vars/calls etc. like 'y' and declares them with
    # the right types.
    nodes = [expr]
    for node_ in nodes:
        nodes.extend(node_[:])

        # a variable
        if node_.cls in ["Var", "Cvar", "Fvar",
                "Get", "Cget", "Fget", "Nget"]:
            name = node_.name

            # not in lambda scope
            if name not in lnames:

                # defined as a parameter in function
                if name in params.names:
                    type = params[params.names.index(name)].type
                    node_.type = type
                    node_.declare.type = type

                # declared in function
                elif name in declares.names:
                    type = declares[declares.names.index(name)].type
                    node_.type = type
                    node_.declare.type = type

    

    mc.configure.configure(lfunc)
    # declare list in lambda function
    if ldeclares["_retval"].type != "TYPE":
        node.type = "func_lambda"
        declares[node.name[1:]].type = "func_lambda"
        node.parent.type = "func_lambda"
        node.parent[0].type = "func_lambda"
