..tex toctree::
   :maxdepth: 2


Matlab2cpp
==========

Introduction
============

.. automodule:: matlab2cpp

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
environmental variables manually (with or without the `.py` extendtion).



Example
-------

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

.. argparse::
    :module: matlab2cpp.__init__
    :func: create_parser
    :prog: mconvert

Suppliment configuration (`matlabfile.py`)
==========================================

.. automodule:: matlab2cpp.supplement

Functions
=========

Suppliment configuration (`matlabfile.py`)
------------------------------------------

.. autofunction:: matlab2cpp.supplement.set_variables
.. autofunction:: matlab2cpp.supplement.get_variables
.. autofunction:: matlab2cpp.supplement.str_variables

Code translation
================

Translation rules
-----------------

.. automodule:: matlab2cpp.translations.__init__

Administrative translation
--------------------------

.. autofunction:: matlab2cpp.target._program.Program

Mathematical Variables
----------------------
.. autofunction:: matlab2cpp.translations._arma_common.configure_arg

Codeblock translation
---------------------
.. automodule:: matlab2cpp.supplement

.. autofunction:: matlab2cpp.translations._assign_common.Assign

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

