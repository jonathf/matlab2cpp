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

Quick translation functions
---------------------------
.. automodule:: matlab2cpp.qfunctions

.. autofunction:: matlab2cpp.build
.. autofunction:: matlab2cpp.qcpp
.. autofunction:: matlab2cpp.qhpp
.. autofunction:: matlab2cpp.qpy
.. autofunction:: matlab2cpp.qlog
.. autofunction:: matlab2cpp.qscript
.. autofunction:: matlab2cpp.qtree


Creating node tree
===================

.. automodule:: matlab2cpp.tree

Builder class
-------------

.. automodule:: matlab2cpp.tree.builder
.. autoclass:: matlab2cpp.Builder
    :members:

.. .. autofunction:: matlab2cpp.tree.assign.multi
.. .. autofunction:: matlab2cpp.tree.assign.single
.. .. autofunction:: matlab2cpp.tree.branches.forloop
.. .. autofunction:: matlab2cpp.tree.branches.ifbranch
.. .. autofunction:: matlab2cpp.tree.branches.switch
.. .. autofunction:: matlab2cpp.tree.branches.trybranch
.. .. autofunction:: matlab2cpp.tree.branches.whileloop
.. .. autofunction:: matlab2cpp.tree.codeblock.codeblock
.. .. autofunction:: matlab2cpp.tree.expression.create
.. .. autofunction:: matlab2cpp.tree.findend.expression
.. .. autofunction:: matlab2cpp.tree.findend.expression_space
.. .. autofunction:: matlab2cpp.tree.findend.matrix
.. .. autofunction:: matlab2cpp.tree.findend.string
.. .. autofunction:: matlab2cpp.tree.findend.comment
.. .. autofunction:: matlab2cpp.tree.findend.dots
.. .. autofunction:: matlab2cpp.tree.findend.paren
.. .. autofunction:: matlab2cpp.tree.findend.cell
.. .. autofunction:: matlab2cpp.tree.functions.program
.. .. autofunction:: matlab2cpp.tree.functions.function
.. .. autofunction:: matlab2cpp.tree.functions.main
.. .. autofunction:: matlab2cpp.tree.functions.lambda_construct
.. .. autofunction:: matlab2cpp.tree.functions.lamba_func
.. .. autofunction:: matlab2cpp.tree.identify.space_delimiter
.. .. autofunction:: matlab2cpp.tree.identify.string
.. .. autofunction:: matlab2cpp.tree.identify.space_delimited
.. .. autofunction:: matlab2cpp.tree.iterate.list
.. .. autofunction:: matlab2cpp.tree.iterate.comma_list
.. .. autofunction:: matlab2cpp.tree.iterate.space_list
.. .. autofunction:: matlab2cpp.tree.misc.number
.. .. autofunction:: matlab2cpp.tree.misc.string
.. .. autofunction:: matlab2cpp.tree.misc.list
.. .. autofunction:: matlab2cpp.tree.misc.comment
.. .. autofunction:: matlab2cpp.tree.misc.matrix
.. .. autofunction:: matlab2cpp.tree.misc.cell
.. .. autofunction:: matlab2cpp.tree.variables.assign
.. .. autofunction:: matlab2cpp.tree.variables.variable
.. .. autofunction:: matlab2cpp.tree.variables.cell_arg

Configuring datatypes
=====================

.. automodule:: matlab2cpp.datatype

Suggestion engine
-----------------
.. automodule:: matlab2cpp.configure
.. autofunction:: matlab2cpp.configure.configure

Manual assignment
-----------------
.. automodule:: matlab2cpp.supplement
.. autofunction:: matlab2cpp.supplement.Ftypes
.. autofunction:: matlab2cpp.supplement.Stypes
.. autofunction:: matlab2cpp.supplement.Itypes


Node behavior
=============
.. automodule:: matlab2cpp.node

References to other nodes
-------------------------
.. automodule:: matlab2cpp.node.references

.. autoclass:: matlab2cpp.Node
    :members:

Node collection
===============
.. automodule:: matlab2cpp.collection

.. autofunction:: matlab2cpp.collection.All
.. autofunction:: matlab2cpp.collection.Assign
.. autofunction:: matlab2cpp.collection.Assigns
.. autofunction:: matlab2cpp.collection.Band
.. autofunction:: matlab2cpp.collection.Bcomment
.. autofunction:: matlab2cpp.collection.Block
.. autofunction:: matlab2cpp.collection.Bor
.. autofunction:: matlab2cpp.collection.Branch
.. autofunction:: matlab2cpp.collection.Break
.. autofunction:: matlab2cpp.collection.Case
.. autofunction:: matlab2cpp.collection.Catch
.. autofunction:: matlab2cpp.collection.Cell
.. autofunction:: matlab2cpp.collection.Cget
.. autofunction:: matlab2cpp.collection.Colon
.. autofunction:: matlab2cpp.collection.Cond
.. autofunction:: matlab2cpp.collection.Condline
.. autofunction:: matlab2cpp.collection.Counter
.. autofunction:: matlab2cpp.collection.Cset
.. autofunction:: matlab2cpp.collection.Ctranspose
.. autofunction:: matlab2cpp.collection.Cvar
.. autofunction:: matlab2cpp.collection.Declare
.. autofunction:: matlab2cpp.collection.Declares
.. autofunction:: matlab2cpp.collection.Ecomment
.. autofunction:: matlab2cpp.collection.Elementdivision
.. autofunction:: matlab2cpp.collection.Elexp
.. autofunction:: matlab2cpp.collection.Elif
.. autofunction:: matlab2cpp.collection.Elmul
.. autofunction:: matlab2cpp.collection.Else
.. autofunction:: matlab2cpp.collection.End
.. autofunction:: matlab2cpp.collection.Eq
.. autofunction:: matlab2cpp.collection.Error
.. autofunction:: matlab2cpp.collection.Exp
.. autofunction:: matlab2cpp.collection.Expr
.. autofunction:: matlab2cpp.collection.Fget
.. autofunction:: matlab2cpp.collection.Float
.. autofunction:: matlab2cpp.collection.For
.. autofunction:: matlab2cpp.collection.Fset
.. autofunction:: matlab2cpp.collection.Func
.. autofunction:: matlab2cpp.collection.Funcs
.. autofunction:: matlab2cpp.collection.Fvar
.. autofunction:: matlab2cpp.collection.Ge
.. autofunction:: matlab2cpp.collection.Get
.. autofunction:: matlab2cpp.collection.Gt
.. autofunction:: matlab2cpp.collection.Header
.. autofunction:: matlab2cpp.collection.Headers
.. autofunction:: matlab2cpp.collection.If
.. autofunction:: matlab2cpp.collection.Imag
.. autofunction:: matlab2cpp.collection.Include
.. autofunction:: matlab2cpp.collection.Includes
.. autofunction:: matlab2cpp.collection.Inline
.. autofunction:: matlab2cpp.collection.Inlines
.. autofunction:: matlab2cpp.collection.Int
.. autofunction:: matlab2cpp.collection.Lambda
.. autofunction:: matlab2cpp.collection.Land
.. autofunction:: matlab2cpp.collection.Lcomment
.. autofunction:: matlab2cpp.collection.Le
.. autofunction:: matlab2cpp.collection.Leftelementdivision
.. autofunction:: matlab2cpp.collection.Leftmatrixdivision
.. autofunction:: matlab2cpp.collection.Log
.. autofunction:: matlab2cpp.collection.Lor
.. autofunction:: matlab2cpp.collection.Lt
.. autofunction:: matlab2cpp.collection.Main
.. autofunction:: matlab2cpp.collection.Matrix
.. autofunction:: matlab2cpp.collection.Matrixdivision
.. autofunction:: matlab2cpp.collection.Minus
.. autofunction:: matlab2cpp.collection.Mul
.. autofunction:: matlab2cpp.collection.Ne
.. autofunction:: matlab2cpp.collection.Neg
.. autofunction:: matlab2cpp.collection.Nget
.. autofunction:: matlab2cpp.collection.Not
.. autofunction:: matlab2cpp.collection.Nset
.. autofunction:: matlab2cpp.collection.Opr
.. autofunction:: matlab2cpp.collection.Otherwise
.. autofunction:: matlab2cpp.collection.Params
.. autofunction:: matlab2cpp.collection.Paren
.. autofunction:: matlab2cpp.collection.Plus
.. autofunction:: matlab2cpp.collection.Program
.. autofunction:: matlab2cpp.collection.Project
.. autofunction:: matlab2cpp.collection.Resize
.. autofunction:: matlab2cpp.collection.Return
.. autofunction:: matlab2cpp.collection.Returns
.. autofunction:: matlab2cpp.collection.Set
.. autofunction:: matlab2cpp.collection.Sget
.. autofunction:: matlab2cpp.collection.Sset
.. autofunction:: matlab2cpp.collection.Statement
.. autofunction:: matlab2cpp.collection.String
.. autofunction:: matlab2cpp.collection.Struct
.. autofunction:: matlab2cpp.collection.Structs
.. autofunction:: matlab2cpp.collection.Switch
.. autofunction:: matlab2cpp.collection.Transpose
.. autofunction:: matlab2cpp.collection.Try
.. autofunction:: matlab2cpp.collection.Tryblock
.. autofunction:: matlab2cpp.collection.Var
.. autofunction:: matlab2cpp.collection.Vector
.. autofunction:: matlab2cpp.collection.Warning
.. autofunction:: matlab2cpp.collection.While



Translation rules
=================
.. automodule:: matlab2cpp.rules
