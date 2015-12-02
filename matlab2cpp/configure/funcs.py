import os

def funcs(node):

    func = None

    # lambda scope
    if "_" + node.name in node.program[1]:
        func = node.program[1]["_" + node.name]
    
    # local scope
    elif node in node.program[1]:
        func = node.program[1][node]

    # external file in same folder
    else:

        for program in node.project:

            # don't use the file your in as external library
            if program is node.program:
                continue

            if os.path.basename(program.name) == node.name+".m":
                func = program[1][0]
                break
        else:
            return False

    node.backend = func.backend

    if node.backend == "func_return":

        node.backend = func.backend
        node.declare.type = func[1][0].type
        params = func[2]

        for i in xrange(len(node)):
            params[i].suggest = node[i].type
            node[i].suggest = params[i].type

    elif node.backend == "func_returns":
        node.backend = func.backend
        params = func[2]

        for j in xrange(len(params)):
            params[j].suggest = node[j].type
            node[j].suggest = params[j].type

        if node.parent.cls == "Assigns":
            # node.parent.backend = "func_returns"

            returns = func[1]
            for j in xrange(len(returns)):
                returns[j].suggest = node.parent[j].type
                node.parent[j].suggest = returns[j].type

    elif node.backend == "func_lambda":

        ret = func[1][0]
        if ret.type != "TYPE" and node.type == "TYPE":
            node.type = ret.type
        elif ret.type == "TYPE" and node.type != "TYPE":
            ret.type = node.type
        node.declare.type = "func_lambda"

        params = func[2]
        for i in xrange(len(node)):
            params[i].suggest = node[i].type

    return True
        
