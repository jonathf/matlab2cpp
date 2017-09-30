import matlab2cpp as mc
from .funcs import funcs
from . import armadillo

Counter = "structs"

def Var(node):
    """
Example:
    >>> print(mc.qcpp("a.b = 4; c = a"))
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    struct _A
    {
      int b ;
    } ;
    <BLANKLINE>
    int main(int argc, char** argv)
    {
      _A a, c ;
      a.b = 4 ;
      c = a ;
      return 0 ;
    }
    """

    if funcs(node):
        return

    if node.parent.cls == "Assign" and node.parent[0] is node:
        #assign b = [a.val], a is a structs, suggest vec -> dim=1
        if node.parent[1].cls == "Matrix" and \
          node.parent[1].backend == "structs" and len(node.parent[1][0]) == 1:
            node.declare.suggest = (1, node.parent[1].mem)
        #assign b = a, where a is a struct/structs.
        #This code sets b backend and type to a's backend and type
        elif node.parent[1].cls in ("Var",)\
                and node.parent[1].backend in ("struct", "structs"):

            backend = node.parent[1].backend

            node.parent[1].declare
            if hasattr(node.parent[1], "_declare"):

                node.declare.type = backend
                node.declare.backend = backend
                node.declare._declare = node.parent[1]._declare
                node._declare = node.parent[1]._declare
                node.backend = backend

        else:
            node.declare.suggest = node.parent[1].type
    
    if node.declare.type != "TYPE":
        node.type = node.declare.type


def Get(node):

    if funcs(node):
        return

    #in backends.py backend is set to datatype. If a is rowvec,
    #i want a(2) to have backend rowvec and and datatype double
    #This code sets backend to rowvec, and below datatype is set
    #Thus backend is set before datatype is changed to double
    #mc.configure.backends.Get(node)
    
    #vec
    if node.declare.dim == 1:
        mc.configure.backends.Get(node)
        armadillo.vec(node)
        return

    #rowvec
    if node.declare.dim == 2:
        mc.configure.backends.Get(node)
        armadillo.rowvec(node)
        return

    #mat
    if node.declare.dim == 3:
        mc.configure.backends.Get(node)
        armadillo.mat(node)
        return

    #cube
    if node.declare.dim == 4:
        mc.configure.backends.Get(node)
        armadillo.cube(node)
        return
    
    if node.parent.cls == "Assign" and node.parent[0] is node:
        node.declare.suggest = node.parent[1].type

    if node.declare.type != "TYPE":
        node.type = node.declare.type

def Set(node):

    #in backends.py backend is set to datatype. If a is rowvec,
    #i want a(2) to have backend rowvec and and datatype double
    #This code sets backend to rowvec, and below datatype is set
    #Thus backend is set before datatype is changed to double
    #mc.configure.backends.Get(node)
    
    #vec
    if node.declare.dim == 1:
        mc.configure.backends.Get(node)
        armadillo.vec(node)
        return

    #rowvec
    if node.declare.dim == 2:
        mc.configure.backends.Get(node)
        armadillo.rowvec(node)
        return

    #mat
    if node.declare.dim == 3:
        mc.configure.backends.Get(node)
        armadillo.mat(node)
        return

    #cube
    if node.declare.dim == 4:
        mc.configure.backends.Get(node)
        armadillo.cube(node)
        return
    
    if node.parent.cls == "Assign":
        node.declare.suggest = node.parent[1].type

    if node.declare.type != "TYPE":
        node.type = node.declare.type
        
    
def Fvar(node):

    if node.parent.cls == "Assign" and node.parent[0] is node:
        node.declare.suggest = node.parent[1].type

    if node.declare.type != "TYPE":
        node.type = node.declare.type

def Fset(node):

    if node.parent.cls == "Assign":
        node.declare.suggest = node.parent[1].type

    if node.declare.type != "TYPE":
        node.type = node.declare.type

def Sset(node):

    if node.parent.cls == "Assign":
        node.declare.suggest = node.parent[1].type

    if node.declare.type != "TYPE":
        node.type = node.declare.type


def Assign(node):
    if node[1].type == "TYPE":
        return
    node.type = node[1].type
    # node[0].declare.suggest = node[1].type
    

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
    #node[0].suggest = "uword"
    #index = node.parent.children.index(node)
    #tbb = node.parent.children[index - 1].cls

    #if tbb == "Tbb_for":
    #    node[0].type = "uword"

def Neg(node):
    node.type = node[0].type
    if node[0].mem == 0:
        node.mem = 1


def opr(node):
    node.type = [n.type for n in node]

Plus = opr
def Minus(node):
    opr(node)
    if node.mem == 0:
        node.mem = 1

def Mul(node):
    opr(node)
    mem = max([n.mem for n in node])
    if node[0].dim == 2 and node[1].dim == 1:
        node.type = (0, mem)
    elif node.dim == 1 and node[1].dim == 2:
        node.type = (3, mem)

Elmul = opr
Paren = opr
def Exp(node):
    opr(node)

    if node.num and node.mem < 2:
        node.mem = 3

def Elexp(node):
    node.type = [n.type for n in node]

End = "int"
Int = "int"
Float = "double"
String = "string"
Imag = "cx_double"
def division(node):
    opr(node)
    if node.num and node.mem < 2:
        node.mem = 3
Matrixdivision = division
Elementdivision =  division
Leftmatrixdivision = division
Leftelementdivition = division

All = "uvec"

def Colon(node):
    # context: array argument (must always be uvec)
    if node.group.cls in ("Get", "Cget", "Nget", "Fget", "Sget",
                "Set", "Cset", "Nset", "Fset", "Sset") and \
                node.parent.backend not in ("func_return", "func_returns", "reserved", "func_lambda"):
        node.type = "uvec"

    else:

        # context: matrix concatination
        if node.group.cls in ("Matrix",) and node.group.num:
            node.type = "rowvec"

        # context: pass to function
        elif node.parent.cls in ("Get", "Cget", "Nget", "Fget", "Sget",
                "Set", "Cset", "Nset", "Fset", "Sset"):
            node.type = "rowvec"

        # context: assignment
        elif node.group.cls in ("Assign",) and node.group[0].num:
            node.type = "rowvec"

        else:
            node.type = "rowvec"

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
        declares[node.name[1:]].type = "func_lambda"
        node.parent.type = "func_lambda"
        node.parent[0].type = "func_lambda"
    node.type = "func_lambda"

def Assigns(node):
    if node[-1].type != "TYPE":
        node.type = node[-1].type


if __name__ == "__main__":
    import doctest
    doctest.testmod()
