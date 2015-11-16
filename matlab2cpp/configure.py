"""
Consider the following program where the datatypes are unassigned: ::

    >>> print mc.qhpp("function c=f(); a = 4; b = 4.; c = a+b", suggest=False)
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    TYPE f()
    {
      TYPE a, b, c ;
      a = 4 ;
      b = 4. ;
      c = a+b ;
      return c ;
    }

Since all variables are unknown, the program decides to fill in the dummy
variable `TYPE` for each unknown variable.

The supplement file created by `mconvert` or :py::`~matlab2cpp.qpy` reflects
all these unknown variables as follows::

    >>> print mc.qpy(
    ...     "function c=f(); a = 4; b = 4.; c = a+b", suggest=False)
    functions = {
      "f" : {
        "a" : "", # int
        "b" : "", # double
        "c" : "",
      },
    }
    includes = [
      '#include <armadillo>',
      'using namespace arma ;',
    ]

To the right of the type assignment, the program will add a suggestion to aid
the user.  The next time the `mconvert`-script is run, the inserted values will
be imported and used.

The user can automatically populate the datatypes to some degree by using the
`-s` or `--suggestions` flag (or using the `suggest=True` flag for `mc.qpy`)::

    >>> print mc.qpy("function c=f(); a = 4; b = 4.; c = a+b", suggest=True)
    functions = {
      "f" : {
        "a" : "int",
        "b" : "double",
        "c" : "double",
      },
    }
    includes = [
      '#include <armadillo>',
      'using namespace arma ;',
    ]

The suggestions are created through an iterative process.  The variable `a` and
`b` get assigned the datatypes `int` and `double` because of the direct
assignment of variable.  After this, the process starts over and tries to find
other variables that suggestion could fill out for.  In the case of the `c`
variable, the assignment on the right were and addition between `int` and
`double`.  To not loose precision, it then chooses to keep `double`, which is
passed on to the `c` variable.  In practice the suggestions can potentially fill
in all datatypes automatically in large programs, and often quite intelligently.

The resulting program will have the following complete form:

    >>> print mc.qhpp(
    ...     "function c=f(); a = 4; b = 4.; c = a+b", suggest=True)
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    double f()
    {
      double b, c ;
      int a ;
      a = 4 ;
      b = 4. ;
      c = a+b ;
      return c ;
    }
"""

import os
import matlab2cpp as mc

def configure(self, suggest=True, **kws):
    """
configure backend

See also:
    :py:func:`matlab2cpp.Builder.configure <Builder.configure>`
    """
    nodes = self.project.flatten(False, True, False)

    while True:

        for node in nodes[::-1]:

            if node.cls in ("Get", "Var"):

                if node.type == "func_lambda":
                    node.backend = "func_lambda"

                    if not (node.parent.cls in \
                            ("Declares", "Returns", "Params")) and\
                            hasattr(node.parent[-1].declare, "reference"):

                        if node.parent.cls == "Assign":
                            node.declare.reference = \
                                    node.parent[-1].declare.reference
                        node.reference = node.declare.reference

                # lambda scope
                if node.backend == "func_lambda":
                    if hasattr(node, "reference"):
                        func = node.reference
                    else:
                        func = None

                # local scope
                elif node in node.program[1]:
                    func = node.program[1][node]
                    node.backend = func.backend

                # external file in same folder
                else:

                    for program in self.project:

                        # don't use file your in as external library
                        if program is node.program:
                            continue

                        if os.path.basename(program.name) == node.name+".m":
                            func = program[1][0]
                            node.backend = func.backend
                            break
                    else:
                        func = None
                        node.translate(only=True)

                if not (func is None):

                    if node.backend == "func_return":

                        node.backend = func.backend
                        node.declare.type = func[1][0].type
                        params = func[2]

                        for i in xrange(len(node)):
                            params[i].suggest = node[i].type
                            node[i].suggest = params[i].type

                    elif node.backend == "func_returns":
                        node.backend = func.backend
                        params = func[2]

                        for j in xrange(len(params)):
                            params[j].suggest = node[j].type
                            node[j].suggest = params[j].type

                        if node.parent.cls == "Assigns":
                            node.parent.backend = "func_returns"

                            returns = func[1]
                            for j in xrange(len(returns)):
                                returns[j].suggest = node.parent[j].type
                                node.parent[j].suggest = returns[j].type

                    elif node.backend == "func_lambda":

                        ret = func[1][0]
                        if ret.type != "TYPE" and node.type == "TYPE":
                            node.type = ret.type
                        elif ret.type == "TYPE" and node.type != "TYPE":
                            ret.type = node.type

                        params = func[2]
                        for i in xrange(len(node)):
                            params[i].suggest = node[i].type

            elif node.cls in ("Fvar", "Cget", "Fget", "Nget", "Colon"):
                node.translate(only=True)

            elif node.cls == "Vector":

                if node and node[0].backend == "struct":
                    declare = node.func[0][
                            node.func[0].names.index(node[0].name)]
                    if declare.backend == "structs":
                        node.backend = "structs"

                node.type = [n.type for n in node]
                node.translate(only=True)

            elif node.cls == "Matrix":

                if node[0] and node[0][0].backend == "struct":
                    declare = node.func[0][
                            node.func[0].names.index(node[0][0].name)]
                    if declare.backend == "structs":
                        node.backend = "structs"

                node.type = [n.type for n in node]
                node.translate(only=True)

            elif node.cls == "Assign" and node[0].cls != "Set" and node[0].type == "TYPE":
                node[0].suggest = node[1].type


            if node.type == "TYPE":

                if node.cls == "Mul":
                    node.translate(only=True)

                elif node.cls in ("Transpose", "Ctranspose"):
                    node.type = node[0].type
                    if node[0].num and node[0].dim in (1,2):
                        node.dim = 3-node[0].dim

                elif node.cls not in\
                        ("Set", "Cset", "Fset", "Nset", "Sset",
                        "Get", "Cget", "Fget", "Nget", "Sget",
                        "Assign", "Assigns"):
                    node.type = [n.type for n in node]

                elif node.cls == "Fvar":
                    node.declare.type = node.type

            elif node.backend == "unknown":
                node.backend = node.type

            # Assign suggestion
            if node.cls == "For":
                var, range = node[:2]
                var.suggest = "int"

            elif node.cls == "Neg" and node[0].mem == 0:
                node.mem = 1




        if suggest:

            complete = True

            for program in self.project:
                
                suggests = program.suggest
                program.stypes = suggests
                program.ftypes = suggests
                complete = complete and not any([any(v) for v in suggests.values()])

            if complete:
                break

        else:
            break

    for program in self.project:
        program[-1].children = []

if __name__ == "__main__":
    import doctest
    doctest.testmod()
