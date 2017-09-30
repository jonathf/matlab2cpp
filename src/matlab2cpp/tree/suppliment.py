
class Fbuilder(object):
    "Same as Ftypes, but placed in builder"
    def __get__(self, instance, owner):
        out = {}
        for program in instance:
            out.update(program.ftypes)
        return out
    def __set__(self, instance, value):
        for program in instance:
            program.ftypes = value


class Ibuilder(object):
    "Same as Itypes, but placed in builder"
    def __get__(self, instance, owner):
        out = set()
        for program in instance:
            out = out.union(program.itypes)
        return out
    def __set__(self, instance, value):
        for program in instance:
            program.itypes = value


class Sbuilder(object):
    "Same as Stypes, but placed in builder"
    def __get__(self, instance, owner):
        out = {}
        for program in instance:
            out.update(program.stypes)
        return out
    def __set__(self, instance, value):
        for program in instance:
            program.stypes = value


class Vbuilder(object):
    "Same as Vtypes, but placed in builder"
    def __get__(self, instance, owner):
        out = {}
        for program in instance:
            out.update(program.vtypes)
        return out
    def __set__(self, instance, value):
        for program in instance:
            program.vtypes = value




