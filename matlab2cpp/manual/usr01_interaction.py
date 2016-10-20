"""
.. _usr01:

User interaction
================

The simplest way to interact with the `Matlab2cpp`-toolbox is to use the
`m2cpp` frontend.  The script automatically creates files with various
extensions containing translations and/or meta-information.

.. autoprogram:: m2cpp:parser
    :prog: m2cpp

For the user, the flags -o, -c, -s, -S, -r, -p -omp, -tbb are the useful flags.
The flags -t, -T  are good for debugging because they print the structure of the 
Abstract Syntax Tree (AST). The -d flag gives useful
information on the parsing of the Matlab code and insight in how the AST is built.

Suggest flags, -s, -S
---------------------

Read the section :ref:`usr02_suggestion_engine` first.
When using m2cpp the corresponding suggest is set with the flag -s. The suggest
engine works well for simple cases. For more complex cases, not all the variables
get a type suggestion and the suggested type could be wrong. 

The other suggest flag -S get the datatypes by running the (Matlab) code with Matlab.
Information of the datatypes are written to files which can be extracted by the code 
translator. For this flag to work, in addition to having Matlab installed, the Matlab 
Engine API for Python has to be installed
(see: `Install MATLAB Engine API for Python <http://se.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html>`_).
Matlab has to be able to run the code to extract the datatypes. So if the code
require datafiles or special Matlab modules (e.g. numerical modules),
these have to be available for this option to work. The Matlab suggest option is not 100%,
but still quite good at suggesting datatypes. A downside with the using Matlab to suggest
datatypes, is that Matlab takes some time to start up and then run the (Matlab) code.

Multiple directories, -p paths_file
-----------------------------------

In Matlab the script and function files have to be in the same folder for the function files to be found. To call a function script located in a different folder, the folder has to be added to path. This can be done with `addpath` or `path`. In a separate file from the Matlab main and function scripts, a separate script can be written to set the path to different folders::

    Dir='/path_to_folder/SeismicLab/codes/';
    path(path, strcat(Dir,'bp_filter/'));
    path(path, strcat(Dir,'decon'));
    path(path, strcat(Dir,'dephasing'));
    path(path, strcat(Dir,'fx'));
    ...

The flag option `-p paths_file` can be set to parse such a file. Then Matlab as well as m2cpp can find function scripts that are located in other directories.
    
.. _parallel_flags:

Parallel flags, -omp, -tbb
--------------------------

The program m2cpp can do parallelization of simple for loops (so called embarrasingly parallel).
To let the program know which loops the user wants to parallelize, use the pragma `%#PARFOR`
before the loop (similar to the way its done in OpenMP). The flags -omp and -tbb can then
be used to chose if OpenMP code or TBB code will be inserted to parallelize the code. Matlab's
`parfor` doesn't require the pragma `%#PARFOR` to parallelize. If neither -omp nor -tbb flag is
used, no OpenMP or TBB code is inserted and we will get a sequential for loop.
When compiling,  try link flags `-fopenmp` for OpenMP and `-ltbb` for TBB. OpenMP is usually available
for the compiler out of the box. TBB needs to be installed (see: https://www.threadingbuildingblocks.org/).
The TBB code makes use of lambda functions which is a C++ feature. C++11 is probably not set as
standard for the compiler, i.e., in the GNU compiler g++, the flag
`-std=c++11` is required to make use of C++11 features.

Quick translation functions
---------------------------

Even though `m2cpp` is sufficient for performing all code translation, many
of the examples in this manual are done through a python interface, since some
of the python functionality also will be discussed.  Given that `Matlab2cpp`
is properly installed on your system, the python library is available in
Python's path. The module is assumed imported as::

    >>> import matlab2cpp as mc

Quick functions collection of frontend tools for performing code translation.
Each of the function :py:func:`~matlab2cpp.qcpp`, :py:func:`~matlab2cpp.qhpp`,
:py:func:`~matlab2cpp.qpy` and :py:func:`~matlab2cpp.qlog` are directly related
to the functionality of the :program:`m2cpp` script. The name indicate the
file extension that the script will create.  In addition there are the three
functions :py:func:`~matlab2cpp.qtree` and :py:func:`~matlab2cpp.qscript`. The
former represents a summary of the created node tree. The latter is a simple
translation tool that is more of a one-to-one translation.

For an overview of the various quick-functions, see :ref:`dev01`.

Plotting functionality
----------------------

Plotting functionality is available through a wrapper, which calls Python's matplotlib.
If a Matlab code with plotting calls is translated, the file `SPlot.h` is generated.
The C++ file that is generated also `#include` this file. To compile the generated code,
the Python have to be included. The code in `SPlot.h` makes of C++11 features, so compiler
options for C++11 may be needed as well. With the GNU compiler g++, I can compile
the generated code with:
`g++ my_cpp_file.cpp -o runfile -I /usr/include/python2.7/ -lpython2.7 -larmadillo -std=c++11`

Additional flags could be -O3 (optimization) -ltbb (in case of TBB parallelization)
"""
import matlab2cpp as mc
