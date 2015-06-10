#!/usr/bin/env python
# encoding: utf8

import matlab2cpp

if __name__ == "__main__":

    parser = matlab2cpp.create_parser()
    args = parser.parse_args()
    matlab2cpp.main(args)

