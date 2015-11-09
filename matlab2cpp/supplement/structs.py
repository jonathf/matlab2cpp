"""
Data structures in Matlab can be constructed explicitly through the
`struct`-function.  However, they can also be constructed implicitly by direct
assignment.  For example will `a.b=4` create a `struct` with name `a` that has
one field `b`.  When translating such a snippet, it creates a C++-struct, such
that 

    >>> print mc.qhpp("function f(); a.b = 4.", suggest=True)
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    struct _A
    {
      double b ;
    } ;
    <BLANKLINE>
    void f()
    {
      _A a ;
      a.b = 4. ;
    }

In the suppliment file, the local variable `a` will be assigned as a `struct`.
In addition, since the struct has content, the suppliment file creates a new
section for structs.  It will have the following form:

    >>> print mc.qpy("function f(); a.b = 4.", suggest=True)
    functions = {
      "f" : {
        "a" : "struct",
      },
    }
    structs = {
      "a" : {
        "b" : "double",
      },
    }
    includes = [
      '#include <armadillo>',
      'using namespace arma ;',
    ]

Given that the data structure is in the form of an array, the process is similar
to a single element.  There is only two differences.  In the translation, the
struct is declared as an array:

    >>> print mc.qhpp("function f(); a(1).b = 4.", suggest=True)
    #include <armadillo>
    using namespace arma ;
    <BLANKLINE>
    struct _A
    {
      double b ;
    } ;
    <BLANKLINE>
    void f()
    {
      _A a[100] ;
      a[0].b = 4. ;
    }

The translation assigned reserves 100 pointers for the content of `a`.
Obviously, there are situations where this isn't enough, and the number should
be increased. To adjust this number, the suppliment file specifies the number of
elements in the integer `_size`:

    >>> print mc.qpy("function f(); a(1).b = 4.", suggest=True)
    functions = {
      "f" : {
        "a" : "structs",
      },
    }
    structs = {
      "a" : {
        "_size" : 100,
            "b" : "double",
      },
    }
    includes = [
      '#include <armadillo>',
      'using namespace arma ;',
    ]
"""
import matlab2cpp as mc

def set(node, types):

    structs = node.program[3]

    # Structs
    for name in types.keys():

        if name in structs.names:

            types = types[name]
            struct = structs[structs.names.index(name)]

            for key in types.keys():

                if key in struct.names:

                    var = struct[struct.names.index(key)]

                    if var.cls == "Counter":
                        var.value = str(types[key])
                    else:
                        var.type = types[key]

                else:
                    var = mc.collection.Declare(struct, key, backend="struct",
                        type=types[key])


def get(node):

    structs = node.program[3]
    types_s = {}
    for struct in structs:

        types_s[struct["name"]] = types = {}

        for var in struct:

            type = var.prop["type"]
            if type == "TYPE":
                type = ""

            if type == "structs":
                type = var.prop["value"]

            types[var.name] = type

    return types_s


class Stypes(object):

    def __get__(self, instance, owner):
        return get(instance)

    def __set__(self, instance, value):
        set(instance, value)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
