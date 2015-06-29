import snippets
import os

def retrieve(node, name, **kws):

    prms, include_code, library_code = snippets.__dict__.get(name)

    params = {}
    params.update(node.prop)
    params.update(prms)
    params.update(kws)
    params["file"] = os.path.basename(node.program.name)

    include_code = include_code % params
    library_code = library_code % params

    return include_code, library_code
