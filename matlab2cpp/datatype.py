"""
One of the translation challenges is how each variable type determined. In C++
all variables have to be explicitly declared, while in Matlab they are declared
implicitly at creation.  When translating between the two languages, there are
many variables where the data types are unknown and impossible for the
Matlab2cpp software to translate.  How to translate the behavior of an integer
is vastly different from an float matrix.
    
Variable types
--------------

Even though not always relevant, all node has it's own datatype.  It can be
referenced by `node.type` and can be inserted as placeholder through
`%(type)s`.  Note however that there are many data types available.  The
options for valid variable types are listed in the supplement file.  They can
be roughly split into two groups: **numerical** and **non-numerical** types.
The numerical types are as follows:

+---------------+----------------+---------+---------+----------+------------+
|               | *unsigned int* | *int*   | *float* | *double* | *complex*  |
+===============+================+=========+=========+==========+============+
| *scalar*      | uword          | int     | float   | double   | cx_double  |
+---------------+----------------+---------+---------+----------+------------+
| *vector*      | uvec           | ivec    | fvec    | vec      | cx_vec     |
+---------------+----------------+---------+---------+----------+------------+
| *row\-vector* | urowvec        | irowvec | frowvec | rowvec   | cx_rowvec  |
+---------------+----------------+---------+---------+----------+------------+
| *matrix*      | umat           | imat    | fmat    | mat      | cx_mat     |
+---------------+----------------+---------+---------+----------+------------+
| *cube*        | ucube          | icube   | fcube   | cube     | cx_cube    |
+---------------+----------------+---------+---------+----------+------------+

Values along the horizontal axis represents the amount of memory reserved per
element, and the along the vertical axis represents the various number of
dimensions.  The names are equivalent to the ones in the Armadillo package.

The non-numerical types are as follows:

+---------------+------------------------+
| Name          | Description            |
+===============+========================+
| *char*        | Single text character  |
+---------------+------------------------+
| *string*      | Text string            |
+---------------+------------------------+
| *struct*      | Struct container       |
+---------------+------------------------+
| *structs*     | Struct array container |
+---------------+------------------------+
| *func_lambda* | Anonymous function     |
+---------------+------------------------+
| *wall_clock*  | Timer function         |
+---------------+------------------------+

Numerical datatypes
~~~~~~~~~~~~~~~~~~~

Most of the allowed datatypes are numerical values with varying type-space and
dimensionality.  So when addressing a numerical value, the nodes attributes
`node.dim` and node.mem` can often be useful, since they contain direct
information about that information.

Example:
    >>> node = mc.collection.Var(None, "name", type="ivec")
    >>> print node.type
    ivec
    >>> print node.dim, node.mem
    1 1

These nodes also support dynamic rewriting of the datatype.
Continuing our example:
    >>> node.dim = 3
    >>> print node.type
    imat
    >>> node.mem = 4
    >>> print node.type
    cx_mat

The connection between the nummerical values and datatypes is as follows:

+-------+-------------+--+-------+--------------+
| *mem* | Description |  | *dim* | Description  |
+=======+=============+==+=======+==============+
| 0     | unsiged int |  | 0     | scalar       |
+-------+-------------+--+-------+--------------+
| 1     | integer     |  | 1     | (col-)vector |
+-------+-------------+--+-------+--------------+
| 2     | float       |  | 2     | row-vector   |
+-------+-------------+--+-------+--------------+
| 3     | double      |  | 3     | matrix       |
+-------+-------------+--+-------+--------------+
| 4     | complex     |  | 4     | cubu         |
+-------+-------------+--+-------+--------------+
"""

import supplement
import matlab2cpp as mc

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

others = {"char", "string", "TYPE", "func_lambda", "struct", "structs", "cell",
        "wall_clock"}


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

def pointer_split(name):
    p = name.count("*")
    if not p:
        return 0, name
    return p, name[:-p]


def get_dim(val):

    while val[-1] == "*":
        val = val[:-1]

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

    while val[-1] == "*":
        val = val[:-1]

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

    while val[-1] == "*":
        val = val[:-1]

    if val in others:   num = False
    else:               num = True

    return num


def get_name(dim, mem):
    return dims[dim].intersection(mems[mem]).pop()


def get_type(instance):

    if instance.prop["type"] == "TYPE":
        instance = instance.declare
    return instance.prop["type"]

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
        return get_type(instance) #+ "*"*instance.pointer

    def __set__(self, instance, value):
        value = value or "TYPE"
        if isinstance(value, str):
            p, value = pointer_split(value)
            instance.pointer = p
        else:
            value = common_strict(value)
        instance.prop["type"] = value


class Suggest(object):

    def __set__(self, instance, value):
        if value == "TYPE":
            return
        instance.declare.prop["suggest"] = value
    def __get__(self, instance, owner):
        return supplement.suggests.get(instance)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
