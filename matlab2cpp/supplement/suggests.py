"""
"""

def get(node):

    funcs = node.program[1]
    structs = node.program[3]

    suggest = {}

    for func in funcs:

        suggest[func.name] = suggest_ = {}

        declares, params = func[0], func[2]
        for var in declares[:]+params[:]:

            type = var.prop["type"]
            if type == "TYPE":
                type = ""

            if not type:

                type = var.prop["suggest"]
                if type == "TYPE":
                    type = ""
                if type:
                    suggest_[var.name] = type

    for struct in structs:

        suggest[struct.name] = suggest_ = {}

        for var in struct:

            type = var.prop["type"]
            if type == "TYPE":
                type = ""

            if not type:

                type = var.prop["suggest"]
                if type == "TYPE":
                    type = ""
                if type:
                    suggest_[var.name] = type

    return suggest

class Sstypes(object):

    def __get__(self, instance, owner):
        return get(instance)

    def __set__(self, instance, value):
        raise AttributeError("Suggestions not to be set manually")

if __name__ == "__main__":
    import doctest
    import matlab2cpp as mc
    doctest.testmod()
