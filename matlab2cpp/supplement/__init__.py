"""
"""

PREFIX = """# encoding: utf-8
#
# Supplement file
#
# Valid inputs:
#
# uword   int     float   double cx_double
# uvec    ivec    fvec    vec    cx_vec
# urowvec irowvec frowvec rowvec cx_rowvec
# umat    imat    fmat    mat    cx_mat
# ucube   icube   fcube   cube   cx_cube
#
# char    string  struct  structs func_lambda
"""

from .functions import Ftypes
from .suggests import  Sstypes
from .structs import Stypes
from .includes import Itypes
from .verbatim import Vtypes

import matlab2cpp as mc


def str_variables(types_f={}, types_s={}, types_i=[],
        suggest={}, prefix=True, types_v={}):
    """
Convert a nested dictionary for types, suggestions and structs and use them to
create a suppliment text ready to be saved.

Kwargs:
    types_f (dict): Function variables datatypes
    types_s (dict): Struct variables datatypes
    types_i (list): Includes in header
    types_v (dict): Verbatim translations
    suggest (dict): Suggested datatypes for types_f and types_s
    prefix (bool): True if the type explaination should be included

Returns: str
    String representation of suppliment file

Example:
    >>> types_f = {"f" : {"a":"int"}, "g" : {"b":""}}
    >>> types_s = {"c" : {"d":""}}
    >>> types_i = ["#include <armadillo>"]
    >>> suggest = {"g" : {"b":"float"}, "c" : {"d":"vec"}}
    >>> print(str_variables(types_f, types_s, types_i, suggest, prefix=False))
    functions = {
      "f" : {
        "a" : "int",
      },
      "g" : {
        "b" : "", # float
      },
    }
    structs = {
      "c" : {
        "d" : "", # vec
      },
    }
    includes = [
      '#include <armadillo>',
    ]
    """

    if prefix:
        out = PREFIX
    else:
        out = ""

    if types_f:

        if prefix:
            out += "\n"

        out += "functions = {\n"

        keys = types_f.keys()
        keys.sort()

        for name in keys:


            out += '  "%s" : {\n' % (name)
            types = types_f[name]

            keys2 = types.keys()
            keys2.sort()
            l = max([len(k) for k in keys2]+[0])+4

            for key in keys2:
                val = types[key]
                sug = suggest.get(name, {}).get(key, "")

                if key[:1] == "_":
                    continue

                elif val:
                    out += " "*(l-len(key)) + '"%s" : "%s",\n' % (key, val)

                elif sug:
                    out += " "*(l-len(key)) + '"%s" : "", # %s\n' % (key, sug)

                else:
                    out += " "*(l-len(key)) + '"%s" : "",\n' % (key)

            out += "  },\n"

        out += "}"

    if types_s:

        if types_f or prefix:
            out += "\n"

        out += "structs = {\n"

        keys = types_s.keys()
        keys.sort()

        for name in keys:

            out += '  "%s" : {\n' % (name)
            types = types_s[name]

            keys2 = types.keys()
            keys2.sort()
            l = max([len(k) for k in keys2])+4

            for key in keys2:
                val = types[key]
                sug = suggest.get(name, {}).get(key, "")

                if key[-5:] == "_size":
                    val = val or 100
                    out += " "*(l-len(key)) + '"%s" : %s,\n' % (key, val)

                elif val:
                    out += " "*(l-len(key)) + '"%s" : "%s",\n' % (key, val)

                elif sug:
                    out += " "*(l-len(key)) + '"%s" : "", # %s\n' % (key, sug)

                else:
                    out += " "*(l-len(key)) + '"%s" : "",\n' % (key)

            out += "  },\n"

        out += "}"

    if types_i:

        if prefix or types_f or types_s:
            out += "\n"

        out += "includes = [\n"

        for key in types_i:
            if key:
                out += "  '" + key + "',\n"

        out += "]"

    if types_v:

        if types_f or prefix or types_s or types_i:
            out += "\n"

        out += "verbatims = {\n"

        keys = types_v.keys()
        keys.sort()
        l = max([len(k) for k in keys])+2

        for key in keys:
            val = types_v[key]
            if "\n" in val:
                out += " "*(l-len(key)) + '"%s" : """%s""",\n' % (key, val)
            else:
                out += " "*(l-len(key)) + '"%s" : "%s",\n' % (key, val)

        out += "}"

    return out


if __name__ == "__main__":
    import doctest
    doctest.testmod()

