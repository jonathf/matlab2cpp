"""
.. _usr03:

Configuring datatypes
=====================

One of the translation challenges is how each variable type determined. In C++
all variables have to be explicitly declared, while in Matlab they are declared
implicitly at creation.  When translating between the two languages, there are
many variables where the data types are unknown and impossible for the
Matlab2cpp software to translate.  How to translate the behavior of an integer
is vastly different from an float matrix.

As noted in the last section :ref:`usr02`, each node can have multiple
backends. At the simplest level, each node have
a :py:mod:`~matlab2cpp.datatype` which represents what backend rule should be
used in translation. 

.. autoattribute:: matlab2cpp.Node.type

Function scope
--------------

If not specified otherwise, the program will not assign datatype types to any
of variables. The user could in theory navigate the node tree and assign the
variables one by one using the node attributes to navigate. (See :ref:`usr04`
for details.) However that would be very cumbersome. Instead the datatypes can
be inserted much simpler into the program using supplement attribute 
:py:attr:`~matlab2cpp.Node.ftypes`. The attribute is a nested dictionary where
the outer shell represents the function name the variables are defined. The
inner shell is the variables where keys are variable names and values are
types. For example::

    >>> tree = mc.build("function f(a)")
    >>> print tree.ftypes
    {'f': {'a': ''}}
    >>> tree.ftypes = {"f": {"a": "int"}}
    >>> print mc.qscript(tree)
    void f(int a)
    {
      // Empty block
    }

Here there is one function scope defined by `f`, with one variable `a`.




Anonymous functions
~~~~~~~~~~~~~~~~~~~
.. automodule:: matlab2cpp.supplement.functions

Data structures
~~~~~~~~~~~~~~~
.. automodule:: matlab2cpp.supplement.structs

Suggestions
~~~~~~~~~~~
.. automodule:: matlab2cpp.supplement.suggests

Includes
~~~~~~~~
.. automodule:: matlab2cpp.supplement.includes

Suggestion engine
-----------------
.. automodule:: matlab2cpp.configure
"""
import matlab2cpp as mc
