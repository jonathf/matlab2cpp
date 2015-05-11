dim0 = {"int", "float", "double", "uword", "cx_double"}
dim1 = {"ivec", "fvec", "uvec", "vec", "cx_vec"}
dim2 = {"irowvec", "frowvec", "urowvec", "rowvec", "cx_rowvec"}
dim3 = {"imat", "fmat", "umat", "mat", "cx_mat"}
dim4 = {"icube", "fcube", "ucube", "cube", "cx_cube"}

dims = [dim0, dim1, dim2, dim3, dim4]

mem0 = {"uword", "uvec", "urowvec", "umat", "ucube"}
mem1 = {"int", "ivec", "irowvec", "imat", "icube"}
mem2 = {"float", "fvec", "frowvec", "fmat", "fcube"}
mem3 = {"double", "vec", "rowvec", "mat", "cube"}
mem4 = {"cx_double", "cx_vec", "cx_rowvec", "cx_mat", "cx_cube"}

mems = [mem0, mem1, mem2, mem3, mem4]

others = {"char", "TYPE", "func_lambda", "struct", "imaginary_unit"}


def common_loose(vals):
    """Common denominator among several names.
Loose enforcment"""

    if not isinstance(vals, (tuple, list)) or \
            isinstance(vals[0], int):
        vals = [vals]
    vals = list(vals)

    for i in xrange(len(vals)):
        if isinstance(vals[i], str):
            continue
        if isinstance(vals[i][0], int):
            vals[i] = get_name(*vals[i])

    vals = set(vals)

    if len(vals) == 1:
        return vals.pop()

    vals.discard("TYPE")

    if len(vals) == 1:
        return vals.pop()

    for other in others:
        vals.discard(other)

    if len(vals) == 0:
        return "TYPE"
    elif len(vals) == 1:
        return vals.pop()

    dims_ = map(get_dim, vals)
    if dims_:
        dim = max(*dims_)
    else:
        return "TYPE"
    if dim == 2 and 1 in dims_:
        dim = 3

    types = map(get_mem, vals)
    type = max(*types)

    val = get_name(dim, type)
    return val


def common_strict(vals):
    """Common denominator among several names.
Strict enforcment"""

    if not isinstance(vals, (tuple, list)) \
            or isinstance(vals[0], int):
        vals = [vals]

    vals = list(vals)

    for i in xrange(len(vals)):
        if isinstance(vals[i], str):
            continue
        if isinstance(vals[i][0], int):
            vals[i] = get_name(*vals[i])

    vals = set(vals)

    if len(vals) == 1:
        return vals.pop()

    for other in others:
        if other in vals:
            return "TYPE"

    dims_ = map(get_dim, vals)
    dim = max(*dims_)
    if dim == 2 and 1 in dims_:
        return "TYPE"

    types = map(get_mem, vals)
    type = max(*types)

    val = get_name(dim, type)
    return val



def get_dim(val):

    if val in dim0:     dim = 0
    elif val in dim1:   dim = 1
    elif val in dim2:   dim = 2
    elif val in dim3:   dim = 3
    elif val in dim4:   dim = 4
    elif val in others: dim = None
    else:
        raise ValueError("%s not recognized" % val)
    return dim


def get_mem(val):

    if val in mem0:    mem = 0
    elif val in mem1:  mem = 1
    elif val in mem2:  mem = 2
    elif val in mem3:  mem = 3
    elif val in mem4:  mem = 4
    elif val in others: mem = None
    else:
        raise ValueError("%s not recognized" % val)

    return mem

def get_num(val):

    if val in others:   num = False
    else:               num = True

    return num


def get_name(dim, mem):
    return dims[dim].intersection(mems[mem]).pop()


def get_type(instance):

    name = instance["name"]
    val = instance.prop["type"]
    if val != "TYPE":
        return val

    if instance.parent["class"] in ("Params", "Declares", "Struct"):
        return val

    if instance["class"] in ("Program", "Include", "Includes"):
        return "TYPE"

    elif instance.cls in ("Fvar", "Fget", "Fset", "Nget", "Nset"):
        if instance.cls in ("Nget", "Nset"):
            if instance[0].cls == "String":
                sname = instance[0]["value"]
            else:
                return "TYPE"
        else:
            sname = instance["sname"]

        structs = instance.program[1]
        if name not in structs["names"]:
            return "TYPE"

        struct = structs[structs["names"].index(name)]

        if sname not in struct["names"]:
            return "TYPE"

        node = struct[struct["names"].index(sname)]

    else:
        if instance["class"] == "Func":
            func = instance
        else:
            func = instance.func

        declares = func[0]
        params = func[2]

        if name in declares["names"]:
            node = declares[declares["names"].index(name)]
        elif name in params["names"]:
            node = params[params["names"].index(name)]
        else:
            return "TYPE"

    return node.prop["type"]

    name = instance["name"]
    if instance["class"] in ("Program", "Include", "Includes",
            "Struct", "Structs"):
        return


class Dim(object):

    def __get__(self, instance, owner):
        return get_dim(get_type(instance))

    def __set__(self, instance, value):
        mem = get_mem(get_type(instance))
        instance.prop["type"] = get_name(value, mem)


class Mem(object):

    def __get__(self, instance, owner):
        return get_mem(get_type(instance))

    def __set__(self, instance, value):
        dim = get_dim(get_type(instance))
        instance.prop["type"] = get_name(dim, value)


class Num(object):

    def __get__(self, instance, owner):
        return get_num(get_type(instance))

    def __set__(self, instance, value):
        if not value:
            instance.prop["type"] = "TYPE"
        else:
            raise AttributeError("num can not be set True consistently")


class Type(object):

    def __get__(self, instance, owner):
        return get_type(instance)

    def __set__(self, instance, value):
        value = value or "TYPE"
        value = common_strict(value)
        instance.prop["type"] = value
