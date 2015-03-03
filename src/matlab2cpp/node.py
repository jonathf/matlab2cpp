import collection
from datatype import datatype
import targets

class Node(object):

    def __init__(self, parent, name=None):
        init(self, parent, name)

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

    def summary(self):
        "Node summary"
        return self._summary(0)

    def _summary(self, indent):
        name = self["name"]
        cls = self["class"]
        backend = self["backend"]
        type = self.type()

        if backend == "unknown" and type != "TYPE":
            backend = type

        out = " "*indent + "%16s %-10s %-12s %-5s\n" % (name, cls, backend, type)
        for child in self.children:
            out += child._summary(indent+1)

        return out

    def generate(self):
        """Generate code"""
        self._generate()
        return self.prop["str"]

    def _generate(self):

        for node in self.children:
            node._generate()

        type_ = self.type()
        name = self["name"]
        cls = self["class"]
        backend = self["backend"]

        if type_ == "TYPE" and self.children and \
                cls not in ("Get", "Get2", "Get3"):
            type_ = self.type([n.type() for n in self.children])

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
            print name
            raise KeyError("no %s in %s" % (cls, backend))

        if not isinstance(value, (unicode, str, list, tuple)):
            value = value(self)

        if value is None:
            raise ValueError("missing return in %s.%s" % backend, cls)

        prop = self.prop.copy()
        I = len(self)
        for i in xrange(I):
            prop["%d" % i] = prop["-%d" % (I-i)] = self[i]["str"]

        if not isinstance(value, (str, unicode)):

            value = list(value)
            children = ["%("+str(i)+")s" for i in xrange(len(self))]

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

        self.prop["str"] = value

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

#              if text and text != "TYPE" and self["backend"] == "unknown":
#                  self["backend"] = text

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
            text = str(reduce(lambda x, y: datatype(x)+datatype(y)), text)

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
                node["suggest"] = datatype(text) + node["suggest"]

        return str(node["suggest"])

    def error(self, text):
        self.program.errors.add(text)



group_materials = [
    "Get", "Set", "Sets", "Assign", "Assigns", "Assigned",
    "Assignees", "Func", "Matrix", "For", "If", "Elif", "Else",
    "Block", "Branch", "Statement", "Program"
]

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
    if cls in group_materials:
        node.isgroup = True
    else:
        node.isgroup = False

    index = node.program.next_index()
    if name:
        node["name"] = name
    else:
        node["name"] = "@%06d%s" % (index, node["class"])

    if parent.prop["class"] in ("Program", "Func"):
        node.func = parent
    else:
        node.func = parent.func
    node.prop["func"] = node.func.prop["name"]

    if parent["class"] in group_materials:
        node.group = parent
    else:
        node.group = parent.group
    node["group"] = node.group["name"]

    node["backend"] = "unknown"
    node["str"] = ""
    node["value"] = ""

    node["pointers"] = 0
    node["aux"] = 0

    node["stop"] = False
    node["type"] = datatype("TYPE")
