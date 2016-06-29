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
            try:
                params[i].suggest = node[i].type
                node[i].suggest = params[i].type
            except:
                pass

    elif node.backend == "func_returns":
        node.backend = func.backend
        params = func[2]

        for j in xrange(len(params)):
            try:
                params[j].suggest = node[j].type
                node[j].suggest = params[j].type
            except:
                pass

        if node.parent.cls == "Assigns":
            # node.parent.backend = "func_returns"

            returns = func[1]
            # Got out_of_bounds error, len(returns) where longer than LHS,
            # so i changed for range to min LHS vars and returns from function
            for j in xrange(min(len(node.parent), len(returns))):
                returns[j].suggest = node.parent[j].type
                node.parent[j].suggest = returns[j].type

    elif node.backend == "func_lambda":

        ret = func[1][0]
        node.suggest = ret.type
        ret.suggest = node.type
        if node.type != "TYPE":
            node.declare.type = "func_lambda"

        params = func[2]
        for i in xrange(len(node)):
            params[i].suggest = node[i].type

    return True
        
