"""
.. _usr00:

Matlab2cpp is a semi-automatic tool for converting code from Matlab to C++. matlab2cpp is written in Python and is a Python module. Installing the Matlab2cpp module, makes the module available in Python as a module and can be loaded with "import matlab2cpp". In addition to the module, the script "m2cpp is copied to a folder on the system so that it can be executed by typing "m2cpp" in the terminal (Windows: cmd, cygwin). The "m2cpp" is a small script to handle the input arguments which are then used by the functionality in the module Matlab2cpp.

Note that Matlab2cpp/m2cpp is not meant as a complete tool for creating runnable C++ code.
For example, the `eval`-function can not be supported because there is no
general way to implement it in C++.  Instead the program is aimed as a support
tool, which aims at speed up the conversion process as much as possible for
a user that needs to convert Matlab programs by hand anyway. The software does
this by converting the basic structures of the Matlab-program (functions,
branches, loops, etc.), adds variable declarations, and for some simple code, do
a complete translation. From there manual conversions can be
done by hand.

Matlab2cpp generate C++ code that relies on the linear algebra library Armadillo (http://arma.sourceforge.net/). So while Armadillo isn't required to generate the C++ code, Armadillo is required to compile the program.  Armadillo's API is quite similar to Matlab and cover some of Matlab's functionaliy. Matlab2cpp aims to correctly translate Matlab to the corresponding C++ Armadillo code. Currently, the code will not convert the large library collection of functions
that Matlab currently possesses. However, there is no reason for the code not
to support more of these features in time.

"""
