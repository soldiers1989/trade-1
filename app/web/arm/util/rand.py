"""
    random
"""
import time, random


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
