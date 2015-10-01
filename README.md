Matlab2cpp is a semi-automatic tool for converting code from Matlab to C++.

Note that it is not meant as a complete tool for creating runnable C++ code.
For example, the `eval`-function can not be supported because there is no
general way to implement it in C++.  Instead the program is aimed as a support
tool, which aims at speed up the conversion process as much as possible for
a user that needs to convert Matlab programs by hand anyway.  The software does
this by converting the basic structures of the Matlab-program (functions,
branches, loops, etc.), adds variable declarations, and for some simple code, do
a complete translation.  And any problem the program encounters during
conversion will be written in a log-file. From there manual conversions can be
done by hand.

Currently, the code will not convert the large library collection of functions
that Matlab currently possesses.  However, there is no reason for the code not
to support these features in time. The extension library is easy to extend.

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

Windows:

    > Python setup.py install

The executable mconvert.py can freely be copied or be added to
environmental variables manually (with or without the `.py` extension).



An illustrating Example
-----------------------

Assuming Linux installation and `mconvert` available in path.
Code works analogous in Mac and Windows.

Consider a file `example.m` with the following content: ::

    function y=f(x)
        y = x+4
    end
    function g()
        x = [1,2,3]
        f(x)
    end

Run conversion on the file: ::

    $ mconvert example.m

This will create two files: `example.m.hpp` and `example.m.py`.

In example.m.hpp, the translated C++ code is placed. It looks as
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

Matlab doesn't declare variables explicitly, so Matlab2cpp is unable to complete
the translation.  To create a full conversion, the variables must be declared.
Declarations can be done in the file `example.m.py`. After the first run, it
will look as follows: ::

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
the `-s` flag: ::

    $ mconvert example.m -s

The file `example.m.py` will then automatically be populated with data types
from context: ::


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

It will not always be successful and some of the types might in
some cases be wrong.  It is therefore also possible to adjust these
values manually at any time.

Having run the conversion with the variables converted, creates a
new output for `example.m.hpp`:

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

This is valid and runnable C++ code.
For such a small example, no manual adjustments were necesarry.
