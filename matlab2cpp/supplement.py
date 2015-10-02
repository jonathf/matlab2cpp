#!/usr/bin/env python
# encoding: utf-8

"""
Translate Matlab to C++ has a few challenges.  One of those challenges is how
variable types are handled: In C++ all variables have to be explicitly declared,
while in Matlab they are declared implicitly at creation.  When translating
between the two languages, there are many variables where the data types are
unknown and impossible for the Matlab2cpp software to translate.  How to
translate the behavior of an integer is vastly different from an float matrix.

In practice, the program will not automatically assign datatype.  The result is
an fairly incomplete program and datatypes get a default dummy datatype `TYPE`.
For example:

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

To aid in the process of translation, `mconvert` automatically creates
a supplement file.  The name of the name of the file is the same as the source
file, but with a `.py` extension.  This file will also be imported (as a python
script) each time `mconvert` is executed.  For example:

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

The user can automatically populate it to some degree by using the `-s` or
`--suggestions` flag (or using the `suggest=True` flag).  For example:

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
      int a ;
      double b, c ;
      a = 4 ;
      b = 4. ;
      c = a+b ;
      return c ;
    }

Variable types
--------------

The supplement file consists in practice of only variable `scope` which is
a nested dictionary.  The outer shell of scope has string keys that reference
the name of each function, and declared struct and cells.  The values are
dictionaries that represents the inner shell.  The inner shell has string keys
that refer to the local variable names string values that represents the
variable type.

The options for valid variable types are listed in the supplement file.  They
can be roughly split into two groups: **numerical** and **non-numerical** types.
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
dimensions.  The names are equivalent to the ones in the Armadillo package.

The non-numerical types are as follows:

===========  ======================
char         Single text character
string       Text string
struct       Struct container
structs      Struct array container
func_lambda  Anonymous function
===========  ======================


Anonymous/Lambda functions
--------------------------

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

Data structures and structure arrays
------------------------------------

Data structures in Matlab can be constructed explicitly through the
`struct`-function.  However, they can also be constructed implicitly by direct
assignment.  For example will `a.b=4` create a `struct` with name `a` that has
one field `b`.  When translating such a snippet, it creates a C++-struct, such
that 

    >>> print mc.qhpp("function f(); a.b = 4.", suggest=True)
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    struct _A
    {
      double b ;
    } ;
    <BLANKLINE>
    void f()
    {
      _A a ;
      a.b = 4. ;
    }

In the suppliment file, the local variable `a` will be assigned as a `struct`.
In addition, since the struct has content, the suppliment file creates a new
section for structs.  It will have the following form:

    >>> print mc.qpy("function f(); a.b = 4.", suggest=True)
    functions = {
      "f" : {
        "a" : "struct",
      },
    }
    structs = {
      "a" : {
        "b" : "double",
      },
    }
    includes = [
      '#include <armadillo>',
      'using namespace arma ;',
    ]

Given that the data structure is in the form of an array, the process is similar
to a single element.  There is only two differences.  In the translation, the
struct is declared as an array:

    >>> print mc.qhpp("function f(); a(1).b = 4.", suggest=True)
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    struct _A
    {
      double b ;
    } ;
    <BLANKLINE>
    void f()
    {
      _A a[100] ;
      a[0].b = 4. ;
    }

The translation assigned reserves 100 pointers for the content of `a`.
Obviously, there are situations where this isn't enough, and the number should
be increased. To adjust this number, the suppliment file specifies the number of
elements in the integer `_size`:

    >>> print mc.qpy("function f(); a(1).b = 4.", suggest=True)
    functions = {
      "f" : {
        "a" : "structs",
      },
    }
    structs = {
      "a" : {
        "_size" : 100,
            "b" : "double",
      },
    }
    includes = [
      '#include <armadillo>',
      'using namespace arma ;',
    ]
"""

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
# char    string  struct  structs func_lambda
"""

def set_f(node, types):

    funcs = node.program[1]    

    # Functions
    for name in types.keys():

        if name in funcs.names:

            types = types[name]
            func = funcs[funcs.names.index(name)]
            declares, returns, params = func[0], func[1], func[2]

            for key in types.keys():

                if key in declares.names:

                    if key in returns.names:
                        var = returns[returns.names.index(key)]
                        var.type = types[key]

                    var = declares[declares.names.index(key)]
                    var.type = types[key]

                elif key in params.names:
                    var = params[params.names.index(key)]
                    var.type = types[key]

def get_f(node):

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
        return get_f(instance)
    def __set__(self, instance, value):
        set_f(instance, value)


def get_ss(node):

    funcs = node.program[1]
    structs = node.program[3]

    suggest = {}

    for func in funcs:

        suggest[func["name"]] = suggest_ = {}

        declares, params = func[0], func[2]
        for var in declares[:]+params[:]:

            type = var.prop["type"]
            if type == "TYPE":
                type = ""

            if not type:

                type = var.prop["suggest"]
                if type == "TYPE":
                    type = ""
                if type:
                    suggest_[var["name"]] = type

    for struct in structs:

        suggest[struct["name"]] = suggest_ = {}

        for var in struct:

            type = var.prop["type"]
            if type == "TYPE":
                type = ""

            if not type:

                type = var.prop["suggest"]
                if type == "TYPE":
                    type = ""
                if type:
                    suggest_[var["name"]] = type

    return suggest

class Sstypes(object):
    def __get__(self, instance, owner):
        return get_ss(instance)
    def __set__(self, instance, value):
        raise AttributeError("Suggestions not to be set manually")



def set_s(node, types):

    structs = node.program[3]

    # Structs
    for name in types.keys():

        if name in structs.names:

            types = types[name]
            struct = structs[structs.names.index(name)]

            for key in types.keys():

                if key in struct.names:

                    var = struct[struct.names.index(key)]

                    if var.cls == "Counter":
                        var.value = str(types[key])
                    else:
                        var.type = types[key]

                else:
                    var = collection.Declare(struct, key, backend="struct",
                        type=types[key])


def get_s(node):

    structs = node.program[3]
    types_s = {}
    for struct in structs:

        types_s[struct["name"]] = types = {}

        for var in struct:

            type = var.prop["type"]
            if type == "TYPE":
                type = ""

            types[var.name] = type

    return types_s


class Stypes(object):
    def __get__(self, instance, owner):
        return get_s(instance)
    def __set__(self, instance, value):
        set_s(instance, value)


def set_i(node, types):

    includes = node.program[0]

    # Includes
    for key in types:

        if key not in includes.names:
            collection.Include(includes, key)


def get_i(node):

    includes = node.program[0]

    types_i = []
    for include in includes:
        types_i.append(include.name)

    return types_i

class Itypes(object):
    def __get__(self, instance, owner):
        return get_i(instance)
    def __set__(self, instance, value):
        set_i(instance, value)


def set_variables(program, types_f={}, types_s={}, types_i=[]):
    """
Insert the scope variable types into the node-tree.

Args:
    program (Program): Node-tree representation of program
    types_f (dict): Nested dictionary where outer keys are function names, inner
        keys are name of variables and inner values are datatype name.
    types_s (dict): Nested dictionary where outer keys are struct names, inner
        keys are name of variables and inner values are datatype name.
    types_i (list): List of included statements.

Example:
    >>> prog = mc.build("function f(a,b); c=4; end")
    >>> types_f = {"f": {"a":"int", "b":"vec", "c":"float"}}
    >>> mc.set_variables(prog, types_f=types_f)
    >>> print mc.qhpp(prog)
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    void f(int a, vec b)
    {
      float c ;
      c = (float) 4 ;
    }
"""
    set_f(program, types_f)
    set_s(program, types_s)
    set_i(program, types_i)


def get_variables(program):
    """
Retrieve scope variables from node-tree

Args:
    program (Program): Node-tree representaiton of program

Returns: types_f (dict), types_s (dict), types_i (list), suggest (dict)
    Nested dictionaries as provided in the supplement `.py` file.
    Respectively for function types, struct types, include types and suggested
    types.

Example:
    >>> prog = mc.build("function f(); a=1; b='s'; end")
    >>> types_f, types_s, types_i, suggest = mc.get_variables(prog)
    >>> print suggest
    {'f': {'a': 'int', 'b': 'string'}}
"""

    types_f = get_f(program)
    types_s = get_s(program)
    types_i = get_i(program)
    suggest = get_ss(program)
    return types_f, types_s, types_i, suggest

def str_variables(types_f={}, types_s={}, types_i=[], suggest={}, prefix=True):
    """
Convert a nested dictionary for types, suggestions and structs and use them to
create a suppliment text ready to be saved.

Kwargs:
    types_f (dict): Function variables datatypes
    types_s (dict): Struct variables datatypes
    types_i (list): Includes in header
    suggest (dict): Suggested datatypes for types_f and types_s
    prefix (bool): True if the type explaination should be included

Returns: str
    String representation of suppliment file

Example:
    >>> types_f = {"f" : {"a":"int"}, "g" : {"b":""}}
    >>> types_s = {"c" : {"d":""}}
    >>> types_i = ["#include <armadillo>"]
    >>> suggest = {"g" : {"b":"float"}, "c" : {"d":"vec"}}
    >>> print str_variables(types_f, types_s, types_i, suggest, prefix=False)
    functions = {
      "f" : {
        "a" : "int",
      },
      "g" : {
        "b" : "", # float
      },
    }
    structs = {
      "c" : {
        "d" : "", # vec
      },
    }
    includes = [
      '#include <armadillo>',
    ]
    """

    if prefix:
        out = PREFIX
    else:
        out = ""

    if types_f:

        if prefix:
            out += "\n"

        out += "functions = {\n"

        keys = types_f.keys()
        keys.sort()

        for name in keys:


            out += '  "%s" : {\n' % (name)
            types = types_f[name]

            keys2 = types.keys()
            keys2.sort()
            l = max([len(k) for k in keys2]+[0])+4

            for key in keys2:
                val = types[key]
                sug = suggest.get(name, {}).get(key, "")

                if key[:1] == "_":
                    continue

                elif val:
                    out += " "*(l-len(key)) + '"%s" : "%s",\n' % (key, val)

                elif sug:
                    out += " "*(l-len(key)) + '"%s" : "", # %s\n' % (key, sug)

                else:
                    out += " "*(l-len(key)) + '"%s" : "",\n' % (key)

            out += "  },\n"

        out += "}"

    if types_s:

        if types_f or prefix:
            out += "\n"

        out += "structs = {\n"

        keys = types_s.keys()
        keys.sort()

        for name in keys:

            out += '  "%s" : {\n' % (name)
            types = types_s[name]

            keys2 = types.keys()
            keys2.sort()
            l = max([len(k) for k in keys2])+4

            for key in keys2:
                val = types[key]
                sug = suggest.get(name, {}).get(key, "")

                if key[-5:] == "_size":
                    val = val or 100
                    out += " "*(l-len(key)) + '"%s" : %s,\n' % (key, val)

                elif val:
                    out += " "*(l-len(key)) + '"%s" : "%s",\n' % (key, val)

                elif sug:
                    out += " "*(l-len(key)) + '"%s" : "", # %s\n' % (key, sug)

                else:
                    out += " "*(l-len(key)) + '"%s" : "",\n' % (key)

            out += "  },\n"

        out += "}"

    if types_i:

        if prefix or types_f or types_s:
            out += "\n"

        out += "includes = [\n"

        for key in types_i:
            if key:
                out += "  '" + key + "',\n"

        out += "]"

    return out

from node import collection


if __name__ == "__main__":
    import matlab2cpp as mc
    import doctest
    doctest.testmod()

