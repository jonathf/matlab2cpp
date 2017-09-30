import matlab2cpp as mc

def type_string(node):
    """
Determine string represnentation of type.

Outside scalars and armadillo, the datatype name and their declaration do not
match. This function converts simple datatype declaration and translate them to
equivalent C++ declarations.

+-----------------+-----------------------+
| Input           | Output                |
+=================+=======================+
| numerical types | node.type             |
+-----------------+-----------------------+
| struct, structs | struct container name |
+-----------------+-----------------------+
| func_lambda     | std::function<...>    |
+-----------------+-----------------------+
| string          | std::string           |
+-----------------+-----------------------+

Args:
    node (Node): location in tree
Returns:
    str: String representation of node type
    """

    # lambda-function
    if node.type == "func_lambda":

        # link to actual lambda-function
        func = None

        if hasattr(node.declare, "reference"):
            func = node.declare.reference

        elif "_"+node.name in node.program[1].names:
            func = node.program[1]["_"+node.name]

        if not (func is None):

            # no returns in lambda
            if len(func[1]) == 0:
                ret = "void"
                prm = ", ".join([p.type for p in func[2]])

            # single return
            elif len(func[1]) == 1:
                ret = func[1][0].type
                prm = ", ".join([p.type for p in func[2]])

            # multiple return
            else:
                ret = "void"
                prm = ", ".join([p.type for p in func[2][:]+func[1][:]])

            return "std::function<" + ret + "(" + prm + ")>"

        else:
            node.warning("lambda function content not found")
            return "std::function"

    # struct scalar and array type
    elif node.type in ("struct", "structs"):
        declare = node.declare
        if declare.parent.cls == "Struct":
            declare = declare.parent
        return "_" + declare.name.capitalize()

    elif node.type == "string":
        return "std::string"

    return node.type

if __name__ == "__main__":
    import doctest
    doctest.testmod()
