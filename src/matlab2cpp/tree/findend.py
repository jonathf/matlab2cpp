"""
Rutines for performing look-aheads to find end character.
"""

import constants as c

def expression(self, start):
    "find end of expresion"

    if  self.code[start] not in c.e_start:
        self.syntaxerror(start, "expression start")
    k = start

    while True:

        if self.code[k] == "(":
            k = paren(self, k)

        elif self.code[k] == "[":
            k = matrix(self, k)

        elif self.code[k] == "'" and self.is_string(k):
            k = string(self, k)

        elif self.code[k] == "{":
            k = cell(self, k)

        elif self.code[k:k+3] == "...":
            k = dots(self, k)

        elif self.code[k] == "=":

            if self.code[k+1] == "=":
                k += 1
            else:
                break

        elif self.code[k] in "><~":

            if self.code[k+1] == "=":
                k += 1

        elif self.code[k:k+3] == "...":
            k = dots(self, k)

        elif self.code[k] in c.e_end:
            break

        k += 1

    k -= 1
    while self.code[k] in " \t":
        k -= 1

    return k


def expresion_space(self, start):
    "find end of expression in a space separated list"

    if  self.code[start] not in c.e_start:
        self.syntaxerror(start, "expression start")
    k = last = start

    while True:

        if self.code[k] == "(":
            k = last = paren(self, k)

        elif self.code[k] == "[":
            k = last = matrix(self, k)

        elif self.code[k] == "'":
            if self.is_string(k):
                k = last = string(self, k)
            else:
                last = k

        elif self.code[k] == "{":
            k = last = cell(self, k)

        elif self.code[k:k+3] == "...":
            k = dots(self, k)

        elif self.code[k] == ";":
            return last

        elif self.code[k] == "=":

            if self.code[k+1] == "=":
                k += 1
            else:
                return last

        elif self.code[k] in "><~":

            if self.code[k+1] == "=":
                k += 1

        elif self.code[k] in "+-":
            while self.code[k+1] in " \t":
                k += 1

        elif self.code[k] in " \t":

            if self.is_space_delimiter(k):
                return last
            while self.code[k+1] in " \t+-~":
                k += 1

        elif self.code[k] in c.e_end:
            return last

        elif self.code[k] in c.letters + c.digits + "_@":
            while self.code[k+1] in c.letters + c.digits + "_@":
                k += 1
            last = k

        k += 1


def matrix(self, start):
    "find index to end of matrix"

    if  self.code[start] != "[":
        self.syntaxerror(start, "matrix start ([)")

    k = start+1

    if self.is_space_delimited(start):

        # Ignore first string occurence
        while self.code[k] in " \t":
            k += 1
        if self.code[k] == "'":
            k = string(self, k)+1

        while True:

            if self.code[k] == "[":
                k = matrix(self, k)

            elif self.code[k] == "]":
                return k

            elif self.code[k] == "%":
                k = comment(self, k)

            elif self.code[k] == "'" and self.code[k-1] in c.s_start:
                k = string(self, k)

            k += 1

    else:
        while True:

            if self.code[k] == "[":
                k = matrix(self, k)

            elif self.code[k] == "]":
                return k

            elif self.code[k] == "%":
                k = comment(self, k)

            elif self.code[k] == "'" and self.is_string(k):
                k = string(self, k)

            k += 1


def string(self, start):
    "find end of string"

    if self.code[start] != "'":
        self.syntaxerror(start, "start of string (')")

    k = self.code.find("'", start+1)
    if k == -1:
        self.syntaxerror(start, "matching end of string (')")

#          while self.code[k-1] == "\\" and self.code[k-2] != "\\":
#              k = self.code.find("'", k+1)
#              assert k != -1

    if self.code.find("\n", start, k) != -1:
        self.syntaxerror(start, "non line-feed character in string")

    return k


def comment(self, start):
    "find index to end of comment"

    if self.code[start] != "%":
        self.syntaxerror(start, "comment start")

    # blockcomment
    if self.code[start+1] == "{":
        eoc = self.code.find("%}", start+2)

        if eoc <= -1:
            self.syntaxerror(start, "matching end of comment block (%})")

        return eoc+1

    # Linecomment
    eoc = self.code.find("\n", start)
    if eoc <= -1:
        self.syntaxerror(start, "comment end")
    return eoc


def dots(self, start):
    "find end of multi-line initiator"

    if self.code[start:start+3] != "...":
        self.syntaxerror(start, "three dots (...)")

    k = self.code.find("\n", start)
    if k == -1:
        self.syntaxerror(start, "next line feed character")

    return k


def paren(self, start):
    "find matching parenthesis"

    if self.code[start] != "(":
        self.syntaxerror(start, "start parenthesis")

    k = start+1
    while True:

        if self.code[k] == "%":
            self.syntaxerror(k, "no comments in parenthesis")

        elif self.code[k:k+3] == "...":
            k = dots(self, k)

        elif self.code[k] == "'" and self.is_string(k):
            k = string(self, k)

        elif self.code[k] == "[":
            k = matrix(self, k)

        elif self.code[k] == "(":
            k = paren(self, k)

        elif self.code[k] == ")":
            return k

        k += 1


def cell(self, start):
    "find matching curly parenthesis"
    if  self.code[start] != "{":
        self.syntaxerror(start, "start of cell ({)")

    k = start
    while True:

        if self.code[k] == "%":
            self.syntaxerror(k, "no comment in cell group")

        elif self.code[k] == "'" and self.is_string(k):
            k = string(self, k)
        elif self.code[k] == "(":
            k = paren(self, k)
        elif self.code[k] == "[":
            k = matrix(self, k)
        elif self.code[k] == "}":
            l = k+1
            while self.code[l] in " \t":
                l += 1
            if self.code[l] != "{":
                return k
            k = l

        k += 1
