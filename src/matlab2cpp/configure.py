import os

import supplement


def configure(self, suggest=True, **kws):

    nodes = self.project.flatten(False, True, False)
    while True:

        for node in nodes[::-1]:

            if node.cls in ("Get", "Var"):

                if node.type == "func_lambda":
                    node.backend = "func_lambda"

                    if not (node.parent.cls in \
                            ("Declares", "Returns", "Params")) and\
                            hasattr(node.parent[-1].declare, "reference"):

                        if node.parent.cls == "Assign":
                            node.declare.reference = \
                                    node.parent[-1].declare.reference
                        node.reference = node.declare.reference

                # lambda scope
                if node.backend == "func_lambda":
                    if hasattr(node, "reference"):
                        func = node.reference
                    else:
                        func = None

                # local scope
                elif node in node.program[1]:
                    func = node.program[1][node]
                    node.backend = func.backend

                # external file in same folder
                else:

                    for program in self.project:

                        if os.path.isfile(program.name) and \
                                os.path.basename(program.name) == node.name+".m":
                            func = program[1][0]
                            # self.project[self.project.names.index(
                                # node.name+".m")][1][0]
                            node.backend = func.backend
                            break
                    else:
                        func = None
                        node.translate(only=True)

                if not (func is None):
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
                            node.parent.backend = "func_returns"

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

                        params = func[2]
                        for i in xrange(len(node)):
                            params[i].suggest = node[i].type

            elif node.cls in ("Fvar", "Cget", "Fget", "Nget", "Colon"):
                node.translate(only=True)

            elif node.cls == "Vector":

                if node and node[0].backend == "struct":
                    declare = node.func[0][
                            node.func[0].names.index(node[0].name)]
                    if declare.backend == "structs":
                        node.backend = "structs"

                node.type = [n.type for n in node]
                node.translate(only=True)

            elif node.cls == "Matrix":

                if node[0] and node[0][0].backend == "struct":
                    declare = node.func[0][
                            node.func[0].names.index(node[0][0].name)]
                    if declare.backend == "structs":
                        node.backend = "structs"

                node.type = [n.type for n in node]
                node.translate(only=True)

            if node.type == "TYPE":

                if node.cls not in\
                        ("Set", "Cset", "Fset", "Nset", "Sset",
                        "Get", "Cget", "Fget", "Nget", "Sget",
                        "Assign", "Assigns"):
                    node.type = [n.type for n in node]

                if node.cls in ("Div", "Eldiv", "Rdiv", "Elrdiv"):
                    if node.num and node.mem < 2:
                        node.mem = 2

                elif node.cls == "Fvar":
                    node.declare.type = node.type

            elif node.backend == "unknown":
                node.backend = node.type

            # Assign suggestion
            if node.cls == "For":
                var, range = node[:2]
                var.suggest = "int"

            elif node.cls == "Assign" and node[0].cls != "Set":
                node[0].suggest = node[1].type


            elif node.cls == "Neg" and node[0].mem == 0:
                node.mem = 1

        if suggest:

            complete = True
            for program in self.project:
                types_f, types_s, types_i, suggests =\
                        supplement.get_variables(program)

                for s in suggests:

                    if not suggests[s]:
                        continue

                    if s in types_f:
                        types_f[s].update(suggests[s])
                    elif s in types_s:
                        types_s[s].update(suggests[s])

                    complete = False

                supplement.set_variables(program, types_f, types_s)

            if complete:
                break

            if suggest == 1:
                suggest = 0

        else:
            break

