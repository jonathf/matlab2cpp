# encoding: utf8

"""
"""

import collection

PREFIX = """# Supplement file
#
# Valid inputs:
#
# uword   int     float   double cx_double
# uvec    ivec    fvec    vec    cx_vec
# urowvec irowvec frowvec rowvec cx_rowvec
# umat    imat    fmat    mat    cx_mat
# ucube   icube   fcube   cube   cx_cube
#
# char    struct  func_lambda
"""


def set_variables(program, types):
    """
    """

    structs = program[1]
    for name in types.keys():

        if name in program.names[2:]:

            types_ = types[name]
            func = program[program.names.index(name)]
            declares, returns, params = func[0], func[1], func[2]

            for key in types_.keys():

                if key in declares.names:
                    var = declares[declares.names.index(key)]
                    var.type = types_[key]

                if key in params.names:
                    var = params[params.names.index(key)]
                    var.type = types_[key]

                elif key in returns.names:
                    var = returns[returns.names.index(key)]
                    var.type = types_[key]

        elif name in structs.names:

            types_ = types[name]
            struct = structs[structs.names.index(name)]

            for key in types_.keys():

                if key in struct.names:
                    var = struct[struct.names.index(key)]
                    var.type = types_[key]

                else:
                    var = collection.Declare(struct, key)
                    var.backend = "struct"
                    var.type = types_[key]


def get_variables(program):
    "Retrieve datatype and suggestions from tokentree"
    types = {}
    suggestions = {}
    for func in program[2:]:

        types[func["name"]] = types_ = {}
        suggestions[func["name"]] = suggestions_ = {}

        declares, params = func[0], func[2]
        for var in declares[:]+params[:]:

            type = var.prop["type"]
            if type == "TYPE":
                type = ""
            types_[var["name"]] = type

            if not type:

                type = var.prop["suggest"]
                if type == "TYPE":
                    type = ""
                if type:
                    suggestions_[var["name"]] = type

    for struct in program[1]:

        types[struct["name"]] = types_ = {}
        suggestions[struct["name"]] = suggestions_ = {}

        for var in struct:

            type = var.prop["type"]
            if type == "TYPE":
                type = ""
            types_[var["name"]] = type

            if not type:

                type = var.prop["suggest"]
                if type == "TYPE":
                    type = ""
                if type:
                    suggestions_[var["name"]] = type

    return types, suggestions



def str_variables(types, suggestions={}, structs={}):

    out = "scope = {}\n\n"

    keys = types.keys()
    keys.sort()

    for name in keys:
        out += '%s = scope["%s"] = {}\n' % (name, name)
        types_ = types[name]

        for key, val in types_.items():

            if key[0] == "_":
                if key[1:5] in ("aux_", "ret_"):
                    continue

            if val:
                out += '%s["%s"] = "%s"\n' % (name, key, val)
            else:
                suggest = suggestions.get(name, {}).get(key, "")
                if suggest:
                    out += '%s["%s"] = "" # %s\n' % (name, key, suggest)
                else:
                    out += '%s["%s"] = ""\n' % (name, key)
        out += "\n"

    return PREFIX + "\n" + out

