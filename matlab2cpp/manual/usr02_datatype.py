"""
.. _usr02:

Configuring translation
=======================

One of the translation challenges is how each variable type is determined. In
C++ all variables have to be explicitly declared, while in Matlab they are
declared implicitly at creation.  When translating between the two languages,
there are many variables where the data types are unknown and impossible for
the Matlab2cpp software to translate.  How to translate the behavior of an
integer is vastly different from an float matrix.

To differentiate between types, each node have an attribute
:py:attr:`~matlab2cpp.Node.type` which represents the node datatype.
Datatypes can be roughly split into two groups: **numerical** and
**non-numerical** types.  The numerical types are as follows:

+---------------+--------------+---------+---------+--------+-----------+
|               | unsigned int | integer | float   | double | complex   |
+===============+==============+=========+=========+========+===========+
| `scalar`      | uword        | int     | float   | double | cx_double |
+---------------+--------------+---------+---------+--------+-----------+
| `vector`      | uvec         | ivec    | fvec    | vec    | cx_vec    |
+---------------+--------------+---------+---------+--------+-----------+
| `row\-vector` | urowvec      | irowvec | frowvec | rowvec | cx_rowvec |
+---------------+--------------+---------+---------+--------+-----------+
| `matrix`      | umat         | imat    | fmat    | mat    | cx_mat    |
+---------------+--------------+---------+---------+--------+-----------+
| `cube`        | ucube        | icube   | fcube   | cube   | cx_cube   |
+---------------+--------------+---------+---------+--------+-----------+

Values along the horizontal axis represents the amount of memory reserved per
element, and the along the vertical axis represents the various number of
dimensions.  The names are equivalent to the ones in the Armadillo package.

The non-numerical types are as follows:

+----------------------------------+------------------------+
| Name                             | Description            |
+==================================+========================+
| `char`                           | Single text character  |
+----------------------------------+------------------------+
| `string`                         | Text string            |
+----------------------------------+------------------------+
| :ref:`struct <struct>`           | Struct container       |
+----------------------------------+------------------------+
| :ref:`structs <structs>`         | Struct array container |
+----------------------------------+------------------------+
| :ref:`func_lambda <func_lambda>` | Anonymous function     |
+----------------------------------+------------------------+

Function scope
--------------

If not specified otherwise, the program will not assign datatype types to any
of variables. The user could in theory navigate the node tree and assign the
variables one by one using the node attributes to navigate. (See section
:ref:`usr04` for details.) However that would be very cumbersome. Instead the
datatypes are define collectively inside their scope. In the case of variables
in functions, the scope variables are the variables declaration
:py:class:`~matlab2cpp.Declares` and function parameters
:py:class:`~matlab2cpp.Params`. To reach the variable that serves as
a scope-wide type, the node attribute :py:attr:`~matlab2cpp.Node.declare` can
be used.

Manually interacting with the variable scope is simpler then iterating through
the full tree, but can in many cases still be cumbersome. To simplefy
interaction with datatype scopes, each program has an suppliment attribute
:py:attr:`~matlab2cpp.Node.ftypes`. The attribute is a nested dictionary where
the outer shell represents the function name the variables are defined. The
inner shell is the variables where keys are variable names and values are
types. It can be used to quickly retrievieng and inserting datatypes.
For example::

    >>> tree = mc.build("function f(a)")
    >>> print(tree.ftypes)
    {'f': {'a': ''}}
    >>> tree.ftypes = {"f": {"a": "int"}}
    >>> print(mc.qscript(tree))
    void f(int a)
    {
      // Empty block
    }

.. _func_lambda:

Anonymous functions
-------------------

In addition to normal function, Matlab have support for anonymous function
through the name prefix ``@``.  For example::

    >>> print(mc.qscript("function f(); g = @(x) x^2; g(4)"))
    void f()
    {
      std::function<double(int)> g ;
      g = [] (int x) {pow(x, 2) ; } ;
      g(4) ;
    }

The translator creates an ``C++11`` lambda function with equivalent
functionality.  To achieve this, the translator creates an extra function in
the node-tree.  The name of the function is the same as assigned variable with
a ``_``-prefix (and a number postfix, if name is taken).  The information about
this function dictate the behaviour of the output The supplement file have the
following form::

    >>> print(mc.qpy("function f(); g = @(x) x^2; g(4)"))
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


.. _struct:

Data structure
--------------

Data structures in Matlab can be constructed explicitly through the
``struct``-function.  However, they can also be constructed implicitly by
direct assignment.  For example will ``a.b=4`` create a ``struct`` with name
``a`` that has one field ``b``.  When translating such a snippet, it creates
a C++-struct, such that::

    >>> print(mc.qhpp("function f(); a.b = 4.", suggest=True))
    #ifndef F_M_HPP
    #define F_M_HPP
    <BLANKLINE>
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
    #endif

In the suppliment file, the local variable `a` will be assigned as a `struct`.
In addition, since the struct has content, the suppliment file creates a new
section for structs.  It will have the following form::

    >>> print(mc.qpy("function f(); a.b = 4.", suggest=True))
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

Quick retrieving and inserting struct variables can be done through the
:py:attr:`~matlab2cpp.Node.stypes` attribute::

    >>> tree = mc.build("a.b = 4")
    >>> tree.ftypes = {"f": {"a": "struct"}}
    >>> tree.stypes = {"a": {"b": "double"}}
    >>> print(mc.qcpp(tree))
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    struct _A
    {
      double b ;
    } ;
    <BLANKLINE>
    int main(int argc, char** argv)
    {
      _A a ;
      a.b = 4 ;
      return 0 ;
    }

.. _structs:

Struct tables
-------------

Given that the data structure is indexed, e.g. ``a(1).b``, it forms a struct
table.  Very similar to regular :ref:`structs <struct>`, which only has one
value per element.  There are a couple of differences in the translation.
First, the struct is declared as an array:

    >>> print(mc.qhpp("function f(); a(1).b = 4.", suggest=True))
    #ifndef F_M_HPP
    #define F_M_HPP
    <BLANKLINE>
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
    #endif

The translation assigned reserves 100 pointers for the content of ``a``.
Obviously, there are situations where this isn't enough (or too much), and the
number should be increased. So second, to adjust this number, the suppliment
file specifies the number of elements in the integer ``_size``:

    >>> print(mc.qpy("function f(); a(1).b = 4.", suggest=True))
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

.. _usr02_suggestion_engine:

Suggestion engine
-----------------

The examples so far, when the functions :py:func:`~matlab2cpp.qcpp`,
:py:func:`~matlab2cpp.qhpp` and :py:func:`~matlab2cpp.qpy` are used, the
argument ``suggest=True`` have been used, and all variable types have been
filled in. Consider the following program where this is not the case::

    >>> print(mc.qhpp("function c=f(); a = 4; b = 4.; c = a+b", suggest=False))
    #ifndef F_M_HPP
    #define F_M_HPP
    <BLANKLINE>
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
    #endif

Since all variables are unknown, the program decides to fill in the dummy
variable ``TYPE`` for each unknown variable. Any time variables are unknown,
``TYPE`` is used. The supplement file created by `m2cpp` or
:py:func:`~matlab2cpp.qpy` reflects all these unknown variables as follows::

    >>> print(mc.qpy("function c=f(); a = 4; b = 4.; c = a+b", suggest=False))
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

By flipping the boolean to ``True``, all the variables get assigned datatypes::

    >>> print(mc.qpy("function c=f(); a = 4; b = 4.; c = a+b", suggest=True))
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

The resulting program will have the following complete form:

    >>> print(mc.qhpp()
    ...     "function c=f(); a = 4; b = 4.; c = a+b", suggest=True)
    #ifndef F_M_HPP
    #define F_M_HPP
    <BLANKLINE>
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
    #endif

Note here though that the variable ``c`` didn't have a suggestion. The
suggestion is an interactive process such that ``a`` and ``b`` both must be
known beforehand.  The variable ``a`` and ``b`` get assigned the datatypes
``int`` and ``double`` because of the direct assignment of variable.  After
this, the process starts over and tries to find other variables that suggestion
could fill out for.  In the case of the ``c`` variable, the assignment on the
right were and addition between ``int`` and ``double``.  To not loose
precision, it then chooses to keep `double`, which is passed on to the ``c``
variable.  In practice the suggestions can potentially fill in all datatypes
automatically in large programs, and often quite intelligently. For example,
variables get suggested across function call scope::

    >>> print(mc.qscript('function y=f(x); y=x; function g(); z=f(4)'))
    int f(int x)
    {
      int y ;
      y = x ;
      return y ;
    }
    <BLANKLINE>
    void g()
    {
      int z ;
      z = f(4) ;
    }

And accross multiple files::

    >>> builder = mc.Builder()
    >>> builder.load("f.m", "function y=f(x); y=x")
    >>> builder.load("g.m", "function g(); z=f(4)")
    >>> builder.configure(suggest=True)
    >>> tree_f, tree_g = builder[:]
    >>> print(mc.qscript(tree_f))
    int f(int x)
    {
      int y ;
      y = x ;
      return y ;
    }
    >>> print(mc.qscript(tree_g))
    void g()
    {
      int z ;
      z = f(4) ;
    }

Verbatim translations
---------------------

In some cases, the translation can not be performed. For example, the Matlab
function ``eval`` can not be properly translated. Matlab is interpreted, and
can easily take a string from local name space, and feed it to the interpreter.
In C++ however, the code must be pre-compiled. Not knowing what the string
input is before runtime, makes this difficult. So instead it makes more sense
to make some custom translation by hand.

Since ``matlab2cpp`` produces C++ files, it is possible to edit them after
creation. However, if changes are made to the Matlab-file at a later point, the
custom edits have to be added manually again. To resolve this, ``matlab2cpp``
supports verbatim translations through the suppliment file ``.py`` and through
the node attribute :py:attr:`~matlab2cpp.Node.vtypes`.
:py:attr:`~matlab2cpp.node.vtype` is a dictionary where the keys are string
found in the orginal code, and the values are string of the replacement.

Performing a verbatim replacement has to be done before the node tree is
constructed. Assigning :py:attr:`~matlab2cpp.Node.vtypes` doesn't work very
well. Instead the replacement dictionary can be bassed as argument to
:py:func:`~matlab2cpp.build`::

    >>> tree = mc.build('''a=1
    ... b=2
    ... c=3''', vtypes = {"b": "_replaced_text_"})
    >>> print(mc.qscript(tree))
    a = 1 ;
    // b=2
    _replaced_text_
    c = 3 ;

Note that when a match is found, the whole line is replaced. No also how the
source code is retained a comment above the verbatim translation. The
verbatim key can only match a single line, however the replacement might span
multiple lines. For example::

    >>> replace_code = '''one line
    ... two line
    ... three line'''
    >>> tree = mc.build('''a=1
    ... b=2
    ... c=3''', vtypes={"b": replace_code})
    >>> print(mc.qscript(tree))
    a = 1 ;
    // b=2
    one line
    two line
    three line
    c = 3 ;

Verbatims can also be utilized by modifying the .py file. Consider the Matlab script::

    a = 1 ;
    b = 2 ;
    c = 3 ;

Using the m2cpp script to translate the Matlab script produces a C++ file and a .py file. By adding code to the .py file, verbatim translation can be added. This is done by using the keyword verbatims and setting it to a python dictionary. Similar to vtype, keys are strings found in the original code, and the values are string of the replacement::

    functions = {
    "main" : {
    "a" : "int",
    "b" : "int",
    "c" : "int",
    },
    }
    includes = [
    '#include <armadillo>',
    'using namespace arma ;',
    ]
    verbatims = {"b = 2 ;" : '''one line
    two line
    tree line'''
    }

In the generated C++ file the second assignment is replaced with the verbatim translation::

    int main(int argc, char** argv)
    {
      int a, c ;
      a = 1 ;
      // b = 2 ;
      one line
      two line
      tree line
      c = 3 ;
      return 0 ;
    }

   
"""
import matlab2cpp as mc

if __name__ == "__main__":
    import doctest
    doctest.testmod()
