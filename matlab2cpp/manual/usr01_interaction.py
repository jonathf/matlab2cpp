"""
.. _usr01:

User interaction
================

The simplest way to interact with the `Matlab2cpp`-toolbox is to use the
`m2cpp` frontend.  The script automatically creates files with various
extensions containing translations and/or meta-information.

.. autoprogram:: m2cpp:parser
    :prog: m2cpp

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
"""
import matlab2cpp as mc
