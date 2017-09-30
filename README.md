matlab2cpp is a semi-automatic tool for converting code from Matlab to C++. At the moment, matlab2cpp is the name of the python module while m2cpp is the name of the python script. m2cpp is found in the root folder. When installing the matlab2cpp module, the python script is copied to a system folder so that the script is available in path. Then the m2cpp script can be executed by typing "m2cpp" in the command line interface (cmd in Windows, terminal in Linux).

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
* C++11 (Plotting and TBB require C++11)

Optional:

* TBB
* Sphinx (for compiling documentation)
* Argcomplete (for tab-completion support)

Linux/Mac:

As root, run the following command::

    $ python setup.py install

In addition to installing the matlab2cpp module, the executable ´m2cpp´ is copied to "/usr/local/bin/"
The executable ´m2cpp´ is now available from path.

Windows:

    > Python setup.py install

A bat script is created so that m2cpp.py can be executed by typing m2cpp.
The bat script and m2cpp.py is copied to "sys.executable". "sys.executable" is the location where Python is installed.
The executable ´m2cpp´ is now available from path.

Linux, Mac, Windows:

If you want to put the executable m2cpp in another place, modify the setup.py file. From line 27 starts the code which
makes the m2cpp.py file available from path. Alternatively, remove the code from line 27. The executable m2cpp.py can freely be copied or be added to path or environmental variables manually (with or without the `.py` extension).

Armadillo:

Armadillo is a linear algebra library for the C++ language. The Armadillo library can be found at http://arma.sourceforge.net. 
Some functionality in Armadillo rely on a math library like LAPACK, BLAS, OpenBLAS or MKL. When installing Armadillo, it will look for installed math libraries. 
If Armadillo is installed, the library can be linked with the link flag `-larmadillo`. Armadillo can also be linked directly, see the `FAQ` at the Armadillo webpage for more information. 

I believe MKL is the fastest math library and it can be downloaded for free at https://software.intel.com/en-us/articles/free-mkl.

TBB:

By inserting pragmas in the Matlab code, for loops can be marked by the user. The program can then either insert OpenMP or TBB code to parallelize the for loop. To compile TBB code, the TBB library has to be installed. See :ref:`parallel_flags` for more details.

Sphinx::

    pip install sphinx
    pip install sphinxcontrib-autoprogram
    pip install sphinxcontrib-napoleon
    pip install sphinx-argparse

Argcomplete::

    pip install argcomplete
    activate-global-python-argcomplete

This only works for Bash and would require a restart of terminal emulator.


An illustrating Example
-----------------------

Assuming Linux installation and `m2cpp` is available in path.
Code works analogous in Mac and Windows.

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

This will create two files: `example.m.hpp` and `example.m.py`.

In example.m.hpp, the translated C++ code is placed. It looks as
follows::

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
Declarations can be done in the file `example.m.py`. After the first run, it
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
the `-s` flag::

    $ m2cpp example.m -s

The file `example.m.py` will then automatically be populated with data types
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

It will not always be successful and some of the types might in
some cases be wrong.  It is therefore also possible to adjust these
values manually at any time.

Having run the conversion with the variables converted, creates a
new output for `example.m.hpp`::

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
