

def flatten(node, ordered=False):
    """
Return a list of all nodes

Parameters
----------
node : Node
    Root node to start from
ordered : bool
    If True, make sure the nodes are hierarcically ordered.
    If False, nodes are sorted for easy print.
    """

    if ordered:
        def _f(nod):
            out = [nod]
            for n in nod:
                out.extend(_f(n))
            return out
        return _f(node)

    nodes = [node]
    for child in nodes:
        nodes.extend(child.children)
    return nodes


def set_cfg(root, cfg):

    for name in cfg.keys():
        if name in root["names"]:
            cfg_ = cfg[name]
            func = root[root["names"].index(name)+1]
            declares, returns, params = func[0], func[1], func[2]
            for key in cfg_.keys():
                if key in declares["names"]:
                    var = declares[declares["names"].index(key)]
                    var.type(cfg_[key])
                if key in params["names"]:
                    var = params[params["names"].index(key)]
                    var.type(cfg_[key])
                if key in returns["names"]:
                    var = returns[returns["names"].index(key)]
                    var.type(cfg_[key])


def get_cfg(root):
    "Retrieve datatype and suggestions from tokentree"
    cfg = {}
    scfg = {}
    for func in root[1:]:

        cfg[func["name"]] = cfg_ = {}
        scfg[func["name"]] = scfg_ = {}

        declares, params = func[0], func[2]
        for var in declares[:]+params[:]:
            type = var.type()
            if type == "TYPE":
                type = ""
            cfg_[var["name"]] = type
            if not type:
                type = var.suggest()
                if type == "TYPE":
                    type = ""
                if type:
                    scfg_[var["name"]] = type

    return cfg, scfg



def str_cfg(cfg, scfg={}):

    out = "scope = {}\n\n"

    for name in cfg.keys():
        out += '%s = scope["%s"] = {}\n' % (name, name)
        cfg_ = cfg[name]

        for key, val in cfg_.items():
            if val:
                out += '%s["%s"] = "%s"\n' % (name, key, val)
            else:
                suggest = scfg.get(name, {}).get(key, "")
                if suggest:
                    out += '%s["%s"] = "" # %s\n' % (name, key, suggest)
                else:
                    out += '%s["%s"] = ""\n' % (name, key)
        out += "\n"

    return out



