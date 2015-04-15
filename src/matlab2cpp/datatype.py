dim0 = {"int", "float", "double", "uint", "complex"}
dim1 = {"ivec", "fvec", "uvec", "vec", "cx_vec"}
dim2 = {"irowvec", "frowvec", "urowvec", "rowvec", "cx_rowvec"}
dim3 = {"imat", "fmat", "umat", "mat", "cx_mat"}
dim4 = {"icube", "fcube", "ucube", "cube", "cx_cube"}

dims = [dim0, dim1, dim2, dim3, dim4]

type0 = {"uint", "uvec", "urowvec", "umat", "ucube"}
type1 = {"int", "ivec", "irowvec", "imat", "icube"}
type2 = {"float", "fvec", "frowvec", "fmat", "fcube"}
type3 = {"complex", "cx_vec", "cx_rowvec", "cx_mat", "cx_cube"}

types = [type0, type1, type2, type3]

others = {"char", "TYPE", "func_lambda"}


def validate_name(val):

    if not isinstance(val, str):
        if isinstance(val[0], int):
            val = dims[val[0]].intersection(types[val[1]]).pop()
        else:
            vals = map(validate_name, val)
            assert len(vals)>0
            val = reduce(lambda x,y:x+y, vals).val
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


def get_type(val):

    if val in type0:    type = 0
    elif val in type1:  type = 1
    elif val in type2:  type = 2
    elif val in type3:  type = 3
    elif val in others: type = None
    else:
        raise ValueError("%s not recognized" % val)

    return type

def get_numeric(val):

    if val in others:   numeric = False
    else:               numeric = True

    return numeric


def get_name(dim, type):
    return dims[dim].intersection(types[type]).pop()


class Datatype(object):
    def __init__(self):
        self.node = None
    def __radd__(self, val):
        return self.__add__(val)
    def __rmul__(self, val):
        return self.__mul__(val)

class Dim(Datatype):

    def __get__(self, instance, owner):
        return get_dim(instance._datatype)

    def __set__(self, instance, value):
        type = get_type(instance._datatype)
        instance._datatype = get_name(value, type)

    def __add__(self, dims):
        if not isinstance(dims, (tuple, list)):
            dims = [dims]
        dims = list(dims) + [self.node.dim]
        dim = max(*dims)
        if dim == 2 and 1 in dims:
            self.node._datatype = "TYPE"
        else:
            self.node.dim = dim

    def __iadd__(self, dim):
        self.node.dim = self.node.dim + dim

    def __isub__(self, dim):
        self.node.dim = self.node.dim - dim

    def __mul__(self, dims):
        if not isinstance(dims, (tuple, list)):
            dims = [dims]
        dims = list(dims) + [self.node]
        dim = max(*dims)
        if dim == 2 and 1 in dims:
            self.node._datatype = "TYPE"
            return
        self.node.dim = dim



class Type(Datatype):
    def __get__(self, instance, owner):
        return get_type(instance._datatype)
    def __set__(self, instance, value):
        dim = get_dim(instance._datatype)
        instance._datatype = get_name(dim, value)

    def __add__(self, types):
        if not isinstance(types, (tuple, list)):
            types = [types]
        types = list(types) + [self.node.type]
        type = max(*types)
        self.node.type = type

    def __iadd__(self, type):
        self.node.type = self.node.type + type

    def __isub__(self, dim):
        self.node.type = self.node.type - type

    def __mul__(self, types):
        return self.__add__(types)


class Numeric(Datatype):
    def __get__(self, instance, owner):
        return get_numeric(instance._datatype)
    def __set__(self, instance, value):
        if not value:
            instance._datatype = "TYPE"
        raise AttributeError("numeric can not be set True consistently")


class Name(Datatype):

    def __get__(self, instance, owner):
        return instance._datatype

    def __set__(self, instance, value):
        value = validate_name(value)
        instance._datatype = value

    def __iadd__(self, vals):

        if not isinstance(vals, (tuple, list)):
            vals = [vals]
        vals = map(validate_name, vals)
        vals = set(vals + [self.node._datatype])

        if len(vals) == 1:
            self.node._datatype = vals.pop()

        for other in others:
            if other in vals:
                self.node._datatype = "TYPE"
                return

        dims = map(get_dim, vals)
        dim = max(*dims)
        if dim == 2 and 1 in dims:
            self.node._datatype = "TYPE"
            return

        types = map(get_type, vals)
        type = max(*types)

        name = get_name(dim, type)
        self.node._datatype = name

    def __imul__(self, vals):

        if not isinstance(vals, (tuple, list)):
            vals = [vals]
        vals = map(validate_name, vals)
        vals = set(vals + [self.node._datatype])

        vals.discard("TYPE")

        if len(vals) == 1:
            self.node._datatype = vals.pop()

        for other in others:
            vals.discard(other)

        if not vals:
            self.node._datatype = vals.pop()
            return

        dims = map(get_dim, vals)
        dim = max(*dims)
        if dim == 2 and 1 in dims:
            dim = 3

        types = map(get_type, vals)
        type = max(*types)

        name = get_name(dim, type)
        self.node._datatype = name

