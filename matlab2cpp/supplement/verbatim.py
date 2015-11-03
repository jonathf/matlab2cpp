# encoding: utf-8

import re
import matlab2cpp


def set(D, code):

    for key, value in D.items():

        value = "___" + key + '___' + value.replace('\n', '___')
        findterm = r'.*' + re.escape(key) + r'.*'
        code = re.sub(findterm, value, code)

    return code
        
#find nodes that contain verbatim
def get(node):
    nodes = node.flatten()

    D = {}
    for node in nodes:
        if node.cls == "Verbatim":
            D[node.name] = node.value

    return D
            
    
class Vtypes(object):

    def __get__(self, instance, owner):
        return get(instance)

if __name__ == "__main__":
    import doctest
    import matlab2cpp as mc
    doctest.testmod()
