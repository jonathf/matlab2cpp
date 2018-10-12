.. attention::

    Matlab2cpp er currently unmaintained. As a mainteiner this project ended up
    on the short end of the stick of what I unfortunatly have time for.

    Anyone who want to make changes to it, might do so. I am very open to
    a change in overship.

    I am sorry for the inconvinience.

    Jonathan

==========
Matlab2Cpp
==========

``matlab2cpp`` is a semi-automatic tool for converting code from Matlab to C++.

After installing, the ``matlab2cpp`` command line executable ``m2cpp`` will be
available in path that can be used to convert Matlab code.

Note that it is not meant as a complete tool for creating runnable C++ code.
For example, the `eval`-function can not be supported because there is no
general way to implement it in C++. Instead the program is a support tool,
which aims at speed up the conversion process as much as possible for a user
that needs to convert Matlab programs by hand anyway. The software does this by
converting the basic structures of the Matlab-program (functions, branches,
loops, etc.), adds variable declarations, and for some simple code, do
a complete translation. And any problem the program encounters during
conversion will be written in a log-file. From there manual conversions can be
done by hand.

Currently, the code will not convert the large library collection of functions
that Matlab currently possesses. However, there is no reason for the code not
to support these features in time. The extension library is easy to extend.

Installation
------------
Installation by running the ``pip`` command::

    pip install matlab2cpp

The source-to-source parser do not have any requirements beyond having Python
installed. However, the generated output does have a few requirements to be
compilable. They are as follows.

``C++11``
    Code produces follows the ``C++11`` standard.
``armadillo``
    Armadillo is a linear algebra library for the C++ language. The Armadillo
    library can be found at `http://arma.sourceforge.net`_. Some functionality
    in Armadillo rely on a math library like LAPACK, BLAS, OpenBLAS or MKL.
    When installing Armadillo, it will look for installed math libraries.

    If Armadillo is installed, the library can be linked with the link flag
    ``-l armadillo``. Armadillo can also be linked directly, see the ``FAQ`` at
    the Armadillo webpage for more information.

    I believe MKL is the fastest math library and it can be downloaded for free
    at `https://software.intel.com/en-us/articles/free-mkl`_.
``TBB``
    By inserting pragmas in the code, for loops can be marked by the user. The
    program can then either insert ``OpenMP`` or ``TBB`` code to parallelize
    the for loop. To compile ``TBB`` code, the ``TBB`` library has to be
    installed. See :ref:`parallel_flags` for more details.

An illustrating Example
-----------------------

Assuming Linux installation and `m2cpp` is available in path. Code works
analogous in Mac and Windows.

Consider a file `example.m` with the following content::

    function y=f(x)
        y = x+4
    end
    function g()
        x = [1,2,3]
        f(x)
    end

Run conversion on the file: ::

    $ m2cpp example.m

This will create two files: ``example.m.hpp`` and ``example.m.py``.

In ``example.m.hpp``, the translated C++ code is placed. It looks as follows::

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

Matlab doesn't declare variables explicitly, so m2cpp is unable to complete
the translation.  To create a full conversion, the variables must be declared.
Declarations can be done in the file ``example.m.py``. After the first run, it
will look as follows::

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
    # char    string  struct  structs func_lambda

    functions = {
      "f" : {
        "y" : "",
        "x" : "",
      },
      "g" : {
        "x" : "",
      },
    }
    includes = [
      '#include <armadillo>',
      'using namespace arma ;',
    ]

In addition to defining includes at the bottom, it is possible to declare
variables manually by inserting type names into the respective empty strings.
However, some times it is possible to guess some of the variable types from
context.  To let the software try to guess variable types, run conversion with
the ``-s`` flag::

    $ m2cpp example.m -s

The file ``example.m.py`` will then automatically be populated with data types
from context::

    # ...

    functions = {
      "f" : {
        "y" : "irowvec",
        "x" : "irowvec",
      },
      "g" : {
        "x" : "irowvec",
      },
    }
    includes = [
      '#include <armadillo>',
      'using namespace arma ;',
    ]

It will not always be successful and some of the types might in some cases be
wrong. It is therefore also possible to adjust these values manually at any
time.

Having run the conversion with the variables converted, creates a new output
for ``example.m.hpp``::

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

This is valid and runnable C++ code. For such a small example, no manual
adjustments were necessary.
