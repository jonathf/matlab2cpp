import collection
import datatype as dt
import targets
import snippets
import utils
import reference as ref

import time
from datetime import datetime as date


class Node(object):
    """
General definition of a token representation of code
    """

    dim = dt.Dim()
    mem = dt.Mem()
    num = dt.Num()
    type = dt.Type()
    suggest = dt.Suggest()

    func = ref.Func_reference()
    program = ref.Program_reference()
    line = ref.Line_reference()
    group = ref.Group_reference()
    declare = ref.Declare_reference()

    names = ref.Names()

    backend = ref.Property_reference("backend")
    str = ref.Property_reference("str")
    ret = ref.Property_reference("ret")
    value = ref.Property_reference("value")
    pointer = ref.Property_reference("pointer")
    cls = ref.Property_reference("class")
    name = ref.Property_reference("name")

    line = ref.Recursive_property_reference("line")
    cur = ref.Recursive_property_reference("cur")
    code = ref.Recursive_property_reference("code")

    def __init__(self, parent, name="", backend="unknown", value="",
            type="TYPE", pointer=0, line=None, cur=None, code=None):
        """
Parameters
----------
parent : Node
    Node parent in the token tree
name : str
    Optional name of the node
        """
        self.children = []
        self.prop = {"type":type, "suggest":type,
                "value":value, "str":"", "name":name,
                "pointer":pointer, "backend":backend,
                "line":line, "cur":cur, "code":code,
                "ret":"",
                "class":self.__class__.__name__}

        # Parental relationship
        self.parent = parent

        if not (self is parent):
            parent.children.append(self)


    def summary(self):
        "Node summary"
        return utils.summary(self, None)


    def translate_tree(self, opt=None):
        """Generate code"""

        nodes = utils.flatten(self, False, True, False)
        if not (opt is None) and opt.disp:
            print "iterating %d nodes" % len(nodes)

        for node in nodes[::-1]:
            node.translate_node(opt)

        return self.prop["str"]

    def translate_node(node, opt=None):

        target = targets.__dict__[node.backend]
        spesific_name = node.cls + "_" + node.name

        if spesific_name in target.__dict__:
            value = target.__dict__[spesific_name]

        elif node.cls in target.__dict__:
            value = target.__dict__[node.cls]

        else:
            print node.program.summary()
            raise KeyError("no %s in %s" % (node.cls, node.backend))


        if not isinstance(value, (unicode, str, list, tuple)):
            value = value(node)

        if isinstance(value, (unicode, Node)):
            value = str(value)

        elif value is None:
            raise ValueError(
    "missing return in function %s in file %s" % (node.cls, node.backend))

        node.ret = repr(value)

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
            raise SyntaxError("interpolation in " + node.backend + "." +\
                    node.cls + " is misbehaving\n" + value + "\n"+str(prop))
        # print repr(value)

        node.prop["str"] = value

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
            if isinstance(type[0], int):
                type = dt.get_name(*type)
            else:
                type = dt.common_strict(type)

        if type == "TYPE":
            return self

        if self.cls in ("Vector", "Matrix"):
            backend = "matrix"
        else:
            backend = type

        line = self
        while line.parent.cls != "Block":
            line = line.parent
        block = line.parent

        # Create new var
        var = "_aux_" + type + "_"
        if var not in line.prop:
            line.prop[var] = 1
        else:
            line.prop[var] += 1
        var = var + str(line.prop[var])

        # Create Assign
        assign = collection.Assign(block, backend=backend, type=type)
        assign.declare.type = type

        # Return value
        aux_var = collection.Var(assign, var, backend=backend, type=type)
        aux_var.create_declare()

        if convert:
            rhs = collection.Get(assign, "_conv_to", backend=backend,
                    type=type)
        else:
            rhs = assign

        swap_var = collection.Var(rhs, var, backend=backend, type=type)
        swap_var.declare.type = type
        rhs.translate_node()

        # Place Assign correctly in Block
        i = block.children.index(line)
        block.children = block[:i] + block[-1:] + block[i:-1]

        # Swap self and Var
        index = self.parent.children.index(self)
        self.parent.children[index] = swap_var
        rhs.children[-1] = self

        swap_var.parent, self.parent = self.parent, swap_var.parent

        # generate code
        swap_var.translate_node()
        aux_var.translate_node()
        if convert:
            assign.translate_node()

        if convert:
            assert self.type != swap_var.type

        return swap_var

    def resize(self):

        if self["_resize"]:
            return
        self["_resize"] = True

        type = self.type
        self.dim = 3

        line = self
        while line.parent.cls != "Block":
            line = line.parent

        name = self.name
        value = self.type + " _" + name + "(" + name + \
                ".memptr(), " + name + ".n_rows, " + name + \
                ".n_cols*" + name + ".n_slices, false) ;"
        filler = collection.Filler(line.parent, value)

        i = line.parent.children.index(line)

        ps = line.parent.children
        line.parent.children = ps[:i] + ps[-1:] + ps[i:-1]

        filler.translate_node(False)

        self.type = type


    def include(self, name, **kws):

        program = self.program
        includes = program[0]
        idname, code = snippets.retrieve(self, name, **kws)

        if idname in includes.names:
            return idname

        for val in kws.values():
            if val == "TYPE":
                return "FUNC"

        collection.Include(includes, name=idname, value=code)
        return idname


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

            elif cls in ("Fvar", "Fget", "Fset", "Nget", "Nset", "Sset", "Sget"):
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
        while code[start] != "\n" and start != 0:
            start -= 1

        if end >= len(code):
            end = len(code)-1
        finish = end
        while code[finish] != "\n" and finish != len(code)-1:
            finish += 1

        pos = cur-start

        error = "%d %d" % (self.line, pos) + " " + typ + " in " +\
                self.cls + ": " + msg + "\n"
        error = error + '"' + code[start+1:finish] + '"'
        error = error + "\n\n"

        return error

    def create_declare(node):

        if not (node is node.declare):
            return node

        if node.cls in ref.structvars:
            if node.cls in ("Nget", "Nset"):
                if node[0].cls == "String":
                    return None
                value = node[0]["value"]
            else:
                value = node.value

            structs = node.program[1]
            assert structs.cls == "Structs"

            if node not in structs:
                struct = collection.Struct(structs, name=node.name)
            else:
                struct = structs[node]

            if value in struct.names:
                return struct[struct.names.index(value)]

            declares = node.func[0]

            if node.cls in ("Sset", "Sget"):
                sname = "_"+value+"_size"
                if sname not in struct.names:
                    collection.Counter(struct, sname, value="100")

                collection.Var(declares, name=node.name, value=value, type="structs")
            else:
                collection.Var(declares, name=node.name, value=value, type="struct")

            return collection.Var(struct, name=value)
            parent = struct

        else:
            parent = node.func[0]

        if node in parent:
            declare = parent[node]
            declare.type = node.type
            declare.pointer = node.pointer
            return declare

        return collection.Var(parent, name=node.name,
                type=node.type, pointer=node.pointer, value=node.value)


    def __getitem__(self, i):
        if isinstance(i, str):
            out = self.prop[i]
            return out

        if isinstance(i, Node):
            i = self.names.index(i.name)

        return self.children[i]

    def __contains__(self, i):
        return i.name in self.names

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

    def pop(self, index):
        return self.children.pop(index)



