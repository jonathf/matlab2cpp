"""
Translating Matlab code is done in two steps. First the Matlab code is
interpreted using the `Builder` module. It creates a tree
representation of the code where each segment of code is represented by a node.
To observe the node structure it possible to either use `mconvert` with the `-t`
option, or the python function `mc.qtree`. For example:

    >>> print mc.qtree("a = 2+2")
            Program    program      TYPE    unamed
            Includes   program      TYPE    
            | Include    program      TYPE    #include <armadillo>
            | Include    program      TYPE    using namespace arma ;
      1   1 Funcs      program      TYPE    unamed
      1   1 | Main       func_common  TYPE    main
      1   1 | | Declares   func_return  TYPE    
      1   1 | | | Var        unknown      (int)   a
      1   1 | | Returns    func_return  TYPE    
      1   1 | | Params     func_return  TYPE    
      1   1 | | Block      code_block   TYPE    
      1   1 | | | Assign     unknown      TYPE    
      1   1 | | | | Var        unknown      (int)   a
      1   5 | | | | Plus       expression   int     
      1   5 | | | | | Int        int          int     
      1   7 | | | | | Int        int          int     
            Inlines    program      TYPE    unamed
            Structs    program      TYPE    unamed
            Headers    program      TYPE    unamed
            Log        program      TYPE    unamed
            | Error      program      TYPE    Var:0

There is quite a lot going on in this picture. First of all, each line
represents a node. The columns represents repsectively

+---------------------+-------------------------------------+
| line number         | Matlab code line number (if any)    |
+---------------------+-------------------------------------+
| cursor number       | Matlab code cursor number (if any)  |
+---------------------+-------------------------------------+
| node class          | The node categorization type        |
+---------------------+-------------------------------------+
| translation handler | The rule used for translation       |
+---------------------+-------------------------------------+
| datatype            | The data type of the node           |
+---------------------+-------------------------------------+
| node name           | Name of the node (if any)           |
+---------------------+-------------------------------------+

There is a bit of meta-information in the code. This will not be assigned
neither line number nor cursor number. The remaining lines are the nodes used to
do the actual code translation. The can be interpreted as follows:

* The program consists of a collection of functions `Funcs`
* The collection of funcs contains one main function `Main`
* The mainfunction contain declaration info, return value info and parameter
  info in it's three first node children.
* The fourth child is the code block `Block` which contains the function
  content.
* The code block contains one code line, an assignment `Assign`.
* The assignment contains a left hand side variable `Var` and an expression
  right hand side `Plus`
* The expression `Plus` is addition and contains the two integers both classed
  `Int`.

The class of each node is determined as the are created as the Matlab code is
translated. The translation handler and the datatype however varies a bit. Some
are fixed, like that `Program` is handled by the `program` translation rule or
that `Int` have the datatype `int`. Others, like the variable `Var` can change
upong how the configuration is set up. Intutivly enough, if datatype is set to
`int`, then the translation handler will follow and also be `int`:

    >>> print mc.qtree("a = 2+2", suggest=True)
            Program    program      TYPE    unamed
            Includes   program      TYPE    
            | Include    program      TYPE    #include <armadillo>
            | Include    program      TYPE    using namespace arma ;
      1   1 Funcs      program      TYPE    unamed
      1   1 | Main       func_common  TYPE    main
      1   1 | | Declares   func_return  int     
      1   1 | | | Var        int          int     a
      1   1 | | Returns    func_return  TYPE    
      1   1 | | Params     func_return  TYPE    
      1   1 | | Block      code_block   TYPE    
      1   1 | | | Assign     unknown      TYPE    
      1   1 | | | | Var        int          int     a
      1   5 | | | | Plus       expression   int     
      1   5 | | | | | Int        int          int     
      1   7 | | | | | Int        int          int     
            Inlines    program      TYPE    unamed
            Structs    program      TYPE    unamed
            Headers    program      TYPE    unamed
            Log        program      TYPE    unamed

In other words, there are for these nodes, multiple translation for depending on
context. This is important to achieve the desired behavior.

Modules
~~~~~~~

builder

assign          
branches
codeblock
expression
findend
functions
identify
iterate
misc
variables

constants

"""

import matlab2cpp as mc
from builder import Builder
__all__ = ["Builder"]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
