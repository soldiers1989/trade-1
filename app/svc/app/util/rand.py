import time, random



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


def vcode(t, l):
    """
        random verify code
    :param t: str, type, n-number, s-alpha string, ns-number/alpha string
    :param l: int, length
    :return:
    """
    if t == 'n':
        code = num(l)
    elif t == 's':
        code = alpha(l)
    elif t == 'ns':
        code = alnum(l)
    else:
        code = None
    return code


def _cbase(num, b):
    """
        return string of num(oct number) with base by (b) string
    :return: str
    """
    return ((num == 0) and "0") or (_cbase(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])


def uuid():
    """

    :return:
    """
    n = random.randint(1000,9999)*10**16 + int(time.time()*10**6)
    return _cbase(n, 36)