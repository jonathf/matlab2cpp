import os
from . import tree

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

    #Get code_block
    code_block = builder.project[0][1][0][3]

    #save variables that are assigned of type string
    variables = {}
    folder_paths = []

    #each node in code_block is basically one line of code
    for node in code_block:
        #Assignments node
        if node.cls == "Assign":
            subnodes = node[1].flatten(ordered=False, reverse=False, inverse=False)

            str_tmp = ''
            for subnode in subnodes:
                if subnode.cls == "String":
                    str_tmp += subnode.value

                elif subnode.cls == "Var" and subnode.type == "string":
                    str_tmp += variables[subnode.name]

            variables[node[0].name] = str_tmp

        #Statement node
        if node.cls == "Statement" and node[0].cls == "Get" and node[0].name in {"path", "addpath"}:
            subnodes = node[0].flatten(ordered=False, reverse=False, inverse=False)

            str_tmp = ''
            for subnode in subnodes:
                if subnode.cls == "String":
                    str_tmp += subnode.value

                if subnode.cls == "Var" and subnode.type == "string":
                    str_tmp += variables[subnode.name]

            folder_paths.append(str_tmp)

    #remove separator if it is at the end of the string
    folder_paths = [path.rstrip(os.path.sep) for path in folder_paths]
    return folder_paths

