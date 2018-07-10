import random



def num(nlen):
    """
        generate random numbers
    :param nlen:
    :return:
    """
    return str(random.randint(10**(nlen-1), 10**nlen-1))


def alpha(nlen):
    """
        generate random alpha strings
    :param nlen:
    :return:
    """
    s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    rs = ''
    for i in range(nlen):
        rs += s[random.randint(0, len(s)-1)]

    return rs


def alnum(nlen):
    """
        generate random alpha/number s
    :param nlen:
    :return:
    """
    s = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    rs = ''
    for i in range(nlen):
        rs += s[random.randint(0, len(s)-1)]

    return rs