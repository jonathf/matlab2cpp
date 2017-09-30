import matlab2cpp
import matlab2cpp.node as nmodule

def preorder_transform_AST(node, nargin = False, suggest = False):
    # Modify the abstract syntax tree (AST), also try to overload funtions
    # node is project node
    project = node.project
    nodes = nmodule.Node.flatten(project, False, False, False)

    # remove the nodes for clear, close and clc so they are not included in the translation
    nodes = remove_close_clear_clc(nodes)

    # Change right hand side variable to uvec if assigned with find, b = find(a==3)
    if suggest:
        nodes = modify_find(nodes)

    #a multiplication with a complex double results in complex double
    #works with fx_decon_demo.m needs more testing and maybe a refactoring
    if suggest:
        nodes = complex_mul(nodes)

    # remove nargin if args.nargin == False, Thus by default. Use -n flag to keep nargin
    if nargin == False:
        project = remove_nargin(project)

    # add temporary variables for multiple return function
    project = add_parameters(project)

    # change data type from real to complex, if left hand side is real and right hand side is complex in assignment
    if suggest:
        change_to_complex(project)

    return project


def postorder_transform_AST(node):
    project = node.project

    # move the "using namespace arma ;" node last in the includes list
    project = modify_arma_last(project)

    #move #define NOMINMAX to first position
    project = modify_define_first(project)

    return project


# node is project node
def change_to_complex(project):

    # for each program in project
    for idx, program in enumerate(project):
        dictionary = program.ftypes
        new_complex_types = {}
        new_complex_dim = {}

        # for each function (in Funcs) in program
        for func in program[1]:
            func_name = func.name

            # flatten nodes in the function
            nodes = func.flatten(False, False, False)

            #look for assignment
            for n in nodes:
                if n.cls in "Assign" and len(n) == 2:
                    lhs, rhs = n
                    if lhs.mem and lhs.mem != 4 and rhs.mem == 4:
                        lhs.mem = 4

                        # add variable name as key and complex type as type
                        if (lhs.name in new_complex_dim) and (new_complex_dim[lhs.name] < lhs.dim):

                            new_complex_dim[lhs.name] = lhs.dim

                            lhs.type = (lhs.dim, lhs.mem)
                            new_complex_types[lhs.name] = lhs.type

                        else:
                            new_complex_dim[lhs.name] = lhs.dim
                            lhs.type = (lhs.dim, lhs.mem)
                            new_complex_types[lhs.name] = lhs.type

                        dictionary[func_name][lhs.name] = new_complex_types[lhs.name]

        # clear the types in the program
        nodes = program.flatten(False, False, False)
        for idy, node in enumerate(nodes):
            node.type = "TYPE"

        # use dictionary to set ftypes
        program.ftypes = dictionary

    # unset the configured flag
    project.builder.configured = False

    # configure again
    project.builder.configure(True)

    #print(dictionary)


def complex_mul(nodes):
    for node in nodes:
        if node.cls == "Assign":
            lhs, rhs = node

            if rhs.cls == "Mul":
                if rhs[0].type == "cx_double":
                    declares = node.func[0]

                    for var in declares:
                        if var.name == lhs.name:
                            var.type = "cx_double"
    return nodes


# remove the nodes for clear, close and clc so they are not included in the translation
def remove_close_clear_clc(nodes):
    for n in nodes:
        if n.backend == "reserved" and n.name in ("clear", "close", "clc"):
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
                #print(declares.cls)
                for var in declares:
                    if var.name == lhs.name:
                        var.type = "uvec"
    return nodes


# move the "using namespace arma ;" node last in the includes list
def modify_define_first(project):
    for program in project:
        includes = program[0]
        index = 0

        for include in includes:
            if include != includes[0] and include.name[:7] == "#define":
                #print("hello " + include.name)
                define_include = includes.children.pop(index)
                includes.children.insert(0, define_include)

            index += 1

    return project


# move the "using namespace arma ;" node last in the includes list
def modify_arma_last(project):
    for program in project:
        includes = program[0]
        index = 0

        for include in includes:
            if include != includes[-1] and include.name == "using namespace arma ;":
                #includes += [includes.pop(index)] # remove and append arma include node
                using_arma = includes.children.pop(index)
                includes.children.append(using_arma)

            index += 1
    return project


# remove nargin if args.nargin == False, Thus by default. Use -n flag to keep nargin
def remove_nargin(project):
    # node is project
    for program in project:
        # for func in funcs
        funcs = program[1]
        for func in funcs:
            #print(func.summary())
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
                            # print(parent.summary())
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
            #print(n.summary())

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
