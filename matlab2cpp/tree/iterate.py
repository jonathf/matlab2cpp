"""
Rutines for iterating lists

+------------------------------------------------+----------------------+
| Functions                                      | Description          |
+================================================+======================+
| :py:func:`~matlab2cpp.tree.iterate.comma_list` | Iterate over a comma |
|                                                | separated list       |
+------------------------------------------------+----------------------+
| :py:func:`~matlab2cpp.tree.iterate.space_list` | Iterate over a space |
|                                                | delimited list       |
+------------------------------------------------+----------------------+
"""

import constants as c
import findend
import identify


def comma_list(self, start):
    """
Iterate over a comma separated list

Args:
    self (Builder): Code constructor
    start (int): Current position in code

Returns:
    list : A list of 2-tuples that represents index start and end for each
    expression in list
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

            if not count:
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
    list : A list of 2-tuples that represents index start and end for each
    expression in list
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
            
        if self.code[k] in ";\n":
            out.append([])
            count = False
            if self.code[k] == ";": # and self.code[k+1] == "\n":
                while self.code[k] != "\n":
                    k += 1

        if self.code[k] in c.e_start:

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
