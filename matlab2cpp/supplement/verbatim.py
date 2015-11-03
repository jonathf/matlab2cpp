import re
import matlab2cpp

# in: code, D is dictionary, returns modified code
def set(D, code):
    for key, value in D.items():
        value = '_' + value.replace('\n', '\n_')
        findterm = r'.*' + re.escape(key) + r'.*'
        code = re.sub(findterm, value, code)

    print code

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
