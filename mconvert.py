#!/usr/bin/env python
# encoding: utf8

"""
The frontend of the Matlab2cpp program is the `mconvert` script.
Most operations for performing a translation can be handled from it.
"""

import matlab2cpp

parser = matlab2cpp.create_parser()

if __name__ == "__main__":
    args = parser.parse_args()
    matlab2cpp.main(args)

