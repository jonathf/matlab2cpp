Matlab2cpp is a semi-automatic tool for converting code from Matlab to C++.

Note that it is not meant as a complete tool for creating runnable C++ code.
For example, the `eval`-function will not be supported because there is no
general way to implement it in C++.
Instead the program is aimed as support tool, which aims at speed up the
conversion process as much as possible for a user that needs to convert Matlab
programs by hand anyway.
The software does this by converting the basic structures of the
Matlab-program (functions, branches, loops, etc.), adds
variable declarations, and for some lower level code, do a complete
translation.
Any problem the program encounters will be written in a log-file.

Currently, the code will not convert the large library collection
of functions that Matlab currently possesses.
However, there is no reason for the code not to support these features in time.

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
