
def variable_lists(node):
    nodes = node.flatten(ordered=False, reverse=False, inverse=False)

    #store some variable names, in private or shared
    assigned_var = []
    type_info = []

    #get iterator name
    iterator_name = node[0].name
    for n in nodes:
        if n.cls == "Assign":
            #index = n.parent.children.index(n)
            #lhs var of the assignment
            if n[0].cls == "Var":
                if n[0].name not in assigned_var:
                    assigned_var.append(n[0].name)
                    type_info.append(n[0].type)


            """
            if n[0].cls == "Set":
                var_name = n[0].name

                #subnodes to Set
                #index = n.parent.children.index(n)
                #subnodes = n.parent[index].flatten(ordered=False, reverse=False, inverse=False)
                subnodes = n[0].flatten(ordered=False, reverse=False, inverse=False)

                for subnode in subnodes[1:]:
                    if subnode.name and subnode.name == iterator_name:
                        shared_variable.append(var_name)
                        #print(subnode.name)
            """

        #multiple return from function are assigned to vars
        if n.cls == "Assigns": #and n.backend == "func_returns":
            for sub_node in n:
                if sub_node.cls == "Var":
                    if sub_node.name not in assigned_var:
                        assigned_var.append(sub_node.name)
                        type_info.append(sub_node.type)


        #get the iteration variable in the for loop
        if n.cls == "Var" and n.parent.cls == "For":
            if n.name not in assigned_var:
                assigned_var.append(n.name)
                type_info.append(n.type)

    #shared_variable = list(set(shared_variable))
    #print(shared_variable)

    #for n in nodes:
    #    if (n.cls == "Var" or n.cls == "Get") and n.backend != "reserved" and n.name \
    #            not in [shared_variable, node[0].name]:
    #        private_variable.append(n.name)

    #private_variable = list(set(private_variable))

    #return private_variable, shared_variable, assigned_var, type_info
    return assigned_var, type_info

def omp(node, start, stop, step):
    assigned_var, type_info = variable_lists(node)

    #out = "#pragma omp parallel for\nfor (%(0)s=" + start + \
            #    "; %(0)s<=" + stop + "; %(0)s"

    temp_str = ""
    if len(assigned_var) > 1:
        temp_str = ", ".join(assigned_var[1:])
        temp_str = "firstprivate(" + temp_str + ")"

    out = "#pragma omp parallel for " + temp_str + "\nfor (%(0)s=" + start + \
                "; %(0)s<=" + stop + "; %(0)s"

    return out

def tbb(node, start, stop, step):
    assigned_var, type_info = variable_lists(node)

    any_vec_or_mat = False
    for var, type in zip(assigned_var, type_info):
        if type not in ["uword", "int", "float", "double"]:
            any_vec_or_mat = True

    #tbb.counter += 1
    out = "{\n"

    #str_val = str(tbb.counter)
    if any_vec_or_mat:
        declare_struct = "struct tbb_var_struct" + "\n{"

        for var, type in zip(assigned_var, type_info):
            if type not in ["uword", "int", "float", "double"]:
                declare_struct += "\n" + type + " " + var + ";"

        declare_struct += "\n} " + ";\n"
        declare_struct += "tbb::combinable<struct tbb_var_struct" + "> tbb_per_thread_data" + " ;\n"

        out += declare_struct

    #for var, type in zip(assigned_var, type_info):
    #    out += "tbb::enumerable_thread_specific<" + type + "> " + "_" + var + " = " + var + " ;\n"

    out += "tbb::parallel_for(tbb::blocked_range<size_t>(" + start + ", " + stop + "+1" + \
                  "),\n" + "[&]" + "(const tbb::blocked_range<size_t>& _range) \n{\n"

    #assign to local L, x, y
    for var, type in zip(assigned_var, type_info):
        if type in ["uword", "int", "float", "double"]:
            out += type + " " + var + ";\n"

    if any_vec_or_mat:
        out += "struct tbb_var_struct" + " tbb_struct_vars = tbb_per_thread_data" + ".local() ;\n"

        for var, type in zip(assigned_var, type_info):
            if type not in ["uword", "int", "float", "double"]:
                out += type + "& " + var + " = " + "tbb_struct_vars." + var + ";\n"

    #for var, type in zip(assigned_var, type_info):
    #    out += type + "& " + var + " = _" + var + ".local() ;\n"

    out += "for (" + "%(0)s = _range.begin(); %(0)s != _range.end(); %(0)s"

    # special case for '+= 1'
    if step == "1":
        out += "++"
    else:
        out += "+=" + step

    out += ")\n{\n%(2)s\n}"
    out += "\n}\n);\n"
    out += "}"
    return out

#tbb.counter = 0
