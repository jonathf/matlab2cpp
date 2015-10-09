==========
Matlab2cpp
==========


Introduction
============


.. include:: ../../README.md


User interaction
================

.. automodule:: matlab2cpp

.. autoprogram:: mconvert:parser
    :prog: mconvert

Quick functions
---------------
.. automodule:: matlab2cpp.qfunctions

.. autofunction:: matlab2cpp.build
.. autofunction:: matlab2cpp.qcpp
.. autofunction:: matlab2cpp.qhpp
.. autofunction:: matlab2cpp.qpy
.. autofunction:: matlab2cpp.qlog
.. autofunction:: matlab2cpp.qtree
.. autofunction:: matlab2cpp.qscript


Creating node tree
===================

.. automodule:: matlab2cpp.tree

Builder class
-------------

.. automodule:: matlab2cpp.tree.builder
.. autoclass:: matlab2cpp.tree.builder.Builder

Functions
---------
.. automodule:: matlab2cpp.tree.functions
.. autofunction:: matlab2cpp.tree.functions.program
.. autofunction:: matlab2cpp.tree.functions.function
.. autofunction:: matlab2cpp.tree.functions.main
.. autofunction:: matlab2cpp.tree.functions.lambda_
.. autofunction:: matlab2cpp.tree.functions.lamba_func

Codeblock
---------
.. automodule:: matlab2cpp.tree.codeblock
.. autofunction:: matlab2cpp.tree.codeblock.codeblock

Branches
--------
.. automodule:: matlab2cpp.tree.branches
.. autofunction:: matlab2cpp.tree.branches.for_
.. autofunction:: matlab2cpp.tree.branches.if_
.. autofunction:: matlab2cpp.tree.branches.while_
.. autofunction:: matlab2cpp.tree.branches.switch_
.. autofunction:: matlab2cpp.tree.branches.try_

Assignments
-----------
.. automodule:: matlab2cpp.tree.assign
.. autofunction:: matlab2cpp.tree.assign.multi
.. autofunction:: matlab2cpp.tree.assign.single

Variables
---------
.. automodule:: matlab2cpp.tree.variable
.. autofunction:: matlab2cpp.tree.variable.assign
.. autofunction:: matlab2cpp.tree.variable.variable
.. autofunction:: matlab2cpp.tree.variable.cell_arg

Miscellaneous
-------------
.. automodule:: matlab2cpp.tree.misc
.. autofunction:: matlab2cpp.tree.misc.number
.. autofunction:: matlab2cpp.tree.misc.string
.. autofunction:: matlab2cpp.tree.misc.list
.. autofunction:: matlab2cpp.tree.misc.comment
.. autofunction:: matlab2cpp.tree.misc.matrix
.. autofunction:: matlab2cpp.tree.misc.cell





Configuring datatypes
---------------------

.. automodule:: matlab2cpp.supplement

Error log
---------

.. automodule:: matlab2cpp.utils

Extending code translations
===========================

.. automodule:: matlab2cpp.tree

Translation rules
-----------------
.. automodule:: matlab2cpp.translations.__init__

The Node node
-------------

.. automodule:: matlab2cpp.node

Reserved translations
---------------------
.. automodule:: matlab2cpp.translations._reserved

Application programming interface
=================================

Quick translations
------------------

.. autofunction:: matlab2cpp.qcpp

.. autofunction:: matlab2cpp.qhpp

.. autofunction:: matlab2cpp.qpy

Building node-tree
------------------

.. automodule:: matlab2cpp.tree

Treebuilder class
~~~~~~~~~~~~~~~~~
.. autoclass:: matlab2cpp.treebuilder.Treebuilder
    :members:


Translation rules
-----------------


Node references
---------------

.. automodule:: matlab2cpp.references
.. autoattribute:: matlab2cpp.node.backend
.. autoattribute:: matlab2cpp.node.cls
.. autoattribute:: matlab2cpp.node.code
.. autoattribute:: matlab2cpp.node.cur
.. autoattribute:: matlab2cpp.node.line
.. autoattribute:: matlab2cpp.node.name
.. autoattribute:: matlab2cpp.node.names
.. autoattribute:: matlab2cpp.node.ret
.. autoattribute:: matlab2cpp.node.str
.. autoattribute:: matlab2cpp.node.value


Other nodes
-----------

.. autoattribute:: matlab2cpp.node.declare
.. autoattribute:: matlab2cpp.node.func
.. autoattribute:: matlab2cpp.node.group
.. autoattribute:: matlab2cpp.node.line
.. autoattribute:: matlab2cpp.node.program


Datatypes
---------

.. automodule:: matlab2cpp.datatype

.. autoattribute:: matlab2cpp.node.dim
.. autoattribute:: matlab2cpp.node.mem
.. autoattribute:: matlab2cpp.node.num
.. autoattribute:: matlab2cpp.node.type
.. autoattribute:: matlab2cpp.node.suggest
.. autoattribute:: matlab2cpp.node.pointer



Translation rules
=================


Function translation
--------------------

.. automodule:: matlab2cpp.translations._func_common

Single return
~~~~~~~~~~~~~
.. automodule:: matlab2cpp.translations._func_return

Multiple (or no) returns
~~~~~~~~~~~~~~~~~~~~~~~~
.. automodule:: matlab2cpp.translations._func_returns

Lambda/Unnamed functions
~~~~~~~~~~~~~~~~~~~~~~~~
.. automodule:: matlab2cpp.translations._func_lambda


Codeblock translation
---------------------

.. automodule:: matlab2cpp.translations._code_block
.. autofunction:: matlab2cpp.translations._code_block.Statement
.. autofunction:: matlab2cpp.translations._code_block.While
.. autofunction:: matlab2cpp.translations._code_block.Branch
.. autofunction:: matlab2cpp.translations._code_block.If
.. autofunction:: matlab2cpp.translations._code_block.Elif
.. autofunction:: matlab2cpp.translations._code_block.Else
.. autofunction:: matlab2cpp.translations._code_block.Switch
.. autofunction:: matlab2cpp.translations._code_block.Case
.. autofunction:: matlab2cpp.translations._code_block.Otherwise
.. autofunction:: matlab2cpp.translations._code_block.Tryblock
.. autofunction:: matlab2cpp.translations._code_block.Try
.. autofunction:: matlab2cpp.translations._code_block.Catch
.. autofunction:: matlab2cpp.translations._code_block.Block
.. autofunction:: matlab2cpp.translations._code_block.Assigns
.. autofunction:: matlab2cpp.translations._code_block.For
.. autofunction:: matlab2cpp.translations._code_block.Bcomment
.. autofunction:: matlab2cpp.translations._code_block.Lcomment
.. autofunction:: matlab2cpp.translations._code_block.Ecomment


Expressions
-----------

.. automodule:: matlab2cpp.translations._expressions


Administrative translation
--------------------------

.. autofunction:: matlab2cpp.target._program.Program


Mathematical variables
----------------------

.. autofunction:: matlab2cpp.translations._arma_common.configure_arg

.. autofunction:: matlab2cpp.translations._assign_common.Assign



Library modules
===============


.. autofunction:: matlab2cpp.supplement.set_variables
.. autofunction:: matlab2cpp.supplement.get_variables
.. autofunction:: matlab2cpp.supplement.str_variables

