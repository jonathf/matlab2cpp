
Matlab2cpp
==========

Introduction
============

.. include:: ../../README.md

User interaction
================

The frontend (`mconvert`)
-------------------------

.. automodule:: mconvert

The supplement configuration (`.py`-file)
-----------------------------------------

.. automodule:: matlab2cpp.supplement
.. autoprogram:: mconvert:parser

Translation report (`.log`-file)
--------------------------------

Code translation
================

Translation rules
-----------------
.. automodule:: matlab2cpp.translations.__init__

Node references
===============
.. automodule:: matlab2cpp.references

Node properties
---------------
These nodes refer to a set of properties specific to the node and are usually
strings or simple numerical values.
All of these values are available in translations as placeholders.
In addition they can all be manipulated and given new values, if needed.
For example::
    
    node.name = "new_name"

will give a node a new (permanent) name.
The associated placeholder `%(name)s` is then changed accordingly as well.

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


Overview of Translation rules
=============================

Function translation
--------------------

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


Application programming interface
=================================

Suppliment configuration (`matlabfile.py`)
------------------------------------------

.. autofunction:: matlab2cpp.supplement.set_variables
.. autofunction:: matlab2cpp.supplement.get_variables
.. autofunction:: matlab2cpp.supplement.str_variables

