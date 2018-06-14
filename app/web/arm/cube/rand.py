"""
    random
"""
import time, random


def uuid():
    """
        generate uuid by time(16) + random(4) = 20
    :return:
    """
    isec, fsec = str(time.time()).split('.')
    return isec + fsec[-6:].zfill(6) + str(random.randint(0, 9999)).zfill(4)
