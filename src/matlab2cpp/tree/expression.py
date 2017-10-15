"""
Expression interpretor
"""
from __future__ import print_function
from .. import collection


RECIVER_OPERATORS = {
    "^": collection.Exp,
    ".^": collection.Elexp,
    "\\": collection.Leftmatrixdivision,
    ".\\": collection.Leftelementdivision,
    "/": collection.Matrixdivision,
    "./": collection.Elementdivision,
    "*": collection.Mul,
    ".*": collection.Elmul,
    "+": collection.Plus,
    "-": collection.Minus,
    ":": collection.Colon,
    "<": collection.Lt,
    "<=": collection.Le,
    ">": collection.Gt,
    ">=": collection.Ge,
    "==": collection.Eq,
    "~=": collection.Ne,
    "&": collection.Band,
    "|": collection.Bor,
    "&&": collection.Land,
    "||": collection.Lor,
}


def create(self, node, start, end=None, start_opr=None):
    """
Create expression in three steps:

    1) In order, split into sub-expressions for each dividing operator
    2) Address prefixes, postfixes, parenthesises, etc.
    3) Identify the remaining singleton

Args:
    self (Builder): Code constructor.
    node (Node): Reference to the parent node
    start (int): current possition in code
    end (int, optional): end of expression. Required for space-delimited expression.
    start_opr (str, optional): At which operator the recursive process is. (For internal use)

Returns:
	int : index to end of the expression

Examples::

    >>> from matlab2cpp.tree import Builder
    >>> builder = Builder(True)
    >>> builder.load("unnamed", "a*b+c/d") # doctest: +NORMALIZE_WHITESPACE
    loading unnamed
         Program     functions.program
       0 Main        functions.main
       0 Codeblock   codeblock.codeblock 
       0   Statement     codeblock.codeblock  'a*b+c/d'
       0     Expression  expression.create    'a*b+c/d'
       0     Expression  expression.create    'a*b'
       0     Expression  expression.create    'a'
       0     Var         variables.variable   'a'
       2     Expression  expression.create    'b'
       2     Var         variables.variable   'b'
       4     Expression  expression.create    'c/d'
       4     Expression  expression.create    'c'
       4     Var         variables.variable   'c'
       6     Expression  expression.create    'd'
       6     Var         variables.variable   'd'
    >>> builder.configure(suggest=False)
    >>> print(matlab2cpp.qtree(builder, core=True)) # doctest: +NORMALIZE_WHITESPACE
    1 1Block      code_block   TYPE
    1 1| Statement  code_block   TYPE
    1 1| | Plus       expression   TYPE
    1 1| | | Mul        expression   TYPE
    1 1| | | | Var        unknown      TYPE    a
    1 3| | | | Var        unknown      TYPE    b
    1 5| | | Matrixdivisionexpression   TYPE
    1 5| | | | Var        unknown      TYPE    c
    1 7| | | | Var        unknown      TYPE    d
    """
    from . import findend, identify, constants

    if self.code[start:start+3] == "...":
        start = findend.dots(self, start)
        start += 1
        while self.code[start] in " \t":
            start += 1

    if self.code[start] == ":":

        if self.disp:

            print("%4d     Expression " % (start), end="")
            print("%-20s" % "expression.create", end="")
            print(repr(self.code[start:start+1]))

            print("%4d     All        " % (start), end="")
            print("%-20s" % "expression.create", end="")
            print(repr(self.code[start:start+1]))

        collection.All(node, cur=start, code=self.code[start])
        return start

    if end is None:
        end = findend.expression(self, start)

    if self.disp:
        print("%4d     Expression " % (start), end="")
        print("%-20s" % "expression.create", end="")
        print(repr(self.code[start:end+1]))

    if  self.code[start] not in constants.e_start:
        self.syntaxerror(start, "expression start")


    operators = [
        "||", "&&", "|", "&",
        "~=", "==", ">=", ">", "<=", "<",
        ":", "+", "-",
        ".*", "*", "./", "/", ".\\", "\\",
        ".^", "^"]

    if not (start_opr is None):
        operators = operators[operators.index(start_opr)+1:]

    for opr in operators:
        # Pre-screen
        if opr not in self.code[start:end+1]:
            continue

        starts = [start]
        last = start
        ends = []

        k = start
        while True:

            if self.code[k] == "(":
                k = last = findend.paren(self, k)

            elif self.code[k] == "[":
                k = last = findend.matrix(self, k)

            elif self.code[k] == "{":
                k = last = findend.cell(self, k)

            elif self.code[k] == "'":
                if identify.string(self, k):
                    k = last = findend.string(self, k)
                else:
                    last = k

            elif opr == self.code[k:k+len(opr)]:

                if opr in "+-":
                    # no prefixes and no (scientific) numbers
                    if self.code[last] not in constants.letters+constants.digits+")]}" or\
                            self.code[k-1] in "dDeE" and self.code[k-2] in\
                            constants.digits+"." and self.code[k+1] in constants.digits:
                        k += 1
                        continue


                k += len(opr)-1
                while self.code[k+1] in " \t":
                    k += 1

                # no all-operator
                if opr == ":" and self.code[k+1] in ",;\n)]}":
                    k += 1
                    continue

                starts.append(k+1)
                ends.append(last)

            elif self.code[k] in constants.letters+constants.digits+"_":
                last = k

            k += 1
            if k >= end:
                ends.append(end)
                break

        if len(ends) > 1:

            operator = RECIVER_OPERATORS[opr]
            node = operator(node)
            node.cur = start
            node.code = self.code[starts[0]:ends[-1]+1]

            for s,e in zip(starts, ends):
                create(self, node, s, e, opr)

            return end


    # All operators removed at this point!

    END = end

    # Prefixes
    while self.code[start] in "-~":

        if self.code[start] == "-":

            node = collection.Neg(node, cur=start, code=self.code[start:end+1])
            start += 1

        if self.code[start] == "~":

            node = collection.Not(node, cur=start, code=self.code[start:end+1])
            start += 1

        while self.code[start] in " \t":
            start += 1

    # Postfixes
    if self.code[end] == "'" and not self.code[start] == "'":
        if self.code[end-1] == ".":
            node = collection.Transpose(node, cur=start,
                    code=self.code[start:end+1])
            end -= 2
        else:
            node = collection.Ctranspose(node, cur=start,
                    code=self.code[start:end+1])
            node.cur = start
            node.code = self.code[start:end+1]
            end -= 1

        while self.code[end] in " \t":
            end -= 1

    # Parenthesis
    if self.code[start] == "(":
        if self.code[end] != ")":
            self.syntaxerror(end, "parenthesis end")

        node = collection.Paren(node, cur=start, code=self.code[start:end+1])

        start += 1
        while self.code[start] in " \t":
            start += 1

        end -= 1
        while self.code[end] in " \t":
            end -= 1

        return create(self, node, start, end)

    # Reserved keywords
    elif self.code[start:start+3] == "end" and self.code[start+3] in " +-:\t" + constants.e_end:
        node = collection.End(node, cur=start, code=self.code[start:start+3])

    elif self.code[start:start+6] == "return" and self.code[start+6] in " ,;\n":
        node = collection.Return(node, cur=start, code=self.code[start:start+6])

    elif self.code[start:start+5] == "break" and self.code[start+5] in " ,;\n":
        node = collection.Break(node, cur=start, code=self.code[start:start+5])


    # Rest
    elif self.code[start] == "'":
        if self.code[end] != "'":
            self.syntaxerror(end, "string end")

        if "\n" in self.code[start:end]:
            self.syntaxerror(end, "non line-feed characters in string")

        collection.String(node, self.code[start+1:end], cur=start,
                code=self.code[start:end+1])

    elif self.code[start] in constants.digits or\
            self.code[start] == "." and self.code[start+1] in constants.digits:
        cur = self.create_number(node, start)

    elif self.code[start] == "[":
        cur = self.create_matrix(node, start)

    elif self.code[start] == "{":
        cur = self.create_cell(node, start)

    else:
        if self.code[start] not in constants.letters+"@":
            self.syntaxerror(start, "variable name")

        cur = self.create_variable(node, start)

    return END
