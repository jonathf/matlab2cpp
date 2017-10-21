r"""
.. usr05:

Installation
============

Requirements:

* Python 2.7.3
* Armadillo (Not required for running, but generator
  creates armadillo code.)


Optional:

* C++11 (Plotting and TBB require C++11)
* Intel Threading Building Blocks (TBB)
* Intel Math Kernel Library (MKL)
* MATLAB Engine API for Python
* Matplotlib (Python module required for plotting)
* Sphinx (for compiling documentation)
* Argcomplete (for tab-completion support)

Installing Python
-----------------


Installing Armadillo
--------------------

Armadillo can be downloaded at http://arma.sourceforge.net/ . Some of the functionality of Armadillo is a kind of wrapper and relies on a math library as BLAS, OpenBLAS, LAPACK, MKL. To compute x = A\\b or perform fast matrix-matrix multiplication one or more of these math libraries are required. See the Armadillo webpage for details. Install the required math library before installing Armadillo.  Armadillo creates a dynamic library when it is compiled and installed. This dynamic library is configured to use one or more of the math libraries which were found when it was created. You don't need to install Armadillo and use link Armadillo to your program with the dynamic library. It is possible to give include and library path to Armadillo as well as link in one or more math libraries (BLAS, OpenBLAS, LAPACK, MKL). 

You could think of this as manually specifying the linking versus linking the dynamic Armadillo library where which math library to use has already been set. Even if you install Armadillo you have the option to link Armadillo by setting include, linking path and additional flags to link the math library.


Installing Matlab2cpp
---------------------

Matlab2cpp is written in Python. When running the translator program the Matlab2cpp is imported as a module its functionality is used to parse and translate Matlab code to C++. Because of this Python 2.7 is a requirement. 

Matlab2cpp is Open-source and is available at Github (https://github.com/emc2norway/m2cpp) . With the `git` software installed the software can be downloaded to the current folder by typing::

    git clone git@github.com:emc2norway/m2cpp.git

in a terminal (in Windows: cmd, cygwin). Move to the downloaded code with `"cd m2cpp"`. Then the software can be installed by typing

Windows::

    python setup.py install

Mac/Linux::

    sudo python setup.py install

To update the Matlab2cpp to a newer version on git, enter a terminal and move to the folder where you downloaded Matlab2cpp with git clone. To pull the latest version on Github type::

    git pull

and then re-install with the same command used to install the first time as described above. When installing the module 


Installing optional packages
----------------------------

Among these optional packages, TBB, MKL and configuring Matlab to suggest datatypes are probably the most intereting/useful features.

By inserting pragmas in the Matlab code, for loops can be marked by the user. The program can then either insert OpenMP or TBB code to parallelize the for loop. By putting this pragma before the for loop the user guarranties that the iterations are independent and write to different memory locations. To compile TBB code, the TBB library has to be installed. Most compilers now adays come with built in support for OpenMP, therefore no installation should be necessary.

It may not be well known, but MKL is available for free. MKL isn't necessarry as BLAS, OpenBLAS, LAPACK could be used intead.u

C++ is a static language. This means that the variables have to be declared and have the specified datatype. At the moment some of variable types in the generated C++ code can be deduced from the Matlab code. Another option is to run the Matlab code with Matlab and get the datatypes Matlab used when executing the Matlab code. To make use of this option, you need a sufficiently new Matlab version installed (works on R2015b) on your computer.

The plotting functional provided by Matlab2cpp is done by a wrapper for Python's matplotlib module. This wrapper also makes use of C++11 functionality. Compiling the generated C++ code require C++11, Python and Matplotlib. 

Intel Threading Building Blocks (TBB)
+++++++++++++++++++++++++++++++++++++

TBB can be downloaded at https://www.threadingbuildingblocks.org/. On the linux distribution Ubuntu, TBB can be installed from the terminal with the command: `sudo apt-get install libtbb-dev`


Intel Math Kernel Library (MKL)
+++++++++++++++++++++++++++++++

MKL can be downloaded for free at https://software.intel.com/en-us/articles/free-mkl


MATLAB Engine API for Python
++++++++++++++++++++++++++++

Follow the instrucion at: http://se.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html

Matplotlib (Python module required for plotting)
++++++++++++++++++++++++++++++++++++++++++++++++

Matplotlib could be part of your Python installation by default. Else it can be installed with
::

    pip install matplotlib

Sphinx (for compiling documentation)
++++++++++++++++++++++++++++++++++++

::

    pip install sphinx
    pip install sphinxcontrib-autoprogram
    pip install sphinxcontrib-napoleon
    pip install sphinx-argparse



Argcomplete (for tab-completion support)
++++++++++++++++++++++++++++++++++++++++

::

    pip intall argcomplete
    activate-global-python-argcomplete

This only works for Bash and would require a restart of terminal emulator.

"""
