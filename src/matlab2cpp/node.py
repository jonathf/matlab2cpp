import collection
from datatype import datatype
import targets
import snippets
import utils

indexnames = [
    "Assign", "Assigns", "Branch", "For", "Func", "Set", "Set2", "Set3",
    "Statement", "Switch", "Tryblock", "While", "Program", "Block"
]

class Node(object):
    """
General definition of a token representation of code
    """

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

        nodes = utils.flatten(self, ordered=True)
        if disp:
            print "iterating %d nodes" % len(nodes)

        indent = [self]
        out = ""
        for node in nodes:

            index = node["index"]
            name = node["name"]
            cls = node["class"]
            backend = node["backend"]
            type = node.type()

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

        nodes = utils.flatten(self)
        if disp:
            print "iterating %d nodes" % len(nodes)

        for node in nodes[::-1]:

            type_ = node.type()
            name = node["name"]
            cls = node["class"]
            backend = node["backend"]

            if disp:
                print name, cls, type_, backend

            if type_ == "TYPE" and node.children and \
                    cls not in ("Get", "Get2", "Get3", 
                            "Set", "Set2", "Set3"):
                type_ = node.type([n.type() for n in node.children])

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
                raise ValueError("missing return in %s.%s" % backend, cls)

            node["ret"] = repr(value)

            prop = node.prop.copy()
            I = len(node)
            for i in xrange(I):
                prop["%d" % i] = prop["-%d" % (I-i)] = node[i]["str"]

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


    def declare(self, name=""):
        "Declare a variable in the begining of a function."

        func = self.func
        name = name or self["name"]
        declares = func[0]
        params = func[2]
        if name in params["names"]:
            return

        if name in declares["names"]:
            node = declares[declares["names"].index(name)]
            type = self.type()
            if type != "TYPE":
                node.type(type)
            return

        node = collection.Declare(declares, name)
        declares["names"].append(name)
        type = self.type()
        node.type(type)
        node["suggest"] = datatype(type)

    def type(self, text=""):
        "Get/Set datatype"

        if not isinstance(text, str):
            text = map(datatype, text)
            text = str(sum(text))

        if self["class"] == "Func":
            func = self
        elif self["class"] in ("Program", "Include", "Includes"):
            return "TYPE"
        else:
            func = self.func

        declares = func[0]
        params = func[2]
        name = self["name"]

        if text:
            if name in declares["names"]:
                node = declares[declares["names"].index(name)]
                node.suggest(text)

            elif name in params["names"]:
                node = params[params["names"].index(name)]

                node.suggest(text)
            self["type"] = datatype(text)

        else:
            if name in declares["names"]:
                node = declares[declares["names"].index(name)]
                type = str(node["type"])
                if type != "TYPE":
                    return type

            elif name in params["names"]:
                node = params[params["names"].index(name)]
                type = str(node["type"])
                if type != "TYPE":
                    return type

        return str(self["type"])

    def suggest(self, text=""):

        if not isinstance(text, str):
            text = str(reduce(lambda x, y: datatype(x)*datatype(y)), text)

        if text == "TYPE":
            return "TYPE"

        if self["class"] == "Func":
            func = self
        elif self["class"] in ("Program", "Include", "Includes"):
            return "TYPE"
        else:
            func = self.func

        declares = func[0]
        params = func[2]
        name = self["name"]

        if name in declares["names"]:
            node = declares[declares["names"].index(name)]
        elif name in params["names"]:
            node = params[params["names"].index(name)]
        else:
            if not text:
                return self.type()
            return text

        if text:

            if str(node["suggest"]) in ("", "TYPE"):
                node["suggest"] = datatype(text)
            else:
                node["suggest"] = datatype(text) * node["suggest"]

        return str(node["suggest"])

    def propose(self):

        types = [n.prop["type"] for n in self]
        return reduce(lambda x, y: x*y, types).val


    def replace(self, node, *args):
        "replace node in token tree"

        print node["class"], node["name"], "being replaced"
        if not args:

            index1 = self.parent.children.index(self)
            index2 = node.parent.children.index(node)
            self.parent.children[index1] = node
            node.parent.children[index2] = self
            node.parent, self.parent = self.parent, node.parent
#              node._generate()
            return str(node)

        else:

            assert node in targets.__dict__
            matrix = collection.Matrix(self.parent)
            matrix["backend"] = "matrix"
            vector = collection.Vector(matrix)
            vector["backend"] = "matrix"

            for arg in args:
                v = collection.Var(vector, arg)
                v.type(node)
                v["backend"] = node
            self.replace(matrix)
            if self.parent["class"] != "Assign" and len(args) > 1:
                return self.auxillary(node)
            return self


    def auxillary(self, type=""):
        """create a auxillary variable and 
        move actual calcuations to own line."""

        assert self.parent["class"] != "Assign",\
                ".auxillary() must be triggered mid expression."

        if not type:
            type = self.type()

        if self["class"] in ("Vector", "Matrix"):
            backend = "matrix"
        elif type == "TYPE":
            backend = "unknown"
        else:
            backend = type

        line = self
        while line.parent["class"] != "Block":
            line = line.parent
        p = line.parent

        # Create new var
        var = "_aux_" + type

        # Create Assign
        s = collection.Assign(p)
        s["backend"] = backend
        s.type(type)

        # Return value
        v0 = collection.Var(s, var)
        v0.declare()
        v0.type(type)

        # Create aux Var
        v1 = collection.Var(s, var)
        v1.type(type)

        # Place Assign correctly in Block
        i = p.children.index(line)
        p.children = p[:i] + p[-1:] + p[i:-1]

        # Swap self and Var
        index = self.parent.children.index(self)
        self.parent.children[index] = v1
        v1.group = self.group
        self.group = s
        v1.parent = self.parent
        self.parent = s
        s.children[1] = self

        # Generate code for new variables
#          s._generate()
#          v1._generate()

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


    def error(self, text):
        self.program.errors.add(text)


    def __getitem__(self, i):
        if isinstance(i, str):
            out = self.prop.get(i, "")
            if i == "type":
                return str(out)
            return out
        return self.children[i]

    def __setitem__(self, key, val):
        if key == "type" and not isinstance(val, datatype):
            self.type(val)
        else:
            self.prop[key] = val

    def __hasitem__(self, key):
        return key in self.prop

    def __len__(self):
        return len(self.children)

    def __str__(self):
        if not self.prop.has_key("str"):
            return self.summary()
        return self.prop["str"]

    def __add__(self, val):
        return str(self)+val

    def __radd__(self, val):
        return val+str(val)

    def __iter__(self):
        return self.children.__iter__()


def init(node, parent, name=None):

    node.children = []      # node children
    node.prop = {}          # node property

    # Parental relationship
    node.parent = parent
    node.program = parent.program
    if name != "program":
        parent.children.append(node)

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
    node["pointers"] = 0
    node["type"] = datatype("TYPE")

