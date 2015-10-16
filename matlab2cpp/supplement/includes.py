"""
"""

import matlab2cpp

def set(node, types):

    includes = node.program[0]

    # Includes
    for key in types:

        if key not in includes.names:
            matlab2cpp.collection.Include(includes, key)


def get(node):

    includes = node.program[0]

    types_i = []
    for include in includes:
        types_i.append(include.name)

    return types_i


class Itypes(object):

    def __get__(self, instance, owner):
        return get(instance)

    def __set__(self, instance, value):
        set(instance, value)


if __name__ == "__main__":
    import doctest
    import matlab2cpp as mc
    doctest.testmod()
