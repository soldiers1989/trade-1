"""
    quote api
"""
import requests
from decimal import Decimal
from  tlib import token

# base url for remote quote service
_BaseUrl = "http://localhost:9000"

# token for access remote trade service
_ENABLE_KEY = True
_PRIVATE_KEY = "abc"


# quote api error
class QuoteApiError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


# current quote summary
class _Quote(dict):
    def __init__(self, **kwargs):
        self.jkj = Decimal(str(kwargs.get("jkj")))
        self.zsj = Decimal(str(kwargs.get("zsj")))
        self.dqj = Decimal(str(kwargs.get("dqj")))
        self.zgj = Decimal(str(kwargs.get("zgj")))
        self.zdj = Decimal(str(kwargs.get("zdj")))
        self.cjl = kwargs.get("cjl")
        self.cje = Decimal(str(kwargs.get("cje")))
        self.ztj = Decimal(str(kwargs.get("ztj")))
        self.dtj = Decimal(str(kwargs.get("dtj")))

        super().__init__(self, **kwargs)


# level 5 quotes
class _Level5(dict):
    def __init__(self, **kwargs):
        self.mrl1 = kwargs.get('mrl1')
        self.mrj1 = Decimal(str(kwargs.get('mrj1')))
        self.mrl2 = kwargs.get('mrl2')
        self.mrj2 = Decimal(str(kwargs.get('mrj2')))
        self.mrl3 = kwargs.get('mrl3')
        self.mrj3 = Decimal(str(kwargs.get('mrj3')))
        self.mrl4 = kwargs.get('mrl4')
        self.mrj4 = Decimal(str(kwargs.get('mrj4')))
        self.mrl5 = kwargs.get('mrl5')
        self.mrj5 = Decimal(str(kwargs.get('mrj5')))
        self.mcl1 = kwargs.get('mcl1')
        self.mcj1 = Decimal(str(kwargs.get('mcj1')))
        self.mcl2 = kwargs.get('mcl1')
        self.mcj2 = Decimal(str(kwargs.get('mcj2')))
        self.mcl3 = kwargs.get('mcl3')
        self.mcj3 = Decimal(str(kwargs.get('mcj3')))
        self.mcl4 = kwargs.get('mcl4')
        self.mcj4 = Decimal(str(kwargs.get('mcj4')))
        self.mcl5 = kwargs.get('mcl5')
        self.mcj5 = Decimal(str(kwargs.get('mcj5')))

        super().__init__(self, **kwargs)


def _make_token(params):
    """
        add token to params
    :param params:
    :return:
    """
    if not _ENABLE_KEY:
        return params

    return token.generate(params, _PRIVATE_KEY)


def get_quote(code):
    """
        get current quote summary of stock by @code
    :param code:
    :return:
    """
    url = _BaseUrl+"/quote"

    params = {
        'code': code
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()
    if resp.get('status') != 0:
        raise QuoteApiError(resp.get('msg'))

    return _Quote(**resp.get('data').get('quote'))


def get_level5(code):
    """
        get current level 5 quote of stock by @code
    :param code: str, stock code
    :return:
    """
    url = _BaseUrl+"/quote"

    params = {
        'code': code
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()
    if resp.get('status') != 0:
        raise QuoteApiError(resp.get('msg'))

    return _Level5(**resp.get('data').get('quote'))
