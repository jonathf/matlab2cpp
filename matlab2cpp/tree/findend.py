"""
Look-ahead routines to find end character.

+------------------------------------------------------+------------------------+
| Function                                             | Description            |
+======================================================+========================+
| :py:func:`~matlab2cpp.tree.findend.expression`       | Find end of expression |
|                                                      | (non-space delimited)  |
+------------------------------------------------------+------------------------+
| :py:func:`~matlab2cpp.tree.findend.expression_space` | Find end of expression |
|                                                      | (space delimited)      |
+------------------------------------------------------+------------------------+
| :py:func:`~matlab2cpp.tree.findend.matrix`           | Find end of matrix     |
|                                                      | construction           |
+------------------------------------------------------+------------------------+
| :py:func:`~matlab2cpp.tree.findend.string`           | Find end of string     |
+------------------------------------------------------+------------------------+
| :py:func:`~matlab2cpp.tree.findend.comment`          | Find end of comment    |
+------------------------------------------------------+------------------------+
| :py:func:`~matlab2cpp.tree.findend.dots`             | Find continuation      |
|                                                      | after ellipse          |
+------------------------------------------------------+------------------------+
| :py:func:`~matlab2cpp.tree.findend.paren`            | Find matching          |
|                                                      | parenthesis            |
+------------------------------------------------------+------------------------+
| :py:func:`~matlab2cpp.tree.findend.cell`             | Find matching          |
|                                                      | cell-parenthesis       |
+------------------------------------------------------+------------------------+
"""
import matlab2cpp as mc


def expression(self, start):
    """
    Find end of expression (non-space delimited)

Args:
self (Builder): Code constructor
start (int): current position in code

Returns:
int: index location of end of expression
    """

    if  self.code[start] not in mc.tree.constants.e_start:
        self.syntaxerror(start, "expression start")
    k = start

    while True:

        if self.code[k] == "(":
            k = paren(self, k)
            #k += 1
            #break


        elif self.code[k] == "[":
            k = matrix(self, k)

        elif self.code[k] == "'" and mc.tree.identify.string(self, k):
            k = string(self, k)

        elif self.code[k] == "{":
            k = cell(self, k)

        #elif self.code[k:k+3] == "...":
        #    k = dots(self, k)

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

        elif self.code[k] in mc.tree.constants.e_end:
            break

        k += 1

    k -= 1
    while self.code[k] in " \t":
        k -= 1

    return k


def expression_space(self, start):
    """
    Find end of expression (space delimited)

Args:
self (Builder): Code constructor
start (int): current position in code

Returns:
int: index location of end of expression
    """

    if  self.code[start] not in mc.tree.constants.e_start:
        self.syntaxerror(start, "expression start")
    k = last = start

    while True:

        if self.code[k] == "(":
            k = last = paren(self, k)

        elif self.code[k] == "[":
            k = last = matrix(self, k)

        elif self.code[k] == "'":
            if mc.tree.identify.string(self, k):
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

            if mc.tree.identify.space_delimiter(self, k):
                return last
            while self.code[k+1] in " \t+-~":
                k += 1

        elif self.code[k] in mc.tree.constants.e_end:
            return last

        elif self.code[k] in mc.tree.constants.letters + mc.tree.constants.digits + "_@":
            while self.code[k+1] in mc.tree.constants.letters + mc.tree.constants.digits + "_@":
                k += 1
            last = k

        k += 1


def matrix(self, start):
    """
    Find end of matrix construction

Args:
self (Builder): Code constructor
start (int): current position in code

Returns:
int: index location of end of matrix
    """

    if  self.code[start] != "[":
        self.syntaxerror(start, "matrix start ([)")

    k = start+1

    if mc.tree.identify.space_delimited(self, start):

        # Ignore first string occurrence
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

            elif self.code[k] == "'" and mc.tree.identify.string(self, k): #and self.code[k-1] in mc.tree.constants.s_start:
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

            elif self.code[k] == "'" and mc.tree.identify.string(self, k):
                k = string(self, k)

            k += 1


def string(self, start):
    """
Find end of string

Args:
    self (Builder): Code constructor
    start (int): current position in code

Returns:
	int: index location of end of string
    """

    if self.code[start] != "'":
        self.syntaxerror(start, "start of string (')")

    k = self.code.find("'", start+1)
    if k == -1:
        self.syntaxerror(start, "matching end of string (')")

    if self.code.find("\n", start, k) != -1:
        self.syntaxerror(start, "non line-feed character in string")

    return k

def pragma_for(self,start):
    end = self.code.find("\n", start)
    #while self.code[end+1] == "%"
    #    end = self.code.find("\n", start+1)

    if end <= -1:
        self.syntaxerror(start, "comment end")
    return end

def tbb_for(self, start):
    end = self.code.find("\n", start)

    if end <= -1:
        self.syntaxerror(start, "command end")

    return end

def comment(self, start):
    """
Find end of comment

Args:
    self (Builder): Code constructor
    start (int): current position in code

Returns:
	int: index location of end of comment
    """

    if self.code[start] != "%":
        self.syntaxerror(start, "comment start")

    # block comment
    if self.code[start+1] == "{":
        eoc = self.code.find("%}", start+2)

        if eoc <= -1:
            self.syntaxerror(start, "matching end of comment block (%})")

        return eoc+1

    # Line comment
    eoc = self.code.find("\n", start)
    if eoc <= -1:
        self.syntaxerror(start, "comment end")
    return eoc

#should find the end of verbatim area
def verbatim(self, start):
    """
Find end of verbatim

Arg:
   self(Builder): Code constructor
   start (int): current position in code

Returns:
   int: index location of end of verbatim
     """

    if self.code[start:start+3] != "___":
        self.syntaxerror(start, "verbatim start")
    return self.code.find("\n", start)-1


def dots(self, start):
    """
Find continuation of expression after ellipse

Args:
    self (Builder): Code constructor
    start (int): current position in code

Returns:
	int: index location of end of ellipse
    """

    if self.code[start:start+3] != "...":
        self.syntaxerror(start, "three dots (...)")

    k = self.code.find("\n", start)
    if k == -1:
        self.syntaxerror(start, "next line feed character")

    return k


def paren(self, start):
    """
Find matching parenthesis

Args:
    self (Builder): Code constructor
    start (int): current position in code

Returns:
	int: index location of matching parenthesis
    """

    if self.code[start] != "(":
        self.syntaxerror(start, "start parenthesis")

    k = start+1
    while True:

        if self.code[k] == "%":
            self.syntaxerror(k, "no comments in parenthesis")

        elif self.code[k:k+3] == "...":
            k = dots(self, k)

        elif self.code[k] == "'" and mc.tree.identify.string(self, k):
            k = string(self, k)

        elif self.code[k] == "[":
            k = matrix(self, k)

        elif self.code[k] == "(":
            k = paren(self, k)

        elif self.code[k] == ")":
            return k

        k += 1


def cell(self, start):
    """
Find matching cell-parenthesis

Args:
    self (Builder): Code constructor
    start (int): current position in code

Returns:
	int: index location of matching cell-parenthesis
    """

    if  self.code[start] != "{":
        self.syntaxerror(start, "start of cell ({)")

    k = start
    while True:

        if self.code[k] == "%":
            self.syntaxerror(k, "no comment in cell group")

        elif self.code[k] == "'" and mc.tree.identify.string(self, k):
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
