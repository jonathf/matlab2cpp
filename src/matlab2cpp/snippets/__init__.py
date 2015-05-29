import snippets

def retrieve(node, name, **kws):

    prms, include_code, library_code = snippets.__dict__.get(name)
    prms.update(kws)
    include_code = include_code % prms
    library_code = library_code % prms

    keys = prms.keys()
    keys.sort()
    vals = [prms[key] for key in keys]
    key = name+"_"+"_".join(vals)

    return key, include_code, library_code
