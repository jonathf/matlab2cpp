"""
Expression interpretor
"""

from matlab2cpp.node import collection as col

import findend
import identify
import constants as c


def create(self, node, start, end=None, start_opr=None):
    """
Create expression in three steps:

    1) In order, split into sub-expressions for each dividing operator
    2) Address prefixes, postfixes, parenthesises, etc.
    3) Identify the remaining singleton

Args:
    node (Node): Reference to the parent node
    start (int): current possition in code

Kwargs:
    end (int, optional): end of expression
    start_opr (str, optional): At which operator the recursive process is

Returns:
	int : index to end of the expression
    """

    if self.code[start:start+3] == "...":
        start = findend.dots(self, start)
        start += 1
        while self.code[start] in " \t":
            start += 1

    if self.code[start] == ":":

        if self.disp:
            print "%4d     Expression " % (start),
            print repr(self.code[start:start+1])
            print "%4d     All        " % (start),
            print repr(self.code[start:start+1])

        col.All(node, cur=start, code=self.code[start])
        return start

    if end is None:
        end = findend.expression(self, start)

    if self.disp:
        print "%4d     Expression " % (start),
        print repr(self.code[start:end+1])

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

            node = self.retrieve_operator(opr)(node)
            node.cur = start
            node.code = self.code[starts[0]:ends[-1]+1]

            for s,e in zip(starts, ends):
                self.create(node, s, e, opr)

            return end


    # All operators removed at this point!

    END = end

    # Prefixes
    while self.code[start] in "-~":

        if self.code[start] == "-":

            node = col.Neg(node, cur=start, code=self.code[start:end+1])
            start += 1

        if self.code[start] == "~":

            node = col.Not(node, cur=start, code=self.code[start:end+1])
            start += 1

        while self.code[start] in " \t":
            start += 1

    # Postfixes
    if self.code[end] == "'" and not self.code[start] == "'":
        if self.code[end-1] == ".":
            node = col.Ctranspose(node, cur=start,
                    code=self.code[start:end+1])
            end -= 2
        else:
            node = col.Transpose(node, cur=start,
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

        node = col.Paren(node, cur=start, code=self.code[start:end+1])

        start += 1
        while self.code[start] in " \t":
            start += 1

        end -= 1
        while self.code[end] in " \t":
            end -= 1

        return self.create_expression(node, start, end)

    # Reserved keywords
    elif self.code[start:start+3] == "end" and\
            self.code[start+3] in " \t" + c.e_end:
                node = col.End(node, cur=start, code=self.code[start:start+3])

    elif self.code[start:start+6] == "return" and self.code[start+6] in " ,;\n":
        node = col.Return(node, cur=start, code=self.code[start:start+6])

    elif self.code[start:start+5] == "break" and self.code[start+5] in " ,;\n":
        node = col.Break(node, cur=start, code=self.code[start:start+5])


    # Rest
    elif self.code[start] == "'":
        if self.code[end] != "'":
            self.syntaxerror(end, "string end")

        if "\n" in self.code[start:end]:
            self.syntaxerror(end, "non line-feed characters in string")

        col.String(node, self.code[start+1:end], cur=start,
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

    if opr == "^":      return col.Exp
    elif opr == ".^":   return col.Elexp
    elif opr == "\\":   return col.Leftmatrixdivision
    elif opr == ".\\":  return col.Leftelementdivision
    elif opr == "/":    return col.Matrixdivision
    elif opr == "./":   return col.Elementdivision
    elif opr == "*":    return col.Mul
    elif opr == ".*":   return col.Elmul
    elif opr == "+":    return col.Plus
    elif opr == "-":    return col.Minus
    elif opr == ":":    return col.Colon
    elif opr == "<":    return col.Lt
    elif opr == "<=":   return col.Le
    elif opr == ">":    return col.Gt
    elif opr == ">=":   return col.Ge
    elif opr == "==":   return col.Eq
    elif opr == "~=":   return col.Ne
    elif opr == "&":    return col.Band
    elif opr == "|":    return col.Bor
    elif opr == "&&":   return col.Land
    elif opr == "||":   return col.Lor


