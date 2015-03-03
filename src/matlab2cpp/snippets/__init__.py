import snippets


def retrieve(node, name, **kws):

    prms, code = snippets.__dict__.get(name)
    prms.update(kws)
    code = code % prms

    keys = prms.keys()
    keys.sort()
    vals = [prms[key] for key in keys]
    key = name+":"+":".join(vals)

    return key, code
