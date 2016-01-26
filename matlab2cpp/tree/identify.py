"""
Rutines for identifying code structure.

+------------------------------------------------------+-----------------------+
| Function                                             | Description           |
+======================================================+=======================+
| :py:func:`~matlab2cpp.tree.identify.space_delimiter` | Check if at expression|
|                                                      | space-delimiter       |
+------------------------------------------------------+-----------------------+
| :py:func:`~matlab2cpp.tree.identify.string`          | Check if at string    |
|                                                      | start                 |
+------------------------------------------------------+-----------------------+
| :py:func:`~matlab2cpp.tree.identify.space_delimited` | Check if list is      |
|                                                      | space-delimited       |
+------------------------------------------------------+-----------------------+
"""

import constants as c
import findend

def space_delimiter(self, start):
    """
Check if mid-expression space-delimiter. This already assumes that position is
in the middle of a space delimited list. Use `space_delimited` to check if
a list is space or comma delimited.

Args:
    self (Builder): Code constructor
    start (int): Current position in code

Returns:
	bool: True if whitespace character classifies as a delimiter
    """

    if self.code[start] not in " \t":
        self.syntaxerror(start, "space delimiter")

    k = start

    while True:

        if self.code[k:k+3] == "...":
            return False

        elif self.code[k] in " \t":
            pass

        elif self.code[k] in "+-~":
            if self.code[k+1] in " \t":
                return False

        elif self.code[k:k+2] in c.op2:
            return False

        elif self.code[k] in c.op1:
            return False

        else:
            return True

        k += 1


def string(self, k):
    """
Check if at string start

Args:
    self (Builder): Code constructor
    k (int): Current position in code

Returns:
	bool: True if character classifies as start of string.
    """

    if self.code[k] != "'":
        self.syntaxerror(k, "start of string character (')")

    if self.code[k-1] == ".":
        return False

    j = k-1
    while self.code[j] in " \t":
        j -= 1

    if self.code[j] in c.letters+c.digits+")]}_":

        # special cases
        if self.code[j-3:j+1] == "case":
            return True

        return False

    return True


def space_delimited(self, start):
    """
Check if list is space-delimited

Args:
    self (Builder): Code constructor
    start (int): Current position in code

Returns:
	bool: True if list consists of whitespace delimiters
    """

    if  self.code[start] not in c.l_start:
        self.syntaxerror(start, "list start")

    k = start+1
    while self.code[k] in " \t":
        k += 1

    if self.code[k] in c.l_end:
        return False

    if  self.code[k] not in c.e_start:
        self.syntaxerror(k, "expression start")

    if self.code[k] == "'":
        k = findend.string(self, k)+1

        while self.code[k] in " \t":
            k += 1

    while True:

        if self.code[k] == "(":
            k = findend.paren(self, k)

        elif self.code[k] == "[":
            k = findend.matrix(self, k)

        elif self.code[k] == "{":
            k = findend.cell(self, k)

        elif self.code[k] == "'" and string(self, k):
            #k = findend.string(self, k)
            #if self.code[k-1] in c.s_start:
            return True

        elif self.code[k:k+3] == "...":
            k = findend.dots(self, k)

        elif self.code[k] in " \t":
            if space_delimiter(self, k):
                return True
            while self.code[k+1] in " \t":
                k += 1

        elif self.code[k] in c.e_end:
            if self.code[k] == ",":
                return False
            elif self.code[k] in c.l_end:
                return False
            elif self.code[k] != ";":
                return True

            while self.code[k+1] in " \t":
                k += 1

        elif self.code[k+1] in c.letters + c.digits + "_@":
            while self.code[k+1] in c.letters + c.digits + "_@":
                k += 1
        k += 1
