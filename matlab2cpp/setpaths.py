import os
import tree

def multiple_folder_paths(setpath_file):
    builder = tree.builder.Builder()

    folder_paths = []

    if os.path.isfile(setpath_file):
        f = open(setpath_file, "rU")
        code = f.read()
        f.close()
    else:
        return folder_paths

    builder.load("paths_file", code)

    builder.configure()


    #flat ut strukturen på project, se etter string
    code_block = builder.project[0][1][0][3]
    #print ";;;;;;;;;;;;;;;;"
    #print code_block.summary()
    #print ";;;;;;;;;;;;;;;;"

    #nodes = builder.project.flatten(ordered=False, reverse=False, inverse=False)
    #print ";;;;;;;;;;;;;;;;"
    #for node in code_block:
    #    print node.value
    #print ";;;;;;;;;;;;;;;;"

    """
    print "*************"
    print builder.project.summary()
    print "*************"
    """

    #spar assignments variabler av type string
    variables = {}
    folder_paths = []
    rhs_string = ''

    for node in code_block:
        rhs_string = ''
        if node.cls == "Assign":
            subnodes = node[1].flatten(ordered=False, reverse=False, inverse=False)

            str_tmp = ''
            for subnode in subnodes:
                if subnode.cls == "String":
                    str_tmp += subnode.value

                elif subnode.cls == "Var" and subnode.type == "string":
                    str_tmp += variables[subnode.name]

            variables[node[0].name] = str_tmp

        if node.cls == "Statement" and node[0].cls == "Get" and node[0].name in {"path", "setpath"}:
            subnodes = node[0].flatten(ordered=False, reverse=False, inverse=False)

            str_tmp = ''
            for subnode in subnodes:
                if subnode.cls == "String":
                    str_tmp += subnode.value

                if subnode.cls == "Var" and subnode.type == "string":
                    str_tmp += variables[subnode.name]

            folder_paths.append(str_tmp)

    #Ta bort separator om den er på slutten
    folder_paths = [path.rstrip(os.path.sep) for path in folder_paths]
    return folder_paths

