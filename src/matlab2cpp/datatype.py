
types = [
    "char",
    "int", "float",
    "irowvec", "frowvec",
    "ivec", "fvec",
    "imat", "fmat",
    "TYPE"]

class datatype(object):

    def __init__(self, val):

        if not isinstance(val, str):
            vals = map(datatype, val)
            assert len(vals)>0
            val = reduce(lambda x,y:x+y, vals).val

        assert val in types, "%s not recognized" % val
        self.val = val

    def __radd__(self, other):
        return self.__add__(other)

    def __add__(self, other):

        if not other:
            return self

        if not isinstance(other, datatype):
            other = datatype(other)

        v, w = self.val, other.val

        if v == w:
            return self
        if "TYPE" in (v, w):
            return datatype("TYPE")

        if v == "int":
            return other

        if v == "float":
            if w == "int":
                return self
            return other

        if v == "ivec":
            if w == "int":
                return self
            if w == "float":
                return datatype("fvec")
            return other

        if v == "fvec":
            if w in ("int", "float", "ivec"):
                return self
            return other

        if v == "irowvec":
            if w == "int":
                return self
            if w in ("ivec", "fvec"):
                return datatype("TYPE")
            return other

        if v == "frowvec":
            if w in ("int", "float", "irowvec"):
                return self
            if w in ("ivec", "fvec"):
                return datatype("TYPE")
            return other

        if v == "imat":
            if w in ("int", "ivec", "irowvec"):
                return self
            if w in ("float", "fvec", "frowvec"):
                return datatype("fmat")
            return other

        if v == "fmat":
            return self

        if v == "char":
            return datatype("TYPE")

        print v, w
        raise ValueError, "datatype problems"

    def __eq__(self, other):
        if isinstance(other, datatype):
            return self.val == other.val
        elif isinstance(other, str):
            return self.val == other
        return NotImplemented

    def __req__(self, other):
        return self.__eq__(other)

    def __nonzeros__(self):
        return self.val != "TYPE"

    def __str__(self):
        return self.val
