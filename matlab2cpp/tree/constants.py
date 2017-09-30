"""
Matlab consists of various legal start and end characters depending on context.
This module is a small collection of constants available to ensure that context
is defined correctly.

Attributes:
    e_start (str): characers allowed in expression start
    e_end (str): characers allowed to terminate expression
    l_start (str): characters allowed in list start
    l_end (str): characters allowed to terminate list
    prefixes (str): characters allowed as prefix univery operators
    postfix1 (str): characters allowed as postfix univary operators
    postfix2 (tuple): same as postfix1, but tuple of multi-char operators
    op1 (str): characters allowed as infix operators
    op2 (tuple): same as op1, but tuple of multi-char operators
"""

import string

letters = string.ascii_letters
digits = string.digits

# start and end of expression
e_start = letters + digits + "[({~-+:@.'"
e_end = "%])},;\n"

# start and end of lists
l_start = "[({"
l_end = "]})"

# end of keyword
k_end = " \t(,;\n%"

prefixes = "-+~"
postfix1 = "'"
postfix2 = (".'",)

# operators with one character
op1 = r"^\/*+-:<>&|"

# operators using two characters
op2 = (
    ".^", ".\\", "./", ".*",
    "<=", ">=", "==", "~=",
    "&&", "||")
