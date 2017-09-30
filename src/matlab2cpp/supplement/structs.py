"""
"""
import matlab2cpp as mc

def set(node, types):

    structs = node.program[3]

    # Structs
    for name in types.keys():

        if name in structs.names:

            types_ = types[name]
            struct = structs[structs.names.index(name)]

            for key in types_.keys():

                if key in struct.names:

                    var = struct[struct.names.index(key)]

                    if var.cls == "Counter":
                        var.value = str(types_[key])
                    else:
                        var.type = types_[key]

                else:
                    var = mc.collection.Declare(struct, key, backend="struct",
                        type=types_[key])


def get(node):

    structs = node.program[3]
    types_s = {}
    for struct in structs:

        types_s[struct.prop["name"]] = types = {}

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
