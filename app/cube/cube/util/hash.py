"""
    hash method
"""
import hashlib


def md5(str):
    '''
        compute md5 of @str
    :return: string
    '''
    m = hashlib.md5(str.encode())
    return m.hexdigest()



def sha1(str):
    '''
        compute sha1 of @str
    :return: string
    '''
    h = hashlib.sha1(str.encode())
    return h.hexdigest()
