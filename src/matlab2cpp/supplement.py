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

To aid in the process of translation, `mconvert` automatically creates a
supplement file.
The name of the name of the file is the same as the source file, but with a
`.py` extension.
This file will also be imported (as a python script) each time `mconvert` is
executed.
The user can automatically populate it to some degree by using the `-s` or
`--suggestions` flag.
In the other end, the `-r` or `--reset` flag deletes the file before process.

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



def str_variables(types, suggestions={}, structs={}):
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
                if key[1:5] in ("aux_", "ret_"):
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

    return PREFIX + "\n" + out[:-2]

if __name__ == "__main__":
    import matlab2cpp as mc
    import doctest
    doctest.testmod()

