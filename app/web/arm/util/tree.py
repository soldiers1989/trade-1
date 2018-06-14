"""
    make tree
"""


def make(items, parent=None, kid='id', kpid='parent', kchilds='children'):
    """
     make a tree by input item list
    :param items:
    :param parent:
    :param kid:
    :param kpid:
    :param kchilds:
    :return:
    """
    # find child notes of parent
    nodes = []
    for item in items:
        if item[kpid] == parent:
            childs = make(items, item[kid])
            if len(childs) > 0:
                item[kchilds] = childs
            nodes.append(item)

    return nodes


def parents(child, nodes, kid='id', kpid='parent'):
    """
        get child's parent node list
    :param child:
    :param nodes:
    :param kid:
    :param kpid:
    :return:
    """
    prnts = []
    if child is None:
        return prnts

    for node in nodes:
        if node[kid] == child[kpid]:
            # add current parent
            prnts.append(node)
            # add parent's parents
            sparents = parents(node, nodes, kid, kpid)
            if len(sparents) > 0:
                prnts.extend(sparents)

    return prnts


def childs(parent, nodes, kid='id', kpid='parent'):
    """
        get parent's child node list
    :param parent:
    :param nodes:
    :param kid:
    :param kpid:
    :return:
    """
    clds = []

    for node in nodes:
        if node[kpid] == parent[kid]:
            # add current child
            clds.append(node)
            # add child's childs
            schilds = childs(node, nodes, kid, kpid)
            if len(schilds) > 0:
                clds.append(schilds)

    return clds


def parentids(child, nodes, kid='id', kpid='parent'):
    """
        get parent node id list
    :param child:
    :param nodes:
    :param kid:
    :param kpid:
    :return:
    """
    ids = []

    prnts = parents(child, nodes, kid, kpid)
    for prnt in prnts:
        ids.append(prnt[kid])

    return ids


def childids(parent, nodes, kid='id', kpid='parent'):
    """
        get child node id list
    :param parent:
    :param nodes:
    :param kid:
    :param kpid:
    :return:
    """
    ids = []

    clds = childs(parent, nodes, kid, kpid)
    for cld in clds:
        ids.append(cld[kid])

    return ids


def isleaf(node, nodes, kid='id', kpid='parent'):
    """
        check if given node is leaf node
    :param id:
    :param nodes:
    :param kpid:
    :return:
    """
    id = node
    if isinstance(node, dict):
        id = node[kid]

    for nd in nodes:
        if nd[kpid] == id:
            return False

    return True