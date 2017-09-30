import matlab2cpp as mc
from .assign import Assign

def Paren(node):
    """Parenthesis surounding expression.

Examples:
    >>> print(mc.qscript("(1+2)*(3-4)"))
    (1+2)*(3-4) ;
    """
    node.type = node[0].type
    return "(%(0)s)"

def End(node):
    """The 'end' statement indicating not end of block, but end-of-range.
    
Examples:
    >>> print(mc.qscript("x = zeros(2,2,2); x(end, end, end)"))
    x = arma::zeros<cube>(2, 2, 2) ;
    x(x.n_rows-1, x.n_cols-1, x.n_slices-1) ;
    """

    # find context for what end refers to
    pnode = node
    while pnode.parent.cls not in \
            ("Get", "Cget", "Nget", "Fget", "Sget",
            "Set", "Cset", "Nset", "Fset", "Sset", "Block"):
        pnode = pnode.parent

    # end statement only makes sense in certain contexts
    if pnode.cls == "Block":
        node.error("Superfluous end-statement")
        return "end"

    index = pnode.parent.children.index(pnode)
    name = pnode = pnode.parent.name

    if len(node.group) == 1:
        if node.group.dim == 1:
            return name + ".n_rows"
        if node.group.dim == 2:
            return name + ".n_cols"
    
    # what end is referring to
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
    """Return statement

Examples:
    >>> print(mc.qscript("function f(); return"))
    void f()
    {
      return ;
    }
    >>> print(mc.qscript("function y=f(); return; y=1"))
    int f()
    {
      int y ;
      return y ;
      y = 1 ;
      return y ;
    }
    >>> print(mc.qscript("function [y,z]=f(); return; y=1; z=2"))
    void f(int& y, int& z)
    {
      return ;
      y = 1 ;
      z = 2 ;
    }

    """
    func = node.func
    if func.backend == "func_returns":
        return "return"

    if func.backend == "func_lambda":
        return "return _retval"

    return_value = func[1][0].name
    return "return " + return_value


# simple operators
def Mul(node):
    """(Matrix-)multiplication

Examples:
    >>> print(mc.qscript("a = [1,2,3]; b = [4;5;6]; c = a*b"))
    sword _a [] = {1, 2, 3} ;
    a = irowvec(_a, 3, false) ;
    sword _b [] = {4, 5, 6} ;
    b = ivec(_b, 3, false) ;
    c = arma::as_scalar(a*b) ;
    """

    c_flag = False

    if not node[0].num:
        return "", "*", ""

    if len(node) == 2 and node.dim == 0:
        if node[0].backend == "reserved" and node[0].name == "i" and node[1].mem < 4:
            node.value = node[1].value
            return "cx_double(0, %(1)s)"
        elif node[1].backend == "reserved" and node[1].name == "i" and node[0].mem < 4:
            node.value = node[0].value
            return "cx_double(0, %(0)s)"

    dim = node[0].dim
    #mem = max(node[0].mem, 2)
    mem = 0
    for n in node:
        mem = max(mem, n.mem)

    if node.mem == 4 and node[0].dim == 0 and node[0].mem != 4:
        out = "cx_double(%(0)s)"
    else:
        out = "%(0)s"
    index = 1
    for child in node[1:]:
        sVal = str(index)
        index += 1

        # not numerical
        if not child.num:
            return "", "*", ""

        if dim == 0:
            dim = child.dim
            if node.mem == 4 and child.dim == 0 and child.mem != 4:
                c_flag = True

        if dim == 1:
            if child.dim == 0:
                #pass
                dim = 1
            elif child.dim == 1:
                child.error("multiplication shape mismatch, colvec*colvec")
            elif child.dim == 2:
                #pass
                dim = 3
            elif child.dim == 3:
                child.error("multiplication shape mismatch, colvec*matrix")
            elif child.dim == 4:
                child.error("multiplication shape mismatch, colvec*cube")

        elif dim == 2:
            if child.dim == 0:
                #pass
                dim = 2
            elif child.dim == 1:

                out =  "arma::as_scalar(" + out + "*" + "%(" + sVal + ")s" + ")"
                #pass
                dim = 0
                continue
            elif child.dim == 2:
                child.error("multiplication shape mismatch, rowvec*rowvec")
            elif child.dim == 3:
                #pass
                dim = 3

        elif dim == 3:
            if child.dim == 0:
                #pass
                dim = 3
            elif child.dim == 1:
                #pass
                dim = 1
            elif child.dim == 2:
                child.error("multiplication shape mismatch, matrix*rowvec")
            elif child.dim == 3:
                #pass
                dim = 3

        if c_flag:
            out = out + "*" + "(cx_double) %(" + sVal + ")s"
        else:
            out = out + "*" + "%(" + sVal + ")s"
        #mem = max(mem, child.mem)

    node.type = (dim, mem)

    #return "", "*", ""
    return out

def Elmul(node):
    """Element multiplication

Examples:
    >>> print(mc.qscript("a = [1,2,3]; b = [4,5,6]; c = a.*b"))
    sword _a [] = {1, 2, 3} ;
    a = irowvec(_a, 3, false) ;
    sword _b [] = {4, 5, 6} ;
    b = irowvec(_b, 3, false) ;
    c = a%b ;
    """

    # unknown input
    if node.type == "TYPE":
        return "", "__percent__", ""

    # not numerical
    if not node.num:
        node.error("non-numerical multiplication %s" % str([n.type for n in node]))
        return "", "*", ""

    # scalar multiplication, lhs or rhs of elmul is scalar
    if node.dim == 0 or node[0].dim == 0 or node[1].dim == 0:
        return "", "*", ""

    # Sclar's multiplication in Armadillo '%' needs special handle because of
    # interpolation in python
    return "", "__percent__", ""

def Plus(node):
    """Addition

Examples:
    >>> print(mc.qscript("a = [1,2,3]; b = [4,5,6]; c = a+b"))
    sword _a [] = {1, 2, 3} ;
    a = irowvec(_a, 3, false) ;
    sword _b [] = {4, 5, 6} ;
    b = irowvec(_b, 3, false) ;
    c = a+b ;
    """

    # non-numerical addition
    if not node.num:
        node.error("non-numerical addition %s" % str([n.type for n in node]))

    if node.mem == 4 and node.dim == 0:
        out = []
        for child in node:
            if child.mem < 4:
                out.append("cx_double(" + str(child) + ", 0)")
            else:
                out.append(str(child))
        return "+".join(out)

    return "", "+", ""

def Minus(node):
    """Subtraction

Examples:
    >>> print(mc.qscript("a = [1,2,3]; b = [4,5,6]; c = a-b"))
    sword _a [] = {1, 2, 3} ;
    a = irowvec(_a, 3, false) ;
    sword _b [] = {4, 5, 6} ;
    b = irowvec(_b, 3, false) ;
    c = a-b ;
    """
    return "", "-", ""

Gt      = "", ">", ""
Ge      = "", ">=", ""
Lt      = "", "<", ""
Le      = "", "<=", ""
Ne      = "", "!=", ""
Eq      = "", "==", ""
Band    = "", " && ", ""
Land    = "", " && ", ""
Bor     = "", " || ", ""
Lor     = "", " || ", ""

def Elementdivision(node):
    """Element wise division
    """

    # unknown input
    if node.type == "TYPE":

        # default to assume everything scalar
        out = str(node[0])
        for child in node[1:]:

            # force to be float if int in divisor
            if child.cls == "Int":
                out = out + "/" + str(child) + ".0"
            else:
                out = out + "/" + str(child)
        return out

    out = str(node[0])

    
    # I commented out the the code below
    # force float output
    mem = node[0].mem
    if mem<2:
        mem = 2
    mem = max(node[0].mem, node[1].mem)
    
    # I think node will always have length 2,
    # thus for child in node[1:] should be same as child = node[1:]
    # but why fix whats not broken? commented out mem = max(...) and node.mem = mem
    for child in node[1:]:

        # convert ints to floats
        if child.cls == "Int":
            out = out + "/" + str(child) + ".0"

        # avoid int/uword division, or int/int division
        elif mem < 2:
            out = out + "*1.0/" + str(child)

        else:
            out = out + "/" + str(child)

        #mem = max(mem, child.mem)

    #node.mem = mem

    return out


def Leftelementdivision(node):
    """Left element wise division
    """

    # unknown input
    if node.type == "TYPE":
        return "", "\\", ""

    # iterate backwards
    out = str(node[-1])

    # force float output
    mem = node[-1].mem
    if mem<2:
        mem = 2

    for child in node[-2::-1]:

        # avoid explicit integer division
        if child.cls == "Int":
            out = str(child) + ".0/" + out

        # avoid implicit integer division
        if child.mem < 2 and mem < 2:
            out = str(child) + "*1.0/" + out

        else:
            out = str(child) + "/" + out

        #mem = max(mem, child.mem)

    #node.mem = mem
    
    return out


def Matrixdivision(node):

    # start with first element ...
    out = str(node[0])

    mem = node[0].mem or 2
    dim = node[0].dim or 0

    # everything scalar -> use element division
    if {n.dim for n in node} == {0}:

        return Elementdivision(node)

    else:

        # ... iterate over the others
        for child in node[1:]:

            # matrix handle
            if child.dim == 3:
                out = "arma::solve(" + str(child) + ".t(), " + out + ".t(), solve_opts::fast).t()"

            # integer handle
            elif child.cls == "Int":
                out = out + "/" + str(child) + ".0"

            # avoid integer division
            elif child.mem < 2 and mem < 2:
                out = out + "*1.0/" + str(child)

            elif child.type == "int" and mem == 4:
                out = out + "/" + "double(" + str(child) + ")"

            else:
                out = out + "/" + str(child)

            # track memory output
            #mem = max(mem, child.mem)

            # assert if division legal in matlab
            if dim == 0:
                pass
                #dim = child.dim

            elif dim == 1:
                if child.dim == 0:
                    pass
                    #dim = 1
                elif child.dim == 1:
                    node.error("Matrix division error 'colvec\\colvec'")
                elif child.dim == 2:
                    pass
                    #dim = 3
                elif child.dim == 3:
                    node.error("Matrix division error 'colvec\\matrix'")
                elif child.dim == 3:
                    node.error("Matrix division error 'colvec\\cube'")

            elif dim == 2:
                if child.dim == 0:
                    pass
                    #dim = 2
                elif child.dim == 1:
                    pass
                    #dim = 0
                elif child.dim == 2:
                    node.error("Matrix division error 'rowvec\\rowvec'")
                elif child.dim == 3:
                    pass
                    #dim = 2
                elif child.dim == 4:
                    pass
                    #dim = 3

            elif dim == 3:
                if child.dim == 0:
                    pass
                    #dim = 3
                elif child.dim == 1:
                    pass
                    #dim = 1
                elif child.dim == 2:
                    node.error("Matrix division error 'matrix\\rowvec'")
                elif child.dim == 3:
                    pass
                    #dim = 3
                elif child.dim == 4:
                    pass
                    #dim = 4

    #if not (dim is None) and not (mem is None):
    #    node.type = (dim, mem)

    return out


def Leftmatrixdivision(node):
    """Left operator matrix devision
    """

    # unknown input
    if node.type == "TYPE":
        return "", "\\", ""

    # start with first node ...
    out = str(node[0])

    mem = node[0].mem
    dim = node[0].dim

    # everything scalar -> use left element division
    if {n.dim for n in node} == {0}:
        return Leftelementdivision(node)

    else:

        # ... iterate forwards
        for child in node[1:]:

            # classical array inversion
            if child.dim > 0:
                out = "arma::solve(" + out + ", " + str(child) + ", solve_opts::fast)"

            # avoid integer division
            # backwords since left division is reverse
            elif child.mem < 2 and mem < 2:
                out = "(" + out + ")*1.0/" + str(child)
                #mem = 2

            # backwords since left division is reverse
            else:
                out = "(" + out + ")/" + str(child)
                # out = str(child) + "/" + out

            #mem = max(mem, child.mem)

            # assert division as legal
            if dim == 0:
                dim = node.dim

            elif dim == 1:
                if node.dim == 0:
                    pass
                    #dim = 1
                elif node.dim == 1:
                    node.error("Matrix division error 'colvec\\colvec'")
                elif node.dim == 2:
                    pass
                    #dim = 3
                elif node.dim == 3:
                    node.error("Matrix division error 'colvec\\matrix'")
                elif node.dim == 3:
                    node.error("Matrix division error 'colvec\\cube'")

            elif dim == 2:
                if node.dim == 0:
                    pass
                    #dim = 2
                elif node.dim == 1:
                    pass
                    #dim = 0
                elif node.dim == 2:
                    node.error("Matrix division error 'rowvec\\rowvec'")
                elif node.dim == 3:
                    pass
                    #dim = 2
                elif node.dim == 4:
                    pass
                    #dim = 3

            elif dim == 3:
                if node.dim == 0:
                    pass
                    #dim = 3
                elif node.dim == 1:
                    pass
                    #dim = 1
                elif node.dim == 2:
                    node.error("Matrix division error 'matrix\\rowvec'")
                elif node.dim == 3:
                    pass
                    #dim = 3
                elif node.dim == 4:
                    pass
                    #dim = 4

    #node.type = (dim, mem)

    return out



def Exp(node):
    """Exponent
    """

    out = str(node[0])
    for child in node[1:]:
        out = "pow(" + str(out) + ", " + str(child) + ")"

    return out

def Elexp(node):
    """Elementwise exponent
    """

    node.type = node[0].type
    out = str(node[0])

    if len(node) == 2:
        exponent = str(node[1])
        if exponent == "2":
            if(node[0].dim == 0):
                return "m2cpp::square(" + out + ")"
            else:
                return "arma::square(" + out + ")"

    for child in node[1:]:
        out = "arma::pow(" + str(out) + ", " + str(child) + ")"
    return out


def All(node):
    """All ':' element
    """
    arg = node.parent.name

    # is first arg
    if len(node.parent) > 0 and node.parent[0] is node:
        arg += ".n_rows"

    # is second arg
    elif len(node.parent) > 1 and node.parent[1] is node:
        arg += ".n_cols"

    # is third arg
    elif len(node.parent) > 2 and node.parent[2] is node:
        arg += ".n_slices"

    else:
        return "span::all"

    return "m2cpp::span<uvec>(0, " + arg + "-1)"

Neg = "-", "", ""
#Not = "not ", "", ""
Not = "!", "", ""

def Transpose(node):
    """(Simple) transpose

    >>> print(mc.qscript("a = [1,2,3]; b = a.'"))
    sword _a [] = {1, 2, 3} ;
    a = irowvec(_a, 3, false) ;
    b = arma::strans(a) ;
    """

    # unknown datatype
    if not node.num:
        return "arma::strans(%(0)s)"

    """
    # colvec -> rowvec
    if node[0].dim == 1:
        node.dim = 2

    # rowvec -> colvec
    elif node[0].dim == 2:
        node.dim = 1
    """

    # not complex type
    #if node.mem < 4:
    #    return "arma::strans(", "", ")"

    return "arma::strans(", "", ")"

def Ctranspose(node):
    """Complex transpose
    >>> print(mc.qscript("a = [1,2,3]; b = a'"))
    sword _a [] = {1, 2, 3} ;
    a = irowvec(_a, 3, false) ;
    b = arma::trans(a) ;
    """

    # unknown input
    if not node.num:
        return "arma::trans(", "", ")"

    """
    # colvec -> rowvec
    if node[0].dim == 1:
        node.dim = 2

    # rowvec -> colvec
    elif node[0].dim == 2:
        node.dim = 1
    """

    return "arma::trans(", "", ")"

def Colon(node):
    """Colon (as operator)

Examples:
    >>> print(mc.qscript("a = 1:10; b = 1:10:2"))
    a = m2cpp::fspan(1, 1, 10) ;
    b = m2cpp::fspan(1, 10, 2) ;
    >>> print(mc.qscript("a = [1,2,3]; a(1:2:2)"))
    sword _a [] = {1, 2, 3} ;
    a = irowvec(_a, 3, false) ;
    arma::strans(a(m2cpp::span<uvec>(0, 2, 1))) ;
    """

    # context: array argument (must always be uvec)
    if node.group.cls in ("Get", "Cget", "Nget", "Fget", "Sget",
                "Set", "Cset", "Nset", "Fset", "Sset") and node.parent.num:
        #node.type = "uvec"

        node.include("m2cpp")
        # two arguments, use Armadillo span from:to
        if len(node) == 2:

            if node.parent.cls in ("Get", "Cget", "Nget", "Fget", "Sget",
                "Set", "Cset", "Nset", "Fset", "Sset") and node.parent.num and node.parent.backend != "reserved":
                if node.dim in (1, 2):
                    return "arma::span(%(0)s-1, %(1)s-1)"

            if node.group.backend == "reserved":
                node.type = 'rowvec'
                return "m2cpp::fspan(%(0)s, 1, %(1)s)"
            return "m2cpp::span<%(type)s>(%(0)s-1, %(1)s-1)"

        # three arguments, not supported in Armadillo
        elif len(node) == 3:
            if node.group.backend == "reserved":
                node.type = 'rowvec'
                return "m2cpp::fspan(%(0)s, %(1)s, %(2)s)"
            return "m2cpp::span<%(type)s>(%(0)s-1, %(1)s, %(2)s-1)"

        else:
            return "m2cpp::span<%(type)s>(", ", ", ")"

    else:

        # context: matrix concatination
        #if node.group.cls in ("Matrix",) and node.group.num:
        #    node.type = "rowvec"

        # context: pass to function
        #elif node.parent.cls in ("Get", "Cget", "Nget", "Fget", "Sget",
        #        "Set", "Cset", "Nset", "Fset", "Sset"):
        #    node.type = "rowvec"

        # context: assignment
        #elif node.group.cls in ("Assign",) and node.group[0].num:
            #Below the span is set to have the same type as LHS
            #Had to change here ass well or there will be an strans,
            #LHS have  rowvec, while node.type (RHS) have vec dim
            #node.type = node.group[0].type
        #    node.type = "rowvec"
            #print(node.group[0].mem)
            #node.mem = node.group[0].mem

        #else:
        #    node.type = "rowvec"

        #include mconvert.h, which contain namespace m2cpp
        node.include("m2cpp")
        
        # <start>:<stop>
        if len(node) == 2:
            if node.group.cls == "Assign":
                node.type = 'rowvec'
                return "m2cpp::fspan" + "(%(0)s, 1, %(1)s)"
            return "m2cpp::fspan" + "(%(0)s, 1, %(1)s)"

        # <start>:<step>:<stop>
        elif len(node) == 3:
            node.type = 'rowvec'
            args = "(%(0)s, %(1)s, %(2)s)"
            #return "m2cpp::span<" + node.type + ">" + args
            #return "arma::strans(arma::linspace(%(0)s, %(2)s, (%(2)s%(1)s))"
            return "m2cpp::fspan" + args

        #Sets template type to LHS:
        # ex, ti is type vec: ti = (m2cpp::span<vec>(0, 1, nt-1))*dt ;
        #should probably change the if statement above, context: assignment
        #if node.group.cls == "Assign":
            #print(node.group)
            #print(node.group.cls)
            #print(node.group[0].type)
            #print("\n\n\n")
        #    return "m2cpp::span<" + node.group[0].type + ">" +args
        return "m2cpp::span<" + node.type + ">(", ", ", ")"


if __name__ == "__main__":
    import doctest
    doctest.testmod()
