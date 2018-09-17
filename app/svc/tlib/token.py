"""
    token generator & validator form parameters
"""
import time, hashlib


def generate(params, key):
    """
        add token to params
    :param params: dict
    :param key: str
    :return:
        dict, params with _tm/_token items added
    """
    # current timestamp
    timenow = str(int(time.time()))

    # sorted values
    values = []
    for value in params.values():
        if value is not None:
            values.append(str(value))
    values.sort()

    # value string
    valuestr = ''.join(values)

    # key string
    keystr = valuestr+timenow+key
    print(keystr)

    # generate token
    token = hashlib.sha1(keystr.encode()).hexdigest()

    # create new params
    params['_tm'] = timenow
    params['_token'] = token[20:]

    return params


def validate(params, key):
    """
        check token
    :param params: dict
    :param key: str
    :return:
        True for validate passed, otherwise False
    """
    # get timestamp
    timenow = params['_tm']

    # get token
    token = params['_token']

    # sorted values
    values = []
    for k, v in params.items():
        if k not in ['_tm', '_token']:
            values.append(str(v))
    values.sort()

    # value string
    valuestr = ''.join(values)

    # key string
    keystr = valuestr+timenow+key
    print(keystr)

    # generate token
    ctoken = hashlib.sha1(keystr.encode()).hexdigest()[20:]

    if token == ctoken:
        return True

    return False
