"""
Expression interpretor
"""

import matlab2cpp as mc
from . import (
    findend,
    identify,
    constants as c,
)


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

    >>> builder = mc.Builder(True)
    >>> builder.load("unnamed", "a*b+c/d")
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
    >>> print(mc.qtree(builder, core=True)) # doctest: +NORMALIZE_WHITESPACE
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

    if self.code[start:start+3] == "...":
        start = findend.dots(self, start)
        start += 1
        while self.code[start] in " \t":
            start += 1

    if self.code[start] == ":":

        if self.disp:

            print("%4d     Expression " % (start),)
            print("%-20s" % "expression.create",)
            print(repr(self.code[start:start+1]))

            print("%4d     All        " % (start),)
            print("%-20s" % "expression.create",)
            print(repr(self.code[start:start+1]))

        mc.collection.All(node, cur=start, code=self.code[start])
        return start

    if end is None:
        end = findend.expression(self, start)

    if self.disp:
        print("%4d     Expression " % (start),)
        print("%-20s" % "expression.create",)
        print(repr(self.code[start:end+1]))

    if  self.code[start] not in c.e_start:
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
                    if self.code[last] not in c.letters+c.digits+")]}" or\
                            self.code[k-1] in "dDeE" and self.code[k-2] in\
                            c.digits+"." and self.code[k+1] in c.digits:
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

            elif self.code[k] in c.letters+c.digits+"_":
                last = k

            k += 1
            if k >= end:
                ends.append(end)
                break

        if len(ends)>1:

            node = retrieve_operator(self, opr)(node)
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

            node = mc.collection.Neg(node, cur=start, code=self.code[start:end+1])
            start += 1

        if self.code[start] == "~":

            node = mc.collection.Not(node, cur=start, code=self.code[start:end+1])
            start += 1

        while self.code[start] in " \t":
            start += 1

    # Postfixes
    if self.code[end] == "'" and not self.code[start] == "'":
        if self.code[end-1] == ".":
            node = mc.collection.Transpose(node, cur=start,
                    code=self.code[start:end+1])
            end -= 2
        else:
            node = mc.collection.Ctranspose(node, cur=start,
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

        node = mc.collection.Paren(node, cur=start, code=self.code[start:end+1])

        start += 1
        while self.code[start] in " \t":
            start += 1

        end -= 1
        while self.code[end] in " \t":
            end -= 1

        return create(self, node, start, end)

    # Reserved keywords
    elif self.code[start:start+3] == "end" and self.code[start+3] in " +-:\t" + c.e_end:
        node = mc.collection.End(node, cur=start, code=self.code[start:start+3])

    elif self.code[start:start+6] == "return" and self.code[start+6] in " ,;\n":
        node = mc.collection.Return(node, cur=start, code=self.code[start:start+6])

    elif self.code[start:start+5] == "break" and self.code[start+5] in " ,;\n":
        node = mc.collection.Break(node, cur=start, code=self.code[start:start+5])


    # Rest
    elif self.code[start] == "'":
        if self.code[end] != "'":
            self.syntaxerror(end, "string end")

        if "\n" in self.code[start:end]:
            self.syntaxerror(end, "non line-feed characters in string")

        mc.collection.String(node, self.code[start+1:end], cur=start,
                code=self.code[start:end+1])

    elif self.code[start] in c.digits or\
            self.code[start] == "." and self.code[start+1] in c.digits:
        cur = self.create_number(node, start)

    elif self.code[start] == "[":
        cur = self.create_matrix(node, start)

    elif self.code[start] == "{":
        cur = self.create_cell(node, start)

    else:
        if self.code[start] not in c.letters+"@":
            self.syntaxerror(start, "variable name")

        cur = self.create_variable(node, start)

    return END


def retrieve_operator(self, opr):
    """
Retrieve operator class by string

Args:
    opr (str): operator string
Returns:
    Node: class of corrensponding operator
    """

    if opr == "^":      return mc.collection.Exp
    elif opr == ".^":   return mc.collection.Elexp
    elif opr == "\\":   return mc.collection.Leftmatrixdivision
    elif opr == ".\\":  return mc.collection.Leftelementdivision
    elif opr == "/":    return mc.collection.Matrixdivision
    elif opr == "./":   return mc.collection.Elementdivision
    elif opr == "*":    return mc.collection.Mul
    elif opr == ".*":   return mc.collection.Elmul
    elif opr == "+":    return mc.collection.Plus
    elif opr == "-":    return mc.collection.Minus
    elif opr == ":":    return mc.collection.Colon
    elif opr == "<":    return mc.collection.Lt
    elif opr == "<=":   return mc.collection.Le
    elif opr == ">":    return mc.collection.Gt
    elif opr == ">=":   return mc.collection.Ge
    elif opr == "==":   return mc.collection.Eq
    elif opr == "~=":   return mc.collection.Ne
    elif opr == "&":    return mc.collection.Band
    elif opr == "|":    return mc.collection.Bor
    elif opr == "&&":   return mc.collection.Land
    elif opr == "||":   return mc.collection.Lor


if __name__ == "__main__":
    import doctest
    doctest.testmod()
