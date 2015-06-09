.. toctree::
   :maxdepth: 2


Matlab2cpp
==========

Setup
=====

.. automodule:: matlab2cpp.__init__

Installation
------------

Requirements:

* Python 2.7.3
* Armadillo (Not required for running, but generator
  creates armadillo code.)

Linux/Mac:

As root, run the following command:::

    $ python setup.py install

The executable ´mconvert´ is now available from path.

Windows:::

    > Python setup.py install

The executable mconvert.py can freely be copied or be added to
environmental variables manually.

Usage
-----

Assuming Linux installation and ´mconvert´ available in path.
Code works analogous in Mac and Windows.

Consider the following code snippet in the file ´example.m´: ::

    function y=f(x)
        y = x+4
    end
    function g()
        x = [1,2,3]
        f(x)
    end

Run conversion on the file:

    $ mconvert example.m

This will create three files: `example.m.cpp`, `example.m.py` and
`example.m.log`.

In example.m.cpp, the translated C++ code is placed. It looks as
follows: ::

    #include <armadillo>
    using namespace arma ;

    TYPE f(TYPE x)
    {
      TYPE y ;
      y = x+4 ;
      return y ;
    }

    void g()
    {
      TYPE x ;
      x = [1, 2, 3] ;
      f(x) ;
    }

Matlab doesn't declare variables explicitly, so
Matlab2cpp is not able to do a complete translation.
To create a full conversion, the variables must be declared.
Declarations can be done in the file `example.m.py`: ::

    # Supplement file
    #
    # Valid inputs:
    #
    # uint    int     float   double cx_double
    # uvec    ivec    fvec    vec    cx_vec
    # urowvec irowvec frowvec rowvec cx_rowvec
    # umat    imat    fmat    mat    cx_mat
    # ucube   icube   fcube   cube   cx_cube
    #
    # func_lambda
    # char

    scope = {}

    g = scope["g"] = {}
    g["y"] = ""
    g["x"] = ""

    f = scope["f"] = {}
    f["y"] = ""
    f["x"] = ""

It is then possible to declare variables by inserting type names
into the respective empty strings.

However, some times it is possible to guess some of the variable
types from context.
To use suggestions, run conversion with the `-s` flag:

    $ mconvert example.m -s

The file `example.m.py` will then automatically be filled with
types from context: ::


    # ...

    scope = {}

    g = scope["g"] = {}
    g["x"] = "irowvec"

    f = scope["f"] = {}
    f["y"] = "irowvec"
    f["x"] = "irowvec"

It will not always be sucsessful and some of the types might in
some cases be wrong.  It is therefore also possible to adjust these
values at any time.

Having run the conversion with the variables converted, creates a
new output for `example.m.cpp`: ::

    #include <armadillo>
    using namespace arma ;

    irowvec f(irowvec x)
    {
      irowvec y ;
      y = x+4 ;
      return y ;
    }

    void g()
    {
      irowvec x ;
      int _x [] = [1, 2, 3] ;
      x = irowvec(_x, 3, false) ;
      f(x) ;
    }

The file `example.m.log` will contain a list of errors and warnings
created during conversion.

Program frontend (`mconvert`)
=============================

TODO as soon as sphinxarg is working
.. argparse::
    :module: matlab2cpp
    :func: create_parser
    :prog: mconvert

Suppliment configuration (`.py`)
================================

.. automodule:: matlab2cpp.


Code snippits
=============

matlab2cpp.datatype module
--------------------------

.. automodule:: matlab2cpp.datatype
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.generate module
--------------------------

.. automodule:: matlab2cpp.generate
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.node module
----------------------

.. automodule:: matlab2cpp.node
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.reference module
---------------------------

.. automodule:: matlab2cpp.reference
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.treebuilder module
-----------------------------

.. automodule:: matlab2cpp.treebuilder
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.utils module
-----------------------

.. automodule:: matlab2cpp.utils
    :members:
    :undoc-members:
    :show-inheritance:


Module contents
---------------

.. automodule:: matlab2cpp
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.snippets.snippets module
-----------------------------------

.. automodule:: matlab2cpp.snippets.snippets
    :members:
    :undoc-members:
    :show-inheritance:


Module contents
---------------

.. automodule:: matlab2cpp.snippets
    :members:
    :undoc-members:
    :show-inheritance:


Translation targets
===================

matlab2cpp.targets.arma_common module
-------------------------------------

.. automodule:: matlab2cpp.targets.arma_common
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.assign_common module
---------------------------------------

.. automodule:: matlab2cpp.targets.assign_common
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.cell module
------------------------------

.. automodule:: matlab2cpp.targets.cell
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.char module
------------------------------

.. automodule:: matlab2cpp.targets.char
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.code_block module
------------------------------------

.. automodule:: matlab2cpp.targets.code_block
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.cube module
------------------------------

.. automodule:: matlab2cpp.targets.cube
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.cube_common module
-------------------------------------

.. automodule:: matlab2cpp.targets.cube_common
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.cx_cube module
---------------------------------

.. automodule:: matlab2cpp.targets.cx_cube
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.cx_double module
-----------------------------------

.. automodule:: matlab2cpp.targets.cx_double
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.cx_mat module
--------------------------------

.. automodule:: matlab2cpp.targets.cx_mat
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.cx_rowvec module
-----------------------------------

.. automodule:: matlab2cpp.targets.cx_rowvec
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.cx_vec module
--------------------------------

.. automodule:: matlab2cpp.targets.cx_vec
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.double module
--------------------------------

.. automodule:: matlab2cpp.targets.double
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.expression module
------------------------------------

.. automodule:: matlab2cpp.targets.expression
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.fcube module
-------------------------------

.. automodule:: matlab2cpp.targets.fcube
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.float module
-------------------------------

.. automodule:: matlab2cpp.targets.float
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.fmat module
------------------------------

.. automodule:: matlab2cpp.targets.fmat
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.frowvec module
---------------------------------

.. automodule:: matlab2cpp.targets.frowvec
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.func_common module
-------------------------------------

.. automodule:: matlab2cpp.targets.func_common
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.func_lambda module
-------------------------------------

.. automodule:: matlab2cpp.targets.func_lambda
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.func_return module
-------------------------------------

.. automodule:: matlab2cpp.targets.func_return
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.func_returns module
--------------------------------------

.. automodule:: matlab2cpp.targets.func_returns
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.fvec module
------------------------------

.. automodule:: matlab2cpp.targets.fvec
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.icube module
-------------------------------

.. automodule:: matlab2cpp.targets.icube
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.ifloat module
--------------------------------

.. automodule:: matlab2cpp.targets.ifloat
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.iint module
------------------------------

.. automodule:: matlab2cpp.targets.iint
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.imat module
------------------------------

.. automodule:: matlab2cpp.targets.imat
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.int module
-----------------------------

.. automodule:: matlab2cpp.targets.int
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.irowvec module
---------------------------------

.. automodule:: matlab2cpp.targets.irowvec
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.ivec module
------------------------------

.. automodule:: matlab2cpp.targets.ivec
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.mat module
-----------------------------

.. automodule:: matlab2cpp.targets.mat
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.mat_common module
------------------------------------

.. automodule:: matlab2cpp.targets.mat_common
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.matrix module
--------------------------------

.. automodule:: matlab2cpp.targets.matrix
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.program module
---------------------------------

.. automodule:: matlab2cpp.targets.program
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.reserved module
----------------------------------

.. automodule:: matlab2cpp.targets.reserved
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.rowvec module
--------------------------------

.. automodule:: matlab2cpp.targets.rowvec
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.rowvec_common module
---------------------------------------

.. automodule:: matlab2cpp.targets.rowvec_common
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.sandbox module
---------------------------------

.. automodule:: matlab2cpp.targets.sandbox
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.string module
--------------------------------

.. automodule:: matlab2cpp.targets.string
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.struct module
--------------------------------

.. automodule:: matlab2cpp.targets.struct
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.structs module
---------------------------------

.. automodule:: matlab2cpp.targets.structs
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.ucube module
-------------------------------

.. automodule:: matlab2cpp.targets.ucube
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.umat module
------------------------------

.. automodule:: matlab2cpp.targets.umat
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.unknown module
---------------------------------

.. automodule:: matlab2cpp.targets.unknown
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.urowvec module
---------------------------------

.. automodule:: matlab2cpp.targets.urowvec
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.uvec module
------------------------------

.. automodule:: matlab2cpp.targets.uvec
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.uword module
-------------------------------

.. automodule:: matlab2cpp.targets.uword
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.variables module
-----------------------------------

.. automodule:: matlab2cpp.targets.variables
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.vec module
-----------------------------

.. automodule:: matlab2cpp.targets.vec
    :members:
    :undoc-members:
    :show-inheritance:

matlab2cpp.targets.vec_common module
------------------------------------

.. automodule:: matlab2cpp.targets.vec_common
    :members:
    :undoc-members:
    :show-inheritance:


Module contents
---------------

.. automodule:: matlab2cpp.targets
    :members:
    :undoc-members:
    :show-inheritance:
