"""
Rutines for iterating lists

Functions
~~~~~~~~~
list        Iterate over a list
comma_list  Iterate over a comma separated list
space_list  Iterate over a space delimited list
"""

import constants as c
import findend
import identify


def list(self, start):
    """
Iterate over a list

Args:
    self (Builder): Code constructor
    start (int): Current position in code

Returns:
	list : A list of 2-tuples that represents index start and end for each expression in list
    """

    if identify.space_delimited(self, start):
        return space_list(self, start)
    return comma_list(self, start)


def comma_list(self, start):
    """
Iterate over a comma separated list

Args:
    self (Builder): Code constructor
    start (int): Current position in code

Returns:
	list : A list of 2-tuples that represents index start and end for each expression in list
    """

    if  self.code[start] not in c.l_start:
        self.syntaxerror(start, "list start")
    k = start+1

    while self.code[k] in " \t":
        k += 1

    if self.code[k] in "]}":
        return [[]]

    out = [[]]
    count = False

    while True:

        if self.code[k:k+3] == "...":
            k = findend.dots(self, k)

        elif self.code[k] in c.e_start:

            if count:
                self.syntaxerror(k, "comma list indicator")

            count = True
            end = findend.expression(self, k)
            out[-1].append((k, end))

            k = end

        elif self.code[k] == ",":

            if not count:
                self.syntaxerror(k, "comma list indicator")

            count = False

        elif self.code[k] == ";":

            if  count:
                self.syntaxerror(k, "comma list indicator")

            count = False
            out.append([])

        elif self.code[k] in c.l_end:
            return out

        k += 1



def space_list(self, start):
    """
Iterate over a space delimited list

Args:
    self (Builder): Code constructor
    start (int): Current position in code

Returns:
	list : A list of 2-tuples that represents index start and end for each expression in list
    """

    if  self.code[start] not in c.l_start:
        self.syntaxerror(start, "start of list")

    k = start+1
    while self.code[k] in " \t":
        k += 1

    out = [[]]
    count = False

    while True:

        if self.code[k:k+3] == "...":
            k = findend.dots(self, k)

        elif self.code[k] in ";\n":
            out.append([])

        elif self.code[k] in c.e_start:

            if count:
                self.syntaxerror(k, "expression start")

            count = True

            end = findend.expression_space(self, k)
            out[-1].append((k, end))
            k = end

        elif self.code[k] in c.l_end:
            return out

        elif self.code[k] in " \t":
            count = False

        k += 1
