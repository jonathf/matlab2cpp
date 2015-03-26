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

class datatype(object):

    def __init__(self, val):

        if not isinstance(val, str):
            if isinstance(val[0], int):
                val = dims[val[0]].intersection(types[val[1]]).pop()
            else:
                vals = map(datatype, val)
                assert len(vals)>0
                val = reduce(lambda x,y:x+y, vals).val

        self.val = val

        if val in dim0:     self.dim = 0
        elif val in dim1:   self.dim = 1
        elif val in dim2:   self.dim = 2
        elif val in dim3:   self.dim = 3
        elif val in dim4:   self.dim = 4
        elif val in others: self.dim = None
        else:
            raise ValueError("%s not recognized" % val)

        if val in type0:    self.type = 0
        elif val in type1:    self.type = 1
        elif val in type2:    self.type = 2
        elif val in type3:    self.type = 3
        else: self.type = None

        if val in others:   self.numeric = False
        else:               self.numeric = True


    def __add__(self, other):

        if self.val == other.val:
            return self

        if self.val == "TYPE":
            return datatype("TYPE")
        elif other.val == "TYPE":
            return datatype("TYPE")

        if not self.numeric:
            return datatype("TYPE")
        elif not other.numeric:
            return datatype("TYPE")

        dim = max(self.dim, other.dim)
        if dim == 2 and 1 in (self.dim, other.dim):
            return datatype("TYPE")

        type = max(self.type, other.type)

        newval = dims[dim].intersection(types[type]).pop()
        return datatype(newval)


    def __mul__(self, other):
        if self.val == "TYPE":
            return other
        elif other.val == "TYPE":
            return self

        if not self.numeric:
            if not other.numeric:
                if self.val == other.val:
                    return self
            return other
        elif not other.numeric:
            return self

        dim = max(self.dim, other.dim)
        if dim == 2 and 1 in (self.dim, other.dim):
            dim = 3

        type = max(self.type, other.type)

        newval = dims[dim].intersection(types[type]).pop()
        return datatype(newval)


    def __eq__(self, other):
        if isinstance(other, datatype):
            return self.val == other.val
        return NotImplemented

    def __req__(self, other):
        return self.__eq__(other)

    def __nonzeros__(self):
        return self.val != "TYPE"

    def __str__(self):
        return self.val

    def __repr__(self):
        return 'datatype("' + self.val + '")'
