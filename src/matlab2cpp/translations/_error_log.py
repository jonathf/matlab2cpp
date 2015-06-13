"""
Documenting errors and warning in log file
"""

import time
from datetime import datetime as date

def Errors(node):
    if not node.children:
        return ""
    ts = time.time()
    log = "Translated on " +\
            date.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S\n\n')
    return log, "\n\n", ""

def Error(node):
    return '''Error [%(line)d,%(cur)d]: %(value)s in %(cls)s
"%(code)s"'''

def Warning(node):
    return '''Warning [%(line)d,%(cur)d]: %(value)s in %(cls)s
"%(code)s"'''

Project = ""
