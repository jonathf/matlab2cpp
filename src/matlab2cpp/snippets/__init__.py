import snippets

def retrieve(node, name, **kws):

    prms, include_code, library_code = snippets.__dict__.get(name)

    params = {}
    params.update(node.prop)
    params.update(prms)
    params.update(kws)
    params["file"] = node.program.name + ".h"

    include_code = include_code % params
    library_code = library_code % params

    return include_code, library_code
