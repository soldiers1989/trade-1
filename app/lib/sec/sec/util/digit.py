"""
    digit
"""

def strbasen(num, b):
    """
        return string of num(oct number) with base by (b) string
    :return: str
    """
    return ((num == 0) and "0") or (strbasen(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])
