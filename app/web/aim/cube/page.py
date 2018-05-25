"""
    page
"""

DEFAULT_PAGE_SIZE = 20

def start(spos, total):
    """

    :param spos:
    :param total:
    :return:
    """
    if spos is None or spos < 0:
        spos = 0
    elif spos >= total:
        spos = total
    elif spos > 0:
        spos = spos - 1;
    else:
        pass

    return spos


def count(count, spos, total):
    """

    :param count:
    :param spos:
    :param total:
    :return:
    """
    if count is None:
        return DEFAULT_PAGE_SIZE

    return count
