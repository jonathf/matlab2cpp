"""
"""
import matlab2cpp as mc
from . import datatypes, backends, reserved

def configure(root, suggest=True, **kws):
    """
configure backend

See also:
    :py:func:`matlab2cpp.Builder.configure <Builder.configure>`
    """
    if isinstance(root, mc.Builder):
        root = root.project

    loop(root, suggest)
    loop(root, suggest)

def loop(root, suggest):

    nodes = root.flatten(False, True, True)

    while True:
        
        # loop and configure
        for node in nodes:

            # reserved stuff
            if node.cls + "_" + node.name in reserved.__dict__:
                rule = reserved.__dict__[node.cls+"_"+node.name]
                if isinstance(rule, str):
                    node.type = rule
                else:
                    rule(node)

            # Datatype stuff
            if node.prop["type"] != "TYPE":
                pass

            elif node.cls in datatypes.__dict__:
                datatype = datatypes.__dict__[node.cls]
                if isinstance(datatype, str):
                    node.type = datatype
                else:
                    datatype(node)

            # Backend stuff
            if node.backend != "unknown":
                pass

            elif node.cls in backends.__dict__:
                backend = backends.__dict__[node.cls]
                if isinstance(backend, str):
                    node.backend = backend
                else:
                    backend(node)

        # determine if done
        if suggest:

            complete = True

            for program in root.project:
                
                suggests = program.suggest
                program.stypes = suggests
                program.ftypes = suggests
                complete = complete and not any([any(v) for v in suggests.values()])

            if complete:
                break

        else:
            break

    # delete log, if any (create on translate)
    for program in root.project:
        program[-1].children = []
