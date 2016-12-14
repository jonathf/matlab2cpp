"""
"""

import matlab2cpp

def set(node, types):

    includes = node.program[0]

    # Includes
    for key in types:
        #print includes.names

        if key not in includes.names:
            if write_to_includes(key):
                matlab2cpp.collection.Include(includes, key)


def get(node):

    includes = node.program[0]

    types_i = []
    for include in includes:
        if write_to_includes(include.name):
            types_i.append(include.name)

    return types_i


def write_to_includes(include_string):
    write = True
    not_to_include = ['#include <armadillo>', '#include "SPlot.h"', '#include <tbb/tbb.h>', 'include "mconvert.h"']

    if include_string in not_to_include:
        write = False
    return write


class Itypes(object):

    def __get__(self, instance, owner):
        return get(instance)

    def __set__(self, instance, value):
        set(instance, value)


if __name__ == "__main__":
    import doctest
    import matlab2cpp as mc
    doctest.testmod()
