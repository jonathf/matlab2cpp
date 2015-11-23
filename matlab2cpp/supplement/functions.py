"""
"""

import matlab2cpp as mc

def set(node, types):

    funcs = node.program[1]    

    # Functions
    for name in types.keys():

        if name in funcs.names:

            types_ = types[name]
            func = funcs[funcs.names.index(name)]
            declares, returns, params = func[:3]

            for key in types_.keys():

                if key in declares.names:

                    if key in returns.names:
                        var = returns[returns.names.index(key)]
                        var.type = types_[key]

                    var = declares[declares.names.index(key)]
                    var.type = types_[key]

                elif key in params.names:
                    var = params[params.names.index(key)]
                    var.type = types_[key]

def get(node):

    funcs = node.program[1]

    types = {}

    for func in funcs:

        types[func.name] = types_ = {}

        declares, params = func[0], func[2]
        for var in declares[:]+params[:]:

            type = var.type
            if type == "TYPE":
                type = ""
            types_[var.name] = type

            if not type:

                type = var.prop["suggest"]
                if type == "TYPE":
                    type = ""

    return types


class Ftypes(object):
    "Access to function types from program node"
    def __get__(self, instance, owner):
        return get(instance)
    def __set__(self, instance, value):
        set(instance, value)



if __name__ == "__main__":
    import doctest
    doctest.testmod()
