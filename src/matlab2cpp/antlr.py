#!/usr/bin/env python

import os
os.system("java -jar /usr/local/lib/antlr-4.5-complete.jar -Dlanguage=Python2 Matlab.g4")
os.system("cp MatlabListener.py.bak MatlabListener.py")
