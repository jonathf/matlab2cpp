import collection
import datatype as dt
import targets
import snippets
import utils

indexnames = [
    "Assign", "Assigns", "Branch", "For", "Func", "Set", "Set2",
    "Set3", "Sets", "Statement", "Switch", "Tryblock", "While",
    "Program", "Block", "Get", "Get2", "Get3",
]




class Node(object):
    """
General definition of a token representation of code
    """

    dim = dt.Dim()
    mem = dt.Mem()
    num = dt.Num()
    type = dt.Type()

    def __init__(self, parent, name=None):
        """
Parameters
----------
parent : Node
    Node parent in the token tree
name : str
    Optional name of the node
        """
        init(self, parent, name)

    def summary(self, disp=False, group=None):
        "Node summary"

        nodes = utils.flatten(self, False, False, False)
        if disp:
            print "iterating %d nodes" % len(nodes)

        indent = [self]
        out = ""
        for node in nodes:

            index = node["index"]
            name = node["name"]
            cls = node["class"]
            backend = node["backend"]
            type = node.type

            if backend == "unknown" and type != "TYPE":
                backend = type

            while indent and not (node.parent is indent[-1]):
                indent.pop()

            indices = [n["index"] for n in node.children]+[index]
            if (group is None) or group in indices:

                space = " "*(len(indent)-1)
                out += "%3d%s%18s %-10s %-12s %-7s" % \
                        (index, space, name, cls, backend, type)
                out += str(node["ret"]) + "\n"

            indent.append(node)

        return out


    def generate(self, disp, group=None):
        """Generate code"""

        nodes = utils.flatten(self, False, True, False)
        if disp:
            print "iterating %d nodes" % len(nodes)

        for node in nodes[::-1]:

            type_ = node.type
            name = node["name"]
            cls = node["class"]
            backend = node["backend"]

            if disp:
                print name, cls, type_, backend

            if type_ == "TYPE" and node.children and \
                    cls not in ("Get", "Get2", "Get3", 
                            "Set", "Set2", "Set3"):
                node.type = [n.type for n in node]
                type_ = node.type

            if name in targets.reserved.reserved:
                backend = "reserved"
            elif backend == "unknown" and type_ != "TYPE":
                backend = type_

            target = targets.__dict__[backend]
            if cls+"_"+name in target.__dict__:
                value = target.__dict__[cls+"_"+name]
            elif cls in target.__dict__:
                value = target.__dict__[cls]
            else:
                print node.program.summary(disp, group)
                raise KeyError("no %s in %s" % (cls, backend))

            if not isinstance(value, (unicode, str, list, tuple)):
                value = value(node)

            if isinstance(value, unicode):
                value = str(value)

            elif isinstance(value, Node):
                value = str(value)

            elif value is None:
                raise ValueError("missing return in %s.%s" % (backend, cls))

            node["ret"] = repr(value)

            prop = node.prop.copy()
            I = len(node)
            for i in xrange(I):
                prop["%d" % i] = prop["-%d" % (I-i)] = node[i]["str"]
            prop["type"] = node.type

            if not isinstance(value, str):

                value = list(value)
                children = ["%("+str(i)+")s" for i in xrange(len(node))]

                if len(value) == 2:
                    value.insert(1, "")

                value = value[:-1] + [value[-2]] *\
                    (len(children)-len(value)+1) + value[-1:]

                if len(children) == 0:
                    value = value[0] + value[-1]

                elif len(children) == 1:
                    value = value[0] + children[0] + value[-1]

                else:

                    out = value[0]
                    for i in xrange(len(children)):
                        out += children[i] + value[i+1]
                    value = out

            try:
                value = value % prop
            except:
                raise SyntaxError("interpolation in " + backend + "." + cls +
                                " is misbehaving\n" + value + "\n"+str(prop))

            node.prop["str"] = value

        if group:
            for node in nodes:
                if node["index"] == group:
                    return node.parent["str"]

        return self.prop["str"]


    def configure(self, suggestion=False, disp=False):

        nodes = utils.flatten(self, False, True, False)
        if disp:
            print "iterating %d nodes" % len(nodes)

        while True:

            for node in nodes[::-1]:

                name = node["name"]
                cls = node["class"]
                type = node.type

                # Assign some hereditary types
                if type == "TYPE" and node.children and cls not in\
                        ("Set", "Set2", "Set3", "Get", "Get2", "Get3"):
                    node.type = [n.type for n in node]

                if cls in ("Div", "Eldiv", "Rdiv", "Elrdiv"):
                    if node.num and node.mem < 2:
                        node.mem = 2

                backend = node["backend"]

                if backend != "unknown":
                    pass

                elif name in targets.reserved.reserved:
                    node["backend"] = "reserved"


                if backend in "unknown" and type != "TYPE":
                    node["backend"] = type

                # Assign suggestion
                if not suggestion or type != "TYPE":
                    pass

                elif cls == "Assign":
                    node[0].suggest(node[1].type)

                elif cls == "For":
                    var, range = node[:2]
                    var.suggest("int")

                elif cls in ("Var", "Get", "Get2", "Get3",
                        "Assigns", "Vector", "Matrix", "Colon"):

                    if backend == "func_return":
                        names = node.program["names"]
                        func = node.program[names.index(name)]
                        ret_val = func[1][0]
                        node.set_global_type(ret_val.type)
                        params = func[2]
                        for i in xrange(len(node)):
                            params[i].suggest(node[i].type)

                    if backend == "func_returns":
                        names = node.program["names"]
                        func = node.program[names.index(name)]
                        returns = func[1]
                        params = func[2]
                        for i in xrange(len(returns)):
                            returns[i].suggest(node[i].type)
                        for j in xrange(len(params)):
                            params[j].suggest(node[i+j+1].type)

                    if backend == "func_lambda":
                        names = node.program["names"]
                        func = node.program[names.index(name)]
                        ret_val = func[1][0]
                        node.set_global_type(ret_val.type)
                        params = func[2]
                        for i in xrange(len(node)):
                            params[i].suggest(node[i].type)

                    else:
                        node.generate(False, None)

                elif cls == "Neg" and node[0].mem == 0:
                    node.mem = 1

            if suggestion:
                cfg, scfg = utils.get_cfg(self)
                if not [c for c in scfg.values() if any(c)]:
                    return
                else:
                    utils.set_cfg(self, scfg)

            else:
                return



    def declare(self, name=""):
        "Declare a variable in the begining of a function."

        if hasattr(self, "reference"):
            return

        name = name or self["name"]
        if name in targets.reserved.reserved:
            return

        func = self.func
        declares = func[0]
        params = func[2]
        if name in params["names"]:
            self.reference = params[params["names"].index(name)]
            return

        if name in declares["names"]:
            node = declares[declares["names"].index(name)]
            type = self.type
            if type != "TYPE":
                node.type = type
            self.reference = node
            return

        node = collection.Declare(declares, name)
        type = self.type
        node.type = type
        node["suggest"] = type
        self.reference = node

    def set_global_type(self, text):

        self.type = text

        if self["class"] == "Func":
            func = self
        elif self["class"] in ("Program", "Include", "Includes"):
            return
        else:
            func = self.func

        declares = func[0]
        params = func[2]
        name = self["name"]

        for declare in declares:
            if declare["name"] == name:
                node = declare
                break
        else:
            for param in params:
                if param["name"] == name:
                    node = param
                    break
            else:
                return

        node.type = text


    def suggest(self, text):

        if text == "TYPE" or self.type != "TYPE":
            return

        if self["class"] == "Func":
            func = self
        elif self["class"] in ("Program", "Include", "Includes"):
            return
        else:
            func = self.func

        declares = func[0]
        params = func[2]
        name = self["name"]

        for declare in declares:
            if declare["name"] == name:
                node = declare
                break
        else:
            for param in params:
                if param["name"] == name:
                    node = param
                    break
            else:
                return

        if isinstance(text, str):
            text = [text]
        text = list(text)
        node["suggest"] = dt.common_loose(text + [node["suggest"]])


    def auxillary(self, type="", convert=False):
        """create a auxillary variablele and 
        move actual calcuations to own line."""

        assert self.parent["class"] != "Assign",\
                ".auxillary() must be triggered mid expression."

        if not type:
            type = self.type

        if not isinstance(type, str):
            type = dt.common_strict(type)

        if self["class"] in ("Vector", "Matrix"):
            backend = "matrix"
        elif type == "TYPE":
            backend = "unknown"
        else:
            backend = type

        line = self
        while line.parent["class"] != "Block":
            line = line.parent
        block = line.parent

        # Create new var
        var = "_aux_" + type + "_"
        if not line[var]:
            line.prop[var] = 1
        else:
            line.prop[var] += 1
        var = var + str(line[var])

        # Create Assign
        s = collection.Assign(block)
        s["backend"] = backend
        s.set_global_type(type)

        # Return value
        v0 = collection.Var(s, var)
        v0.set_global_type(type)
        v0["backend"] = backend
        v0.declare()

        # Create aux Var
        if convert:
            get = collection.Get(s, "conv_to")
            get.set_global_type(type)
            v1 = collection.Var(get, var)
        else:
            v1 = collection.Var(s, var)

        v1.set_global_type(type)
        v1["backend"] = backend

        # Place Assign correctly in Block
        i = block.children.index(line)
        block.children = block[:i] + block[-1:] + block[i:-1]

        # Swap self and Var
        index = self.parent.children.index(self)
        self.parent.children[index] = v1

        v1.group, self.group = self.group, v1.group
        v1.parent, self.parent = self.parent, v1.parent

        if convert:
            get.children[-1] = self
        else:
            s.children[-1] = self

        return v1


    def include(self, name, **kws):

        includes = self.program[0]
        idname, code = snippets.retrieve(self, name, **kws)

        if idname in includes["names"]:
            return idname

        for val in kws.values():
            if val == "TYPE":
                return "FUNC"

        includes["names"].append(idname)
        include = collection.Include(includes, idname)
        include["value"] = code
        include["backend"] = "program"
        return idname


    def pointer(self, num=None):
        if num is None:
            num = self.prop["pointer"]
        else:
            num = int(num)
            self.prop["pointer"] = num

        if num>0:
            return num*"*"
        elif num<0:
            return (-num)*"&"
        return ""

    def error(self, text):
        self.program.errors.add(text)


    def __getitem__(self, i):
        if isinstance(i, str):
            out = self.prop.get(i, "")
            return out
        return self.children[i]

    def __setitem__(self, key, val):
        self.prop[key] = val

    def __hasitem__(self, key):
        return key in self.prop

    def __len__(self):
        return len(self.children)

    def __str__(self):
        return self.prop["str"]

    def __add__(self, val):
        return str(self)+str(val)

    def __radd__(self, val):
        return str(val)+str(val)

    def __iter__(self):
        return self.children.__iter__()

    def append(self, node):
        node.children.append(node)
        node.prop["names"].append(node["name"])

    def pop(self, index):
        self.prop["names"].pop(index)
        return self.children.pop(index)



def init(node, parent, name=""):

    node.children = []      # node children
    node.prop = {}          # node property

    # Parental relationship
    node.parent = parent
    node.program = parent.program
    if name != "program":
        parent.children.append(node)
        parent["names"].append(name)

    cls = node.__class__.__name__
    node.prop["class"] = cls

    if cls in indexnames:
        index = node["index"] = 0
        node.group = node

    elif parent["index"] != 0:
        node["index"] = parent["index"]
        node.group = parent.group

    else:
        index = node.program["index"] + 1
        node["index"] = index
        node.program["index"] = index
        node.group = parent.group

    if name:
        node["name"] = name
    else:
        node["name"] = ""


    if parent.prop["class"] in ("Program", "Func"):
        node.func = parent
    else:
        node.func = parent.func

    node["backend"] = "unknown"
    node["str"] = ""
    node["value"] = ""
    node["pointer"] = 0
    node["names"] = []

    node["suggest"] = "TYPE"
    node["type"] = "TYPE"

