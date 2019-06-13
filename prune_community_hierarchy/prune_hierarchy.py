import networkx as nx

def get_logodds(fname):
    lo_dic = {}
    for i in open(fname):
        cluid, name, lo = i.strip('\n').split('\t')
        lo_dic[cluid] = (name, float(lo))
    return lo_dic

def get_parent_clid(clid_str):
    return ','.join(clid_str.split(',')[:-1])
	
def get_tree_from_cft(df):
    """ return a tree structure (communities) from cft

    df: a pandas data frame with cluster info such as entropy

    """
    T = nx.DiGraph()

    nodes = set()
    n_prop = {}
    for i, row in df.iterrows():
        n = row['clusterId'] 
        prop_dic = dict(row)

        nodes.add(n)
        n_prop[n] = prop_dic
        T.add_node(n, **prop_dic)

    for n in T.nodes():
        p = get_parent_clid(n)
        if p:
            T.add_edge(p, n)

    return T
	
def prune_tomin_threshold(T, lodic, thr=0.001, zthr=10.0, save_zthr=None, categories = ['ind', 'reg'], drop_invalid = True, verbose=False):
    if save_zthr is None:
        save_zthr = zthr
    def split_condition(root, T, lodic):
        children = list(T.successors(root))
        if len(children) == 0:
            return(None)
        split_condition = True
        valid_children_by_cat = {}
        saved_children_by_cat = {}
        for category in categories:
            count_valid = 0
            valid_children_by_cat[category] = set()
            saved_children_by_cat[category] = set()
            for child in children:
                if lodic[category][child][1] > zthr:
                    count_valid += 1
                    valid_children_by_cat[category]  |= {child}
                if lodic[category][child][1] > save_zthr:
                    saved_children_by_cat[category] |= {child}
            prop_valid = count_valid * 1.0/len(children)
            if prop_valid - thr < -10e-10:
                split_condition=False
            if verbose:
                print("%s Proportion Valid %.3f" %(category, prop_valid))
                print(valid_children_by_cat[category])
        if split_condition:
            valid_children = set(children)
            saved_children = set(children)
            for cat, childset in valid_children_by_cat.items():
                valid_children = valid_children & childset
            for cat, childset in saved_children_by_cat.items():
                saved_children = saved_children & childset
            saved_children = saved_children - valid_children
            dropped_children = set(children) - valid_children
            return(valid_children, saved_children, dropped_children)
        else:
            return(None)
    tovisit = ['0']
    kept_list = []
    while len(tovisit) > 0:
        cur_node = tovisit.pop()
        valid_children = split_condition(cur_node, T, lodic)
        if valid_children is None:
            kept_list += [cur_node]
        else:
            tovisit_children = valid_children[0]
            saved_children = valid_children[1]
            dropped_children = valid_children[2]
            if len(tovisit_children) == 0: #and len(saved_children) == 0:
                kept_list += [cur_node]
            else:
                kept_list += list(saved_children)
                if not drop_invalid:
                    kept_list += list(dropped_children)
            tovisit += list(tovisit_children)
    return(kept_list)