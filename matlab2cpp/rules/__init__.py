"""
Given a fully configured node-tree, the job can start to make a translation.
The translation is the application of a set of translation rules.
The rules are collected in the folder `rules`. All files contained in the folder
tarts with the prefix `_` (to avoid conflicting names with the python
interpreter) and a `.py` extension indicating that the code just a traditional
python script.

Starting with the simplest form of translation is to define a simple string. For
example:

    >>> Int = "6"

The name `Int` (with capital letter) represents the node the rule is applicable
for, the right hand side when it is a string, will be used as the translation
every time `Int` occurs. To illustrate this, consider the following simple
example:

    >>> print mc.qscript("5")
    5 ;

To implement the new rule we (globally) insert the rule for all instances of
`Int` as follows:

    >>> print mc.qscript("5", Int=Int)
    6 ;

Obviously, this type of translation is very useful except for a very few
exceptions. First of all, each `int` (and obviously many other nodes) contain
a value. To represent this value, the translation rule uses string
interpolation. This can be implemented as follows:

    >>> Int = "%(value)s+1"
    >>> print mc.qscript("5", Int=Int)
    5+1 ;

There are also other place holder names. For example, variables `Var` have
a name, which refer to it's scope defined name.  For example:

    >>> Var = "__%(name)s__"
    >>> print mc.qscript("a = 4", Var=Var)
    __a__ = 4 ;

Since all the code is structured as a node tree, many of the node have node
children. The translation is performed leaf-to-root, implying that at the time
of translation of any node, all of it's children are already translated and
available in interpolation. The children are indexed by number, counting from 0.
For example:

    >>> print mc.qscript("2+3")
    2+3 ;

Here we have an addition node `Plus`, with two children, both `Int`. They are
respectively index 0 and 1. We can use this information to manipulate how the
addition works:

    >>> Plus = "%(1)s+%(0)s"
    >>> print mc.qscript("2+3", Plus=Plus)
    3+2 ;

One obvious problem with this approach is that the number of children of node
might be variable. For example the `Plus` in "2+3" has two children while
"1+2+3" has three. To address nodes with variable number of node children,
alternative representation can be used. Instead of defining a string, a tuple of
three string can be used. They represents prefix, infix and postfix between each
node child. For example:

    >>> Plus = "", "+", ""

It implies that there should be noting in front, in between each node child,
a "+" should be used, and nothing at the ends. In practice we get:

    >>> print mc.qscript("2+3", Plus=Plus)
    2+3 ;
    >>> print mc.qscript("1+2+3", Plus=Plus)
    1+2+3 ;

And this is the full extent of how the system uses string values. However, in
practice, they are not used much. Instead functions are used. They are defined
with the same name the class (the software figures the details out what is
what). This function should always take a single `node` argument which
represents the current node in the node tree. The function should return either
a string or tuple in the same way as the directly defined string and tuple are
define so far. For example, without addressing how one can use `node`, the
following is equivalent:

    >>> Plus = "", "+ ", ""
    >>> print mc.qscript("2+3", Plus=Plus)
    2+ 3 ;
    >>> def Plus(node):
    ...     return "", " +", ""
    ...
    >>> print mc.qscript("2+3", Plus=Plus)
    2 +3 ;
"""

import matlab2cpp as mc
import glob
import os
sep = os.path.sep

for name in glob.glob(os.path.dirname(__file__)+sep+"*.py"):

    name = name.split(sep)[-1]
    if name != "__init__":
        exec("import %s" % name[:-3])

if __name__ == "__main__":
    import doctest
    doctest.testmod()
