#!/usr/bin/env python
# encoding: utf-8

"""
Translate Matlab to C++ has a few challenges.
One of those challenges is how variable types are handled:
In C++ all variables have to be explicitly declared, while in Matlab they are
declared implicitly at creation.
When translating between, there are many variables where the data types are
unknown and impossible for the Matlab2cpp software to translate.
How to translate the behavior of an integer is vastly different from an float
matrix.

In practice, the program will not automatically assign datatype.
The result is an fairly incomplete program and datatypes get a default
dummy datatype `TYPE`.
For example:

    >>> print mc.qtranslate(
    ...     "function c=f(); a = 4; b = 4.; c = a+b", suggest=False)
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

To aid in the process of translation, `mconvert` automatically creates a
supplement file.
The name of the name of the file is the same as the source file, but with a
`.py` extension.
This file will also be imported (as a python script) each time `mconvert` is
executed.
For example:

    >>> print mc.qsupplement(
    ...     "function c=f(); a = 4; b = 4.; c = a+b", suggest=False)
    scope = {}
    <BLANKLINE>
    f = scope["f"] = {}
    f["a"] = "" # int
    f["c"] = ""
    f["b"] = "" # double

To the right of the type assignment, the program will add a suggestion to aid
the user.

The user can automatically populate it to some degree by using the `-s` or
`--suggestions` flag (or using the `suggest=True` flat).
For example:

    >>> print mc.qsupplement(
    ...     "function c=f(); a = 4; b = 4.; c = a+b", suggest=True)
    scope = {}
    <BLANKLINE>
    f = scope["f"] = {}
    f["a"] = "int"
    f["c"] = "double"
    f["b"] = "double"

The suggestions are created through an iterative process.
The variable `a` and `b` get assigned the datatypes `int` and `double` because
of the direct assignment of variable.
After this, the process starts over and tries to find other variables that
suggestion could fill out for.
In the case of the `c` variable, the assignment on the right were and addition
between `int` and `double`.
To not loose precision, it then chooses to keep `double`, which is passed on to
the `c` variable.
In practice the suggestions can potentially fill in all datatypes automatically
in large programs, and often quite intelligently.

The resulting program will have the following complete form:

    >>> print mc.qtranslate(
    ...     "function c=f(); a = 4; b = 4.; c = a+b", suggest=True)
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    double f()
    {
      int a ;
      double b, c ;
      a = 4 ;
      b = 4. ;
      c = a+b ;
      return c ;
    }

Variable types
--------------

The supplement file consists in practice of only variable `scope` which is a
nested dictionary.
The outer shell of scope has string keys that reference the name of each
function, and declared struct and cells.
The values are dictionaries that represents the inner shell.
The inner shell has string keys that refer to the local variable names string
values that represents the variable type.

The options for valid variable types are listed in the supplement file.
They can be roughly split into two groups: **numerical** and **non-numerical**
types.
The numerical types are as follows:

+--------------+--------------+---------+---------+----------+------------+
|              |*unsigned int*| *int*   | *float* | *double* | *complex*  |
+--------------+--------------+---------+---------+----------+------------+
| *scalar*     | uword        | int     | float   | double   | cx_complex |
+--------------+--------------+---------+---------+----------+------------+
| *vector*     | uvec         | ivec    | fvec    | vec      | cx_vec     |
+--------------+--------------+---------+---------+----------+------------+
| *row\-vector*| urowvec      | irowvec | frowvec | rowvec   | cx_rowvec  |
+--------------+--------------+---------+---------+----------+------------+
| *matrix*     | umat         | imat    | fmat    | mat      | cx_mat     |
+--------------+--------------+---------+---------+----------+------------+
| *cube*       | ucube        | icube   | fcube   | cube     | cx_cube    |
+--------------+--------------+---------+---------+----------+------------+

Values along the horizontal axis represents the amount of memory reserved per
element, and the along the vertical axis represents the various number of
dimensions.
The names are equivalent to the ones in the Armadillo package.

The non-numerical types are as follows:

===========  =====================
char         Single text character
string       Text string
struct       Struct container
func_lambda  Anonymous function
===========  =====================


Anonymous/Lambda functions
--------------------------

In addition to normal function, Matlab have support for anonymous function
through the name prefix `@`.
For example:

    >>> print mc.qtranslate("function f(); g = @(x) x^2; g(4)", suggest=True)
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    void f()
    {
      std::function<int(int)> g ;
      g = [] (int x) {pow(x,2) ; } ;
      g(4) ;
    }

The translator creates an C++11 lambda function equivalently functionality.
To achieve this, the translator creates an extra function in the node-tree.
The name of the function is the same as assigned variable with a `_`-prefix (and
a number postfix, if name is taken).
The information about this function dictate the behaviour of the output
The supplement file have the following form:

    >>> print mc.qsupplement("function f(); g = @(x) x^2; g(4)", suggest=True)
    scope = {}
    <BLANKLINE>
    _g = scope["_g"] = {}
    _g["x"] = "int"
    <BLANKLINE>
    f = scope["f"] = {}
    f["g"] = "func_lambda"

The function `g` is a variable inside `f`'s function scope.
It has the datatype `func_lambda` to indicate that it should be handled as a
function.
The associated function scope `_g` contains the variables inside the definition
of the anonymous function.

Data structures and structure arrays
------------------------------------

Data structures in Matlab can be constructed explicitly through the
`struct`-function.
However, they can also be constructed implicitly by direct assignment.
For example will `a.b=4` create a `struct` ẁith name `a` that has one field `b`.
When translating such a snippet, it creates a C++-struct, such that 

    >>> print mc.qtranslate("function f(); a.b = 4")
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    struct A
    {
      int b ;
    } ;
    <BLANKLINE>
    void f()
    {
      A a ;
      a.b = 4 ;
    }

"""

import collection


PREFIX = """# Supplement file
#
# Valid inputs:
#
# uword   int     float   double cx_double
# uvec    ivec    fvec    vec    cx_vec
# urowvec irowvec frowvec rowvec cx_rowvec
# umat    imat    fmat    mat    cx_mat
# ucube   icube   fcube   cube   cx_cube
#
# char    string  struct  func_lambda
"""


def set_variables(program, types):
    """
Insert the scope variable types into the node-tree.

Args:
    program (Program): Node-tree representation of program
    types (dict): Nested dictionary as provided in the supplement `.py` file.

Example:
    >>> prog = mc.build("function f(a,b); c=4; end")
    >>> types = {"f": {"a":"int", "b":"vec", "c":"float"}}
    >>> mc.set_variables(prog, types)
    >>> print mc.translate(prog)
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    void f(int a, vec b)
    {
      float c ;
      c = (float) 4 ;
    }
"""

    structs = program[1]
    for name in types.keys():

        if name in program.names[2:]:

            types_ = types[name]
            func = program[program.names.index(name)]
            declares, returns, params = func[0], func[1], func[2]

            for key in types_.keys():

                if key in declares.names:
                    var = declares[declares.names.index(key)]
                    var.type = types_[key]

                if key in params.names:
                    var = params[params.names.index(key)]
                    var.type = types_[key]

                elif key in returns.names:
                    var = returns[returns.names.index(key)]
                    var.type = types_[key]

        elif name in structs.names:

            types_ = types[name]
            struct = structs[structs.names.index(name)]

            for key in types_.keys():

                if key in struct.names:
                    var = struct[struct.names.index(key)]
                    var.type = types_[key]

                else:
                    var = collection.Declare(struct, key)
                    var.backend = "struct"
                    var.type = types_[key]


def get_variables(program):
    """
Retrieve scope variables from node-tree

Args:
    program (Program): Node-tree representaiton of program

Returns: types (dict), suggestions (dict)
    Nested dictionaries as provided in the supplement `.py` file.
    One for the types set, and one for suggestions.

Example:
    >>> prog = mc.build("function f(); a=1; b='s'; end")
    >>> types, suggestions = mc.get_variables(prog)
    >>> print suggestions
    {'f': {'a': 'int', 'b': 'string'}}
"""
    types = {}
    suggestions = {}
    for func in program[2:]:

        types[func["name"]] = types_ = {}
        suggestions[func["name"]] = suggestions_ = {}

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
                if type:
                    suggestions_[var["name"]] = type

    for struct in program[1]:

        types[struct["name"]] = types_ = {}
        suggestions[struct["name"]] = suggestions_ = {}

        for var in struct:

            type = var.prop["type"]
            if type == "TYPE":
                type = ""
            types_[var["name"]] = type

            if not type:

                type = var.prop["suggest"]
                if type == "TYPE":
                    type = ""
                if type:
                    suggestions_[var["name"]] = type

    return types, suggestions



def str_variables(types, suggestions={}, structs={}, header=True):
    """
Convert a nested dictionary for types, suggestions and structs and use them to
create a suppliment text ready to be saved.

Args:
    types (dict): All variables datatypes

Kwargs:
    suggestions (dict): Suggested datatypes
    structs (dict): Conentent of structs

Returns: str
    String representation of suppliment file

Example:
    >>> types = {"f" : {"a":"int"}, "g" : {"b":""}}
    >>> suggestions = {"g" : {"b":"float"}}
    >>> structs = {"c" : {"d":"vec"}}
    >>> print str_variables(types, suggestions, structs)
    # Supplement file
    #
    # Valid inputs:
    #
    # uword   int     float   double cx_double
    # uvec    ivec    fvec    vec    cx_vec
    # urowvec irowvec frowvec rowvec cx_rowvec
    # umat    imat    fmat    mat    cx_mat
    # ucube   icube   fcube   cube   cx_cube
    #
    # char    string  struct  func_lambda
    <BLANKLINE>
    scope = {}
    <BLANKLINE>
    f = scope["f"] = {}
    f["a"] = "int"
    <BLANKLINE>
    g = scope["g"] = {}
    g["b"] = "" # float
"""

    out = "scope = {}\n\n"

    keys = types.keys()
    keys.sort()

    for name in keys:
        out += '%s = scope["%s"] = {}\n' % (name, name)
        types_ = types[name]

        for key, val in types_.items():

            if key[0] == "_":
                if key[:4] in ("_aux", "_ret"):
                    continue

            if val:
                out += '%s["%s"] = "%s"\n' % (name, key, val)
            else:
                suggest = suggestions.get(name, {}).get(key, "")
                if suggest:
                    out += '%s["%s"] = "" # %s\n' % (name, key, suggest)
                else:
                    out += '%s["%s"] = ""\n' % (name, key)
        out += "\n"
    if header:
        out = PREFIX + "\n" + out

    return out[:-2]

if __name__ == "__main__":
    import matlab2cpp as mc
    import doctest
    doctest.testmod()

