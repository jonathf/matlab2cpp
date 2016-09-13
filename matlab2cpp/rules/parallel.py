
def variable_lists(node):
    nodes = node.flatten(ordered=False, reverse=False, inverse=False)

    #store some variable names, in private or shared
    private_variable = []
    shared_variable = []
    assigned_var = []
    type_info = []

    #get iterator name
    iterator_name = node[0].name
    for n in nodes:
        if n.cls == "Assign":
            index = n.parent.children.index(n)

            if n[0].cls == "Var":
                assigned_var.append(n[0].name)
                type_info.append(n[0].type)

            if n[0].cls == "Set":
                var_name = n[0].name

                #subnodes to Set
                #index = n.parent.children.index(n)
                #subnodes = n.parent[index].flatten(ordered=False, reverse=False, inverse=False)
                subnodes = n[0].flatten(ordered=False, reverse=False, inverse=False)

                for subnode in subnodes[1:]:
                    if subnode.name and subnode.name == iterator_name:
                        shared_variable.append(var_name)
                        #print subnode.name

    shared_variable = list(set(shared_variable))
    #print shared_variable

    for n in nodes:
        if (n.cls == "Var" or n.cls == "Get") and n.backend != "reserved" and n.name not in shared_variable:
            private_variable.append(n.name)

    private_variable = list(set(private_variable))
    #print private_variable

    #combine shared and private variable to tbb [ , , , , ] with & before shared
    my_string = ''

    for var in private_variable:
        my_string += var + ", "

    for var in shared_variable:
        my_string += "&" + var + ", "

    my_string = my_string.rstrip(", ")
    my_string = "[" + my_string + "]"
    #print my_string
    #print "assigned var:\n"
    #print assigned_var

    return private_variable, shared_variable, assigned_var, type_info

def tbb(node, start, stop, step):
    private_variable, shared_variable, assigned_var, type_info = variable_lists(node)

    #print "----type_info------"
    #print type_info

    out = "{\n"

    temp_list = []
    temp_assigned_var = set(assigned_var)

    for var in private_variable:
        if var in temp_assigned_var:
            temp_list.append("&_" + var)
        else:
            temp_list.append("&" + var)

    for var in shared_variable:
        temp_list.append("&" + var)

    temp_str = ", ".join(temp_list)
    temp_str = "[" + temp_str + "]"

    for var, type in zip(assigned_var, type_info):
        out += "tbb::enumerable_thread_specific<" + type + "> " + "_" + var + " = " + var + " ;\n"

    out += "\ntbb::parallel_for(tbb::blocked_range<size_t>(" + start + ", " + stop + "+1" + \
                  "),\n" + temp_str + "(const tbb::blocked_range<size_t>& _range) \n{\n"

    #assign to local L, x, y
    for var, type in zip(assigned_var, type_info):
        out += type + "& " + var + " = _" + var + ".local() ;\n"

    out += "\nfor (" + node[0].type + " %(0)s = _range.begin(); %(0)s != _range.end(); %(0)s"

    # special case for '+= 1'
    if step == "1":
        out += "++"
    else:
        out += "+=" + step

    out += ")\n{\n%(2)s\n}"
    out += "\n}\n);\n"
    out += "}\n"
    return out