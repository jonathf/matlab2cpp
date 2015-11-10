"""
In addition to normal function, Matlab have support for anonymous function
through the name prefix `@`.  For example:

    >>> print mc.qhpp("function f(); g = @(x) x^2; g(4)", suggest=True)
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    void f()
    {
      std::function<int(int)> g ;
      g = [] (int x) {pow(x,2) ; } ;
      g(4) ;
    }

The translator creates an C++11 lambda function with equivalent functionality.
To achieve this, the translator creates an extra function in the node-tree.  The
name of the function is the same as assigned variable with a `_`-prefix (and
a number postfix, if name is taken).  The information about this function
dictate the behaviour of the output The supplement file have the following form:

    >>> print mc.qpy("function f(); g = @(x) x^2; g(4)", suggest=True)
    functions = {
      "_g" : {
              "x" : "int",
      },
      "f" : {
        "g" : "func_lambda",
      },
    }
    includes = [
      '#include <armadillo>',
      'using namespace arma ;',
    ]

The function `g` is a variable inside `f`'s function scope.  It has the datatype
`func_lambda` to indicate that it should be handled as a function.  The
associated function scope `_g` contains the variables inside the definition of
the anonymous function.
"""
import matlab2cpp as mc

def set(node, types):

    funcs = node.program[1]    

    # Functions
    for name in types.keys():

        if name in funcs.names:

            types_ = types[name]
            func = funcs[funcs.names.index(name)]
            declares, returns, params = func[:3]

            for key in types_.keys():

                if key in declares.names:

                    if key in returns.names:
                        var = returns[returns.names.index(key)]
                        var.type = types_[key]

                    var = declares[declares.names.index(key)]
                    var.type = types_[key]

                elif key in params.names:
                    var = params[params.names.index(key)]
                    var.type = types_[key]

def get(node):

    funcs = node.program[1]

    types = {}

    for func in funcs:

        types[func["name"]] = types_ = {}

        declares, params = func[0], func[2]
        for var in declares[:]+params[:]:

            type = var.prop["type"]
            if type == "TYPE":
                type = ""
            types_[var["name"]] = type

            if not type:

                type = var.prop["suggest"]
                if type == "TYPE":
                    type = ""

    return types


class Ftypes(object):

    def __get__(self, instance, owner):
        return get(instance)

    def __set__(self, instance, value):
        set(instance, value)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
