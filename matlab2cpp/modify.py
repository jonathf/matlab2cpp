import matlab2cpp
import matlab2cpp.node as nmodule

def transform_AST(node, nargin = False):
    # Modify the abstract syntax tree (AST), also try to overload funtions
    # node is project node
    project = node.project
    nodes = nmodule.Node.flatten(project, False, False, False)

    # remove the nodes for clear, close and clc so they are not included in the translation
    nodes = remove_close_clear_clc(nodes)

    # Change right hand side variable to uvec if assigned with find, b = find(a==3)
    nodes = modify_find(nodes)

    # move the "using namespace arma ;" node last in the includes list
    project = modify_arma_last(project)

    # remove nargin if args.nargin == False, Thus by default. Use -n flag to keep nargin
    if nargin == False:
        project = remove_nargin(project)

    # add temporary variables for multiple return function
    project = add_parameters(project)

    return project


# remove the nodes for clear, close and clc so they are not included in the translation
def remove_close_clear_clc(nodes):
    for n in nodes:
        if n.name in ("clear", "close", "clc"):
            index = n.parent.parent.children.index(n.parent)
            del n.parent.parent.children[index]
    return nodes


# Change right hand side variable to uvec if assigned with find, b = find(a==3)
def modify_find(nodes):
    for n in nodes:
        if n.cls == "Assign":
            lhs, rhs = n
            if rhs.name == "find":
                declares = n.func[0]
                #print declares.cls
                for var in declares:
                    if var.name == lhs.name:
                        var.type = "uvec"
    return nodes


# move the "using namespace arma ;" node last in the includes list
def modify_arma_last(project):
    for program in project:
        includes = program[0]
        index = 0

        for include in includes:
            if include != includes[-1] and \
              include.name == "using namespace arma ;":
                includes += [includes.pop(index)] # remove and append arma include node

            index += 1
    return project


# remove nargin if args.nargin == False, Thus by default. Use -n flag to keep nargin
def remove_nargin(project):
    # node is project
    for program in project:
        # for func in funcs
        funcs = program[1]
        for func in funcs:
            block = func[3]

            # find node.name == nargin
            found_nargin = True
            while found_nargin:
                found_nargin = False
                nodes = nmodule.Node.flatten(block, False, False, False)

                # remove if node.group is branch
                for n in nodes:
                    if n.name == "nargin":
                        # remove branch
                        if n.group.cls in ("Branch", "Switch"):
                            parent = n.group.parent
                            # print parent.summary()
                            del parent.children[parent.children.index(n.group)]
                            # node.group.parent.children.index(node.group)
                            found_nargin = True
                            break
                        else: # node.group is not a branch
                            found_nargin = False
                            break
    return project


# add temporary variables for multiple return function
def add_parameters(project):
    nodes = nmodule.Node.flatten(project, False, False, False)
    for n in nodes:
        if n.cls == "Get" and n.backend == "func_returns":
            func_name = n.name

            func_ret_num = 0
            if n.parent.cls in ("Assign", "Assigns"):

                for sub_node in n.parent:
                    if sub_node.cls != "Get":
                        func_ret_num += 1
                    else:
                        break
            #print n.summary()

            # find the multiple return function
            # Check if function is in the same program

            # Look first for function in current file
            funcs = n.program[1]
            found_func = False
            func = []
            for f in funcs:
                if f.name == n.name:
                    func_found = True
                    #programs = n.program
                    func = f

            # Look for function in external file
            if found_func == False:
                for program in n.project:
                    f = program[1][0]
                    if f.name == n.name:
                        func = f
                        break
                #programs  = [p[1][0] for p in project if p[1][0]= n.program]


            # add needed temporary variables to params
            if func:
                return_params = func[1]
                # dictionary which is used as a counter
                type_counter = {"int" : 0, "float" : 0, "double" : 0, "uword" : 0, "cx_double" : 0,
                "ivec" : 0, "fvec" : 0, "uvec" : 0, "vec" : 0, "cx_vec" : 0,
                "irowvec" : 0, "frowvec" : 0, "urowvec" : 0, "rowvec" : 0, "cx_rowvec" : 0,
                "imat" : 0, "fmat" : 0, "umat" : 0, "mat" : 0, "cx_mat" : 0,
                "icube" : 0, "fcube" : 0, "ucube" : 0, "cube" : 0, "cx_cube" : 0}

                # add or reuse variables, also add change
                while func_ret_num < len(return_params):
                    if return_params[func_ret_num].type not in ("TYPE", "string"):
                        type_counter[return_params[func_ret_num].type] += 1
                        name = "_tmp_" + return_params[func_ret_num].type + \
                               str(type_counter[return_params[func_ret_num].type])

                        # Allocate Var node. n.parent is the assign node
                        swap_var = matlab2cpp.collection.Var(n.parent, name)
                        swap_var.type = return_params[func_ret_num].type
                        swap_var.backend = return_params[func_ret_num].backend
                        swap_var.create_declare()

                        # swap Var and Get (function_returns)
                        n.parent.children[func_ret_num] = swap_var
                        n.parent.children[-1] = n

                    #index += 1
                    func_ret_num += 1
    return project
