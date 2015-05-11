import collection
import datatype as dt
import targets
import snippets
import utils

import time
from datetime import datetime as date

indexnames = [
    "Assign", "Assigns", "Branch", "For", "Func",
    "Set", "Cset", "Fset", "Nset",
    "Get", "Cget", "Fget", "Nget",
    "Statement", "Switch", "Tryblock",
    "While", "Program", "Block", "Node",
]

class Prop(object):
    "general property node"

    def __init__(self, name):
        self.name = name
    def __get__(self, instance, owner):
        return instance.prop[self.name]
    def __set__(self, instance, value):
        instance.prop[self.name] = value

class Rprop(object):
    "recursive property node"

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):

        a = instance.prop[self.name]
        if not (a is None):
            return a

        instances = [instance]
        while True:
            instance = instance.parent
            a = instance.prop[self.name]
            instances.append(instance)
            if a is None:
                assert instance["class"] not in ("Program", "Node")
            else:
                break

        for instance in instances[:-1]:
            instance.prop[self.name] = a

        return a

    def __set__(self, instance, value):
        instance.prop[self.name] = value





class Node(object):
    """
General definition of a token representation of code
    """

    dim = dt.Dim()
    mem = dt.Mem()
    num = dt.Num()
    type = dt.Type()

    backend = Prop("backend")
    str = Prop("str")
    value = Prop("value")
    pointer = Prop("pointer")
    cls = Prop("class")

    end = Prop("end")
    line = Rprop("line")
    cur = Rprop("cur")
    code = Rprop("code")

    def __init__(self, parent=None, name=None):
        """
Parameters
----------
parent : Node
    Node parent in the token tree
name : str
    Optional name of the node
        """
        if parent is None:
            parent = self
            self.program = self
            name = "program"

        init(self, parent, name)

    def summary(self, disp=False, group=None):
        "Node summary"

        nodes = utils.flatten(self, False, False, False)
        if disp:
            print "iterating %d nodes" % len(nodes)

        if not (group is None):
            for node in nodes:
                if node.cls != "Block" and node.line == group:
                    return node.summary(disp, None)

        indent = [self]
        out = ""
        for node in nodes:

            line = node.line
            cur = node.cur

            name = node["name"]
            cls = node["class"]
            backend = node["backend"]
            type = node.type

            if backend == "unknown" and type != "TYPE":
                backend = type

            while indent and not (node.parent is indent[-1]):
                indent.pop()

            space = "| "*(len(indent)-1)
            out += "%3d %3d %s%-10s %-12s %-7s %-18s" % \
                    (line, cur, space, cls, backend, type, name)
            out += str(node["ret"]) + "\n"

            indent.append(node)

        return out


    def generate(self, disp=False, group=None):
        """Generate code"""

        nodes = utils.flatten(self, False, True, False)
        if disp:
            print "iterating %d nodes" % len(nodes)

        for node in nodes[::-1]:

            type_ = node.get_global_type()
            if type == "TYPE":
                type_ = node.type
            name = node["name"]
            cls = node["class"]
            backend = node["backend"]

            if backend == "unknown" and type_ != "TYPE":
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
                raise ValueError(
        "missing return in function %s in file %s" % (cls, backend))

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

        return self.prop["str"]


    def configure(self, suggestion=False, disp=False):

        nodes = utils.flatten(self, False, True, False)
        if disp:
            print "configuring %d nodes" % len(nodes)

        # Find if some names should be reserved
        reserved = {}
        for node in nodes[::-1]:

            name = node["name"]
            if name in targets.reserved.reserved:

                if name not in reserved:
                    reserved[name] = True

                if (node.cls in ("Var", "Fvar", "Cvar") and \
                        node.parent.cls in \
                        ("Assign", "Assigns") and \
                        not (node is node.parent[-1])) or \
                        node.cls in ("Set", "Cset", "Fset", "Nset") or \
                        node.parent.cls == "Param":

                    reserved[name] = False
        reserved = set([k for k,v in reserved.items() if v])
        reserved = reserved.union({"_resize", "_vectorise", "_conv_to"})

        while True:

            for node in nodes[::-1]:

                name = node["name"]
                cls = node["class"]
                type = node.type

                # Assign some hereditary types
                if cls == "Get":

                    names = node.program["names"]
                    if node["name"] in names:
                        func = node.program[names.index(node["name"])]
                        if len(func[1]) == 1:
                            node["backend"] = "func_return"
                        else:
                            node["backend"] = "func_returns"

                elif type == "TYPE":
                    if cls == "Assign":
                        node.type = node[0].type

                    elif node.children and cls not in\
                            ("Set", "Cset", "Fset", "Nset",
                            "Cget", "Fget", "Nget", "Assign"):
                        node.type = [n.type for n in node]


                    elif cls in ("Div", "Eldiv", "Rdiv", "Elrdiv"):
                        if node.num and node.mem < 2:
                            node.mem = 2

                    elif cls == "Fvar":
                        node.set_global_type(type)

                backend = node["backend"]
                if name in reserved:
                    node["backend"] = "reserved"
                    node.generate(False, None)

                elif backend == "unknown" and type != "TYPE":
                    node["backend"] = type

                # Assign suggestion
                if cls == "For":
                    var, range = node[:2]
                    var.suggest("int")

                elif cls == "Get":

                    if backend == "func_return":
                        names = node.program["names"]
                        func = node.program[names.index(name)]
                        ret_val = func[1][0]
                        node.set_global_type(ret_val.type)
                        params = func[2]
#                          print repr(params.code)
#                          print repr(node.code)
#                          print params["class"]
#                          print len(node)
                        for i in xrange(len(node)):
                            params[i].suggest(node[i].type)

                    elif backend == "func_returns":
                        names = node.program["names"]
                        func = node.program[names.index(name)]
                        params = func[2]
                        for j in xrange(len(params)):
                            params[j].suggest(node[j].type)

#                      if backend == "func_lambda":
#                          names = node.program["names"]
#                          func = node.program[names.index(name)]
#                          ret_val = func[1][0]
#                          node.set_global_type(ret_val.type)
#                          params = func[2]
#                          for i in xrange(len(node)):
#                              params[i].suggest(node[i].type)

#                      elif name in ("i", "j"):
#                          node.suggest("imaginary_unit")

                    else:
                        node.generate(False, None)

                elif cls == "Assign" and node[0].cls != "Set":
                    node[0].suggest(node[1].type)

                elif cls in ("Var", "Fvar", "Cget", "Fget", "Nget",
                        "Assigns", "Vector", "Matrix", "Colon"):
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

        name = name or self["name"]

        if self.cls in ("Fvar", "Fset", "Fget", "Nset", "Nget"):
            structs = self.program[1]

            if name not in structs["names"]:
                struct = collection.Struct(structs, name)
            else:
                struct = structs[structs["names"].index(name)]

            if self.cls in ("Nget", "Nset"):

                if self[0].cls == "String":
                    sname = self[0]["value"]
                else:
                    sname = ""

            else:
                sname = self["sname"]

            if sname:
                if sname in struct["names"]:
                    node = struct[struct["names"].index(sname)]
                    if self.type != "TYPE":
                        node.type = self.type

                else:
                    node = collection.Declare(struct, sname)
                    node.type = self.type
                    node["suggestion"] = self.type

            type = "struct"

        else:
            type = self.type

        func = self.func
        declares = func[0]
        params = func[2]

        if name in params["names"]:
            return

        if name in declares["names"]:
            node = declares[declares["names"].index(name)]
            if type != "TYPE":
                node.type = type
            return

        node = collection.Declare(declares, name)
        node.type = type
        node["suggest"] = type


    def set_global_type(self, text):

        name = self["name"]
        if self["class"] in ("Program", "Include", "Includes",
                "Struct", "Structs"):
            return

        elif self.cls in ("Fvar", "Fget", "Fset", "Nget", "Nset"):
            if self.cls in ("Nget", "Nset"):
                if self[0].cls == "String":
                    sname = self[0]["value"]
                else:
                    return
            else:
                sname = self["sname"]

            structs = self.program[1]
            if name not in structs["names"]:
                return

            struct = structs[structs["names"].index(name)]

            if sname not in struct["names"]:
                return

            node = struct[struct["names"].index(sname)]

        else:
            if self["class"] == "Func":
                func = self
            else:
                func = self.func

            declares = func[0]
            params = func[2]

            if name in declares["names"]:
                node = declares[declares["names"].index(name)]
            elif name in params["names"]:
                node = params[params["names"].index(name)]
            else:
                return

        node.type = text

    def get_global_type(self):

        name = self["name"]
        if self["class"] in ("Program", "Include", "Includes",
                "Struct", "Structs"):
            return

        elif self.cls in ("Fvar", "Fget", "Fset", "Nget", "Nset"):
            if self.cls in ("Nget", "Nset"):
                if self[0].cls == "String":
                    sname = self[0]["value"]
                else:
                    return "TYPE"
            else:
                sname = self["sname"]

            structs = self.program[1]
            if name not in structs["names"]:
                return "TYPE"

            struct = structs[structs["names"].index(name)]

            if sname not in struct["names"]:
                return "TYPE"

            node = struct[struct["names"].index(sname)]

        else:
            if self["class"] == "Func":
                func = self
            else:
                func = self.func

            declares = func[0]
            params = func[2]

            if name in declares["names"]:
                node = declares[declares["names"].index(name)]
            elif name in params["names"]:
                node = params[params["names"].index(name)]
            else:
                return "TYPE"

        return node.prop["type"]


    def suggest(self, text):

        if text == "TYPE" or self.type != "TYPE":
            return

        name = self["name"]


        if self["class"] in ("Program", "Include", "Includes"):
            return

        elif self.cls in ("Fvar", "Fget", "Fset", "Nget", "Nset"):
            if self.cls in ("Nget", "Nset"):
                if self[0].cls == "String":
                    sname = self[0]["value"]
                else:
                    return
            else:
                sname = self["sname"]

            structs = self.program[1]
            if name not in structs["names"]:
                return

            struct = structs[structs["names"].index(name)]

            if sname not in struct["names"]:
                return

            node = struct[struct["names"].index(sname)]

        else:
            if self["class"] == "Func":
                func = self
            else:
                func = self.func

            declares = func[0]
            params = func[2]

            if name in declares["names"]:
                node = declares[declares["names"].index(name)]
            elif name in params["names"]:
                node = params[params["names"].index(name)]
            else:
                return

        if isinstance(text, str):
            text = [text]

        text = list(text)
        node["suggest"] = dt.common_loose(text + [node["suggest"]])


    def auxiliary(self, type=None, convert=False, resize=0):
        """Create a auxiliary variablele and
move actual calcuations to own line.

Parameters
----------
type : str, None
    If provided, auxiliary variable type will be converted
        """

        assert self.parent["class"] != "Assign",\
                ".auxiliary() must be triggered mid expression."

        type = type or self.type

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

        v = s
        if convert:
            v = collection.Get(v, "_conv_to")
            v.backend = "reserved"
            v.type = type

        v1 = collection.Var(v, var)
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
            v.children[-1] = self
        else:
            s.children[-1] = self

        # generate code
        s.generate(False)
        v1.generate(False)

        return v1

    def vectorise(self):

        assert self.cls == "Var"
        assert self.dim in (3,4)

        type = self.type
        backend = self.backend
        parent = self.parent
        name = self["name"]

        get = collection.Get(self, "_vectorise")
        get.type = type
        get.dim = 1
        get.backend = "reserved"

        var = collection.Var(get, name)
        var.type = type
        var.backend = backend

        # Rearange variables
        i = parent.children.index(self)
        parent.children[i] = get
        get.parent = parent

        get.generate(False)

        return get

    def resize(self):
        """
Special resize manuver for cubes
a -> resize(a, a.n_rows, a.n_cols*a.n_slices, 1)
        """

        assert self.cls == "Var"
        assert self.dim == 4

        type = self.type
        backend = self.backend
        parent = self.parent
        name = self["name"]

        get = collection.Get(self, "_resize")
        get.type = type
        get.backend = "reserved"

        var = collection.Var(get, name)
        var.type = type
        var.backend = backend

        rows = collection.Var(get, name+".n_rows")
        rows.type = "int"
        rows.backend = "int"

        mul = collection.Mul(get)
        mul.type = "int"
        mul.backend = "expression"

        cols = collection.Var(mul, name+".n_cols")
        cols.type = "int"
        cols.backend = "int"

        slices = collection.Var(mul, name+".n_slices")
        slices.type = "int"
        slices.backend = "int"

        collection.Int(get, "1")

        # Rearange variables
        i = parent.children.index(self)
        parent.children[i] = get
        get.parent = parent

        get.generate(False)

        return get


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


    def error_log(self):

        ts = time.time()
        log = "Translated on " +\
                date.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S\n\n')

        for node in utils.flatten(self):

            cls = node.cls

            if cls == "Assign":
                n0, n1 = node
                t0, t1 = n0.type, n1.type
                if "TYPE" in (t0, t1):
                    continue

                elif n0.num != n1.num:
                    msg = "Incompatible types (%s) and (%s)" % (t0, t1)
                    log = log + node.message(msg, "Error")

                elif n0.dim == n1.dim and n0.mem < n1.mem:
                    msg = "Type conversion (%s) and (%s)" % (t0, t1)
                    log = log + node.message(msg, "Warning")

                elif n0.dim != n1.dim:
                    msg = "Incompatible dimensions (%s) and (%s)" % (t0, t1)
                    log = log + node.message(msg, "Error")

#              elif cls == "Var":
#                  if node.type == "TYPE":
#                      msg = "Undefined variable (%s)" % node["name"]
#                      log = log + node.message(msg, "Error")
#  
#              elif cls == "Get":
#                  if node.type == "TYPE":
#                      msg = "Undefined function/array (%s)" % node["name"]
#                      log = log + node.message(msg, "Error")

            elif cls in ("Fvar", "Fget", "Fset", "Nget", "Nset"):
                msg = "Fieldnames is currently not supported"
                log = log + node.message(msg, "Error")


            elif cls in ("Cvar", "Cget", "Cset"):
                msg = "Cell-structures currently not supported"
                log = log + node.message(msg, "Error")

            elif cls == "Try":
                msg = "Try-catch currently not supported"

            elif cls == "While":
                msg = "While-loops currently not supported"

        return log


    def message(self, msg, typ="Error"):

        code = self.program.code
        cur = self.cur
        end = cur+len(self.code)

        start = cur
        while code[start] != "\n":
            start -= 1

        finish = end
        while code[finish] != "\n":
            finish += 1

        pos = cur-start

        error = "%d %d" % (self.line, pos) + " " + typ + " in " +\
                self.cls + ": " + msg + "\n"
        error = error + '"' + code[start+1:finish] + '"'
        error = error + "\n\n"

        return error


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



def init(node, parent, name):

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

    if cls in ("Program", "Func", "Node"):
        node.func = node
    else:
        node.func = parent.func

    node["backend"] = "unknown"
    node["str"] = ""
    node["value"] = ""
    node["pointer"] = 0
    node["names"] = []

    node["suggest"] = "TYPE"
    node["type"] = "TYPE"

    node["cur"] = None
    node["line"] = None
    node["code"] = None

