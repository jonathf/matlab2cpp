"""
.. _usr03:

Translation rules
=================

In Matlab2cpp, the simplest form for translation is a simple string saved to
a variable.  For example::

    >>> Int = "6"

The name :py:class:`~matlab2cpp.collection.Int` (with capital letter)
represents the node the rule is applicable for integers. The right hand side
when it is a string, will be used as the translation every time
:py:class:`~matlab2cpp.collection.Int` occurs.  To illustrate this, consider
the following simple example, where we pass a snippet to the
:py:func:`~matlab2cpp.qscript` function::

    >>> print(mc.qscript("5"))
    5 ;

To implement the new rule we (globally) insert the rule for all instances of
:py:class:`~matlab2cpp.collection.Int` as follows::

    >>> print(mc.qscript("5", Int=Int))
    6 ;

Obviously, this type of translation is not very useful except for a very few
exceptions. First of all, each :py:class:`~matlab2cpp.collection.Int` (and
obviously many other nodes) contain a value. To represent this value, the
translation rule uses string interpolation. This can be implemented as
follows::

    >>> Int = "|%(value)s|"
    >>> print(mc.qscript("5", Int=Int))
    |5| ;

There are also other attributes than `value`. For example variables,
represented through the node `Var` have a name, which refer to it's scope
defined name.  For example::

    >>> Var = "__%(name)s__"
    >>> print(mc.qscript("a = 4", Var=Var))
    __a__ = 4 ;

Since all the code is structured as a node tree, many of the nodes have node
children. The translation is performed leaf-to-root, implying that at the time
of translation of any node, all of it's children are already translated and
available in interpolation. The children are indexed by number, counting from
0. Consider the simple example of a simple addition::

    >>> print(mc.qtree("2+3", core=True)) # doctest: +NORMALIZE_WHITESPACE
     1  1Block      code_block   TYPE
     1  1| Statement  code_block   TYPE
     1  1| | Plus       expression   int
     1  1| | | Int        int          int
     1  3| | | Int        int          int
    >>> print(mc.qscript("2+3"))
    2+3 ;

The node tree (at it's core) consists of
a :py:class:`~matlab2cpp.collection.Block`.
That code :py:class:`~matlab2cpp.collection.Block` contains
one :py:class:`~matlab2cpp.collection.Statement`. The
:py:class:`~matlab2cpp.collection.Statement` contains the
:py:class:`~matlab2cpp.collection.Pluss` operator, which contains the two
:py:class:`~matlab2cpp.collection.Int`. Each :py:class:`~matlab2cpp.Node` in
the tree represents one token to be translated.

From the perspective of the addition :py:class:`~matlab2cpp.collection.Plus`,
the two node children of class :py:class:`~matlab2cpp.collection.Int` are
available in translation respectivly as index 0 and 1. In interpolation we can
do as follows::

    >>> Plus = "%(1)s+%(0)s"
    >>> print(mc.qscript("2+3", Plus=Plus))
    3+2 ;

One obvious problem with this approach is that the number of children of a node
might not be fixed. For example the `Plus` in "2+3" has two children while
"1+2+3" has three. To address nodes with variable number of node children,
alternative representation can be used. Instead of defining a string, a tuple
of three string can be used. They represents prefix, infix and postfix between
each node child. For example::

    >>> Plus = "", "+", ""

It implies that there should be a "+" between each children listed, and nothing
at the ends. In practice we get::

    >>> print(mc.qscript("2+3", Plus=Plus))
    2+3 ;
    >>> print(mc.qscript("1+2+3", Plus=Plus))
    1+2+3 ;


And this is the extent of how the system uses string values. However, in
practice, they are not used much. Instead of strings and tuples functions are
used. They are defined with the same name the string/tuple. This function
should always take a single argument of type :py:class:`~matlab2cpp.Node` which
represents the current node in the node tree. The function should return either
a :py:class:`~matlab2cpp.str` or :py:class:`~matlab2cpp.tuple` as described
above. For example, without addressing how one can use `node`, the following is
equivalent::

    >>> Plus = "", "+ ", ""
    >>> print(mc.qscript("2+3", Plus=Plus))
    2+ 3 ;
    >>> def Plus(node):
    ...     return "", " +", ""
    ...
    >>> print(mc.qscript("2+3", Plus=Plus))
    2 +3 ;

One application of the ``node`` argument is to use it to configure datatypes.
As discussed in the previous section :ref:`usr02`, the node attribute
:py:attr:`~matlab2cpp.Node.type` contains information about datatype.
For example::

    >>> def Var(node):
    ...     if node.name == "x": node.type = "vec"
    ...     if node.name == "y": node.type = "rowvec"
    ...     return node.name
    >>> print(mc.qscript("function f(x,y)", Var=Var))
    void f(vec x, rowvec y)
    {
      // Empty block
    }

For more details on the behavior of the :py:mod:`~matlab2cpp.node` argument, 
see section on node :ref:`usr04`. For an extensive list of the various nodes
available, see developer manual :ref:`dev06`.


Rule context
------------

In the basic translation rule described above, each node type have one
universal rule. However, depending on context, various nodes should be
addressed differently. For example the snippet `sum(x)` lend itself naturally
to have a rule that targets the name `sum` which is part of the Matlab standard
library. Its translation should is as follows::

    >>> print(mc.qscript("sum(x)"))
    arma::sum(x) ;
    
However, if there is a line `sum = [1,2,3]` earlier in the code, then the
translation for `sum(x)` become very different. `sum` is now an array, and the
translation adapts::

    >>> print(mc.qscript("sum=[1,2,3]; sum(x)"))
    sword _sum [] = {1, 2, 3} ;
    sum = irowvec(_sum, 3, false) ;
    sum(x-1) ;

To address this in the same node will quickly become very convoluted. So
instead, the rules are split into various backends. This simplifies things for
each rule that have multiple interpretations, but also ensures that code isn't
to bloated.  For an overview of the various backend, see the developer manual
:ref:`dev07`.

Reserved rules
--------------

The example above with `sum(x)` is handled by two rules. In the second
iteration, it is a :py:mod:`~matlab2cpp.datatype` of type `irowvec` and is
therefore processed in the corresponding rule for `irowvec`. However, in the
former case, `sum` is a function from the Matlab standard library. In principle
there is only one rule for all function calls like this. However, since the
standard library is large, the rules are segmented into rules for each name. 

In the rule :py:mod:`rules._reserved <matlab2cpp.rules._reserved>`, each
function in the standard library (which matlab2cpp supports) is listed in the
variable `rules.reserved`. The context for reserved function manifest itself
into the rules for function calls :py:class:`~matlab2cpp.collection.Get`,
variables :py:class:`~matlab2cpp.collection.Var` and in some cases,
multivariate assignment :py:class:`~matlab2cpp.collection.Assigns`. As
described above, the rules should then have these names respectively. However
to indicate the name, the rules also includes node names as suffix. For
example, the function call for `sum` is handled in the rule
:py:func:`~matlab2cpp.rules._reserved.Get_sum`.

In practice this allows us to create specific rules for any node with names,
which includes variables, function calls, functions, to name the obvious.
For example, if we want to change the summation function from armadillo to the
`accumulation` from `numeric` module, it would be implemented as follows::

    >>> Get_sum = "std::accumulate(", ", ", ")"
    >>> print(mc.qscript("sum(x)", Get_sum=Get_sum))
    std::accumulate(x) ;

This rules is specific for all function calls with name `sum` and wount be
applied for other functions::

    >>> Get_sum = "std::accumulate(", ", ", ")"
    >>> print(mc.qscript("min(x)", Get_sum=Get_sum))
    min(x) ;

There are many rules to translation rule backends in matlab2cpp. This is mainly
because each datatype have a corresponding backend.


"""
import matlab2cpp as mc
