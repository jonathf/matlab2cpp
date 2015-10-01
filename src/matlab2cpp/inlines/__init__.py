import snippets
import os

def retrieve(node, name, **kws):

    if os.path.isfile(name):

        name = os.path.relpath(name, os.path.dirname(node.program.name))
        include_code = '#include "%s.hpp"' % name
        library_code = ""

        if node.name == name:
            include_code = ""

    else:

        prms, include_code, library_code = snippets.__dict__.get(name)

        params = {}
        params.update(node.properties())
        params.update(prms)
        params.update(kws)

        include_code = include_code % params
        library_code = library_code % params

    if node.file in include_code:
        include_code = include_code.replace(node.file, os.path.basename(node.file))

    return include_code, library_code
