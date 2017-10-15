import re
set_ = set

def set(D, code):

    for key, value in D.items():

        findterm = r'.*' + re.escape(key) + r'.*'
        keys = set_(re.findall(findterm, code))

        value = '___' + value.replace('\n', '___')
        value = value.replace('\\', '//')

        for key_ in keys:
            findterm_ = re.escape(key_)
            value_ = "___" + key_ + value
            code = re.sub(findterm_, value_, code)

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
