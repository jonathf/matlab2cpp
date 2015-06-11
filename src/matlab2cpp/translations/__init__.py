"""
Given a fully configured node-tree, the job can start to make a translation.
The translation is the application of a set of translation rules.

Each node then have their own translation rule witch is collected in the module
`translations`.
Each translation is a dedicated python function, placed in a script.
This function is then synonym with `translation rule` and which file it is
placed in is synonym for `backend`.
The reason for the structuring in this way is that some nodes (Mostly `Get` and
`Var`) have multiple translation depending on context.
If not specified, the translation rule is static and there only exists one.

Simple translations
~~~~~~~~~~~~~~~~~~~

Each function must have the same name as the class, with capitalized first
letter.
All functions takes one argument: the current node in the tree.
Using information about the tree, the function then returns a translation of the
current node.
A basic translation is just a string translation.
For example, a translation of the `:`-element (not to be confused 
with the `:`-operator), can be constructed as follows::

    def All(node):
        return "arma::all"

Basic placeholders and references
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To simplify notation, it is possible to create placeholder for content.
The string `%(name)s` for example, holds the nodes name, if it has one.
For the variable node, this can be used as follows::

    def Var(node):
        return "%(name)s"

Note that alternative to the placeholder, is to get the variable manually from
reference.  The reference `"%(name)s"` will be filled up with the content of
`node.name`.
This allow for the following equivalent translation for `Var`::

    def Var(node):
        return node.name

Reference to node children
~~~~~~~~~~~~~~~~~~~~~~~~~~

Some nodes have children.
Each translation for each child can be inserted by index.
The placeholders `%(0)s`, `%(1)s`, ...
For example, for a multiplication between two children, using placeholder could
have the following form ::

    def Mul(node):
        return "%(0)s * %(1)s"

Alternative to the placeholder, is the direct reference.
Equivalent multiplication translation could be done as follows:

    def Mul(node):
        return str(node[0]) + " * " + str(node[1])

Note that indexing returns the child of index directly.
The `str(node)` is used to get the translation.

Quick tailoring
~~~~~~~~~~~~~~~

Unfortunately, most nodes with children are not fixed, but vary on context.
How many children is given by `len(node)`, and create by context.
This can often add much unnecessary complexity in translation, so a way around
this was devised.
Instead of returning a string, it is possible to return a tuple of strings.
If, for example, three strings are returned, the three strings represents,
prefix, infix and postfix.
For example would a function call could be written as follows ::

    def Get(node):
        return "%(name)s(", ", ", ")"

Given we knew that there where exactly three children, the same code could be
written:

    def Get(node):
        return "%(name)s(%(0)s, %(1)s, %(2)s)"

More generally, how many elements is returned decides behavior.
These behaviors are as follows:

=======  =========================================================
elments  Implication
=======  =========================================================
1        Use the string as translation
2        Prefix and postfix and ignore infix
3        Prefix, infix and postfix respectively
4        Prefix, infix1, infix2, infix2, ..., postfix
N        Prefix, infix1, ..., infix{N-2}, infix{N-2}, ..., postfix
=======  =========================================================
"""
import glob
import os
sep = os.path.sep

for name in glob.glob(os.path.dirname(__file__)+sep+"*.py"):

    name = name.split(sep)[-1]
    if name != "__init__":
        exec("import %s" % name[:-3])
