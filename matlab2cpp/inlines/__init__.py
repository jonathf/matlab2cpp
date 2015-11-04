import snippets
import os

def retrieve(node, name, **kws):

    if os.path.isfile(name):

        name = os.path.relpath(name, os.path.dirname(node.program.name))
        include_code = '#include "%s.hpp"' % name
        library_code = ""

        if node.name == name:
            include_code = ""

    else:

        library_code = ""
        if name == "Splot":
            include_code = '#include "Splot.h"'

        elif name == "m2cpp":
            include_code = '#include "m2cpp.h"'

        elif name == "arma":
            include_code = "#include <armadillo>"
        else:
            include_code = ""

    return include_code, library_code
