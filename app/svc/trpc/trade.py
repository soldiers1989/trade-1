"""
    trade api
"""
import requests, datetime
from decimal import Decimal
from tlib import token

# base url for remote trade service
_BaseUrl = "http://localhost:9000"

# token for access remote trade service
_ENABLE_KEY = True
_PRIVATE_KEY = "abc"

# quote api error
class TradeApiError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


# 当前资产查询
class _Dqzc(dict):
    def __init__(self, **kwargs):
        self.zzc = Decimal(kwargs.get('zzc'))
        self.zjye = Decimal(kwargs.get('zjye'))
        self.kyzj = Decimal(kwargs.get('kyzj'))
        self.kqzj = Decimal(kwargs.get('kqzj'))
        super().__init__(self, **kwargs)


# 当前持仓查询
class _Dqcc(dict):
    def __init__(self, **kwargs):
        self.zqdm = kwargs.get('zqdm')
        self.zqmc = kwargs.get('zqmc')
        self.zqsl = int(kwargs.get('zqsl'))
        self.kmsl = int(kwargs.get('kmsl'))
        super().__init__(self, **kwargs)

# 当日委托查询
class _Drwt(dict):
    def __init__(self, **kwargs):
        self.wtrq = datetime.datetime.strptime(kwargs.get('wtrq'), '%Y%m%d').date()
        self.wtsj = datetime.datetime.strptime(kwargs.get('wtsj'), '%H:%M:%S').time()
        self.gddm = kwargs.get('gddm')
        self.zqdm = kwargs.get('zqdm')
        self.zqmc = kwargs.get('zqmc')
        self.mmbz = kwargs.get('mmbz')
        self.wtjg = Decimal(kwargs.get('wtjg'))
        self.wtsj = int(kwargs.get('wtsl'))
        self.wtbh = kwargs.get('wtbh')
        self.cjsl = int(kwargs.get('cjsl'))
        self.cjjg = Decimal(kwargs.get('cjjg'))
        self.cjje = Decimal(kwargs.get('cjje'))
        self.cdsl = int(kwargs.get('cdsl'))
        self.cdbz = kwargs.get('cdbz')
        self.ztsm = kwargs.get('ztsm')
        super().__init__(self, **kwargs)

# 当日成交查询
class _Drcj(dict):
    def __init__(self, **kwargs):
        self.cjrq = datetime.datetime.strptime(kwargs.get("cjrq"), '%Y%m%d').date()
        self.cjsj = datetime.datetime.strptime(kwargs.get("cjsj"), '%H:%M:%S').time()
        self.gddm = kwargs.get("gddm")
        self.zqdm = kwargs.get("zqdm")
        self.zqmc = kwargs.get("zqmc")
        self.mmbz = kwargs.get("mmbz")
        self.wtjg = Decimal(kwargs.get("wtjg"))
        self.wtsl = int(kwargs.get("wtsl"))
        self.wtbh = kwargs.get("wtbh")
        self.cjsl = int(kwargs.get("cjsl"))
        self.cjjg = Decimal(kwargs.get("cjjg"))
        self.cjje = Decimal(kwargs.get("cjje"))
        self.cjbh = kwargs.get("cjbh")
        self.cdbz = kwargs.get("cdbz")
        self.ztsm = kwargs.get("ztsm")
        super().__init__(self, **kwargs)


# 可撤委托查询
class _Kcwt(dict):
    def __init__(self, **kwargs):
        self.wtrq = datetime.datetime.strptime(kwargs.get('wtrq'), '%Y%m%d').date()
        self.wtsj = datetime.datetime.strptime(kwargs.get('wtsj'), '%H:%M:%S').time()
        self.gddm = kwargs.get('gddm')
        self.zqdm = kwargs.get('zqdm')
        self.zqmc = kwargs.get('zqmc')
        self.wtjg = Decimal(kwargs.get('wtjg'))
        self.wtsj = int(kwargs.get('wtsl'))
        self.wtbh = kwargs.get('wtbh')
        self.cjsl = int(kwargs.get('cjsl'))
        self.cdsl = int(kwargs.get('cdsl'))
        self.ztsm = kwargs.get("ztsm")
        super().__init__(self, **kwargs)


# 股东信息查询
class _Gdxx(dict):
    def __init__(self, **kwargs):
        self.gddm = kwargs.get('gddm')
        self.gdmc = kwargs.get('gdmc')
        self.zjzh = kwargs.get('zjzh')
        self.gdlx = kwargs.get('gdlx')
        super().__init__(self, **kwargs)


# 历史委托查询
class _Lswt(dict):
    def __init__(self, **kwargs):
        self.wtrq = datetime.datetime.strptime(kwargs.get('wtrq'), '%Y%m%d').date()
        self.wtsj = datetime.datetime.strptime(kwargs.get('wtsj'), '%H:%M:%S').time()
        self.gddm = kwargs.get('gddm')
        self.zqdm = kwargs.get('zqdm')
        self.zqmc = kwargs.get('zqmc')
        self.mmbz = kwargs.get('mmbz')
        self.wtjg = Decimal(kwargs.get('wtjg'))
        self.wtsj = int(kwargs.get('wtsl'))
        self.wtbh = kwargs.get('wtbh')
        self.cjsl = int(kwargs.get('cjsl'))
        self.cjjg = Decimal(kwargs.get('cjjg'))
        self.cjje = Decimal(kwargs.get('cjje'))
        self.cdsl = int(kwargs.get('cdsl'))
        self.ztsm = kwargs.get('ztsm')
        super().__init__(self, **kwargs)


# 历史成交查询
class _Lscj(dict):
    def __init__(self, **kwargs):
        self.cjrq = datetime.datetime.strptime(kwargs.get("cjrq"), '%Y%m%d').date()
        self.cjsj = datetime.datetime.strptime(kwargs.get("cjsj"), '%H:%M:%S').time()
        self.gddm = kwargs.get("gddm")
        self.zqdm = kwargs.get("zqdm")
        self.zqmc = kwargs.get("zqmc")
        self.mmbz = kwargs.get("mmbz")
        self.wtjg = Decimal(kwargs.get("wtjg"))
        self.wtsl = int(kwargs.get("wtsl"))
        self.wtbh = kwargs.get("wtbh")
        self.cjsl = int(kwargs.get("cjsl"))
        self.cjjg = Decimal(kwargs.get("cjjg"))
        self.cjje = Decimal(kwargs.get("cjje"))
        self.cjbh = kwargs.get("cjbh")
        super().__init__(self, **kwargs)


# 交割单查询
class _Jgd(dict):
    def __init__(self, **kwargs):
        self.cjrq = datetime.datetime.strptime(kwargs.get("cjrq"), '%Y%m%d').date()
        self.cjsj = datetime.datetime.strptime(kwargs.get("cjsj"), '%H:%M:%S').time()
        self.gddm = kwargs.get("gddm")
        self.zqdm = kwargs.get("zqdm")
        self.zqmc = kwargs.get("zqmc")
        self.mmbz = kwargs.get("mmbz")
        self.wtjg = Decimal(kwargs.get("wtjg"))
        self.wtsl = int(kwargs.get("wtsl"))
        self.wtbh = kwargs.get("wtbh")
        self.cjsl = int(kwargs.get("cjsl"))
        self.cjjg = Decimal(kwargs.get("cjjg"))
        self.cjje = Decimal(kwargs.get("cjje"))
        self.cjbh = kwargs.get("cjbh")
        self.yj = Decimal(kwargs.get('yj', '0.00'))
        self.yhs = Decimal(kwargs.get('yhs'))
        self.ghf = Decimal(kwargs.get('ghf'))
        self.jygf = Decimal(kwargs.get('jygf'))
        self.qtfy = Decimal(kwargs.get('qtfy'))
        super().__init__(self, **kwargs)


# 股票行情查询
class _Gphq:
    def __init__(self, **kwargs):
        self.zqdm = kwargs.get("zqdm")
        self.zqmc = kwargs.get("zqmc")
        self.jkj = Decimal(str(kwargs.get("jkj")))
        self.zsj = Decimal(str(kwargs.get("zsj")))
        self.dqj = Decimal(str(kwargs.get("dqj")))
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


# 限价买入
class _Xjmr:
    def __init__(self, **kwargs):
        self.wtbh = kwargs.get('wtbh')
        super().__init__(self, **kwargs)


# 限价卖出
class _Xjmc:
    def __init__(self, **kwargs):
        self.wtbh = kwargs.get('wtbh')
        super().__init__(self, **kwargs)


# 市价买入
class _Sjmr:
    def __init__(self, **kwargs):
        self.wtbh = kwargs.get('wtbh')
        super().__init__(self, **kwargs)


# 市价卖出
class _Sjmc:
    def __init__(self, **kwargs):
        self.wtbh = kwargs.get('wtbh')
        super().__init__(self, **kwargs)


# 委托撤单
class _Wtcd:
    def __init__(self, **kwargs):
        self.fhxx = kwargs.get('fhxx')
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


def add_account(laccount, lpwd, taccount, tpwd, dept, version, agentservers, tradeservers):
    """
        添加股票账户
    :param laccount:
    :param lpwd:
    :param taccount:
    :param tpwd:
    :param dept:
    :param version:
    :param agentservers:
    :param tradeservers:
    :return:
    """
    url = _BaseUrl+"/account/add"

    agentlst = []
    for agents in agentservers:
        agents = [str(agents[0]), str(agents[1]), str(agents[2])]
        agentlst.append((',').join(agents))
    sagentservers = '|'.join(agentlst)

    tradeslst = []
    for trades in tradeservers:
        trades = [str(trades[0]), str(trades[1]), str(trades[2])]
        tradeslst.append((',').join(trades))
    stradeservers = '|'.join(tradeslst)

    params = {
        'laccount': laccount,
        'lpwd': lpwd,
        'taccount': taccount,
        'tpwd': tpwd,
        'dept': dept,
        'version': version,
        'agents': sagentservers,
        'trades': stradeservers,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise TradeApiError(resp.get('msg'))


def delete_account(account):
    """
        删除股票账户
    :param account:
    :return:
    """
    url = _BaseUrl+"/account/add"

    params = {
        'account': account,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise TradeApiError(resp.get('msg'))


def clear_account():
    """
        清除所有股票账户
    :return:
    """
    url = _BaseUrl+"/account/clear"

    params = {
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise TradeApiError(resp.get('msg'))


def login_account(account):
    """
        股票账户登录
    :param account:
    :return:
    """
    url = _BaseUrl+"/account/login"

    params = {
        'account': account
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise TradeApiError(resp.get('msg'))


def logout_account(account):
    """
        股票账户登出
    :param account:
    :return:
    """
    url = _BaseUrl+"/account/logout"

    params = {
        'account': account,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise TradeApiError(resp.get('msg'))


def status_account(account):
    """
        股票账户交易通道状态
    :param account:
    :return:
        通道状态信息
    """
    url = _BaseUrl+"/account/status"

    params = {
        'account': account,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise TradeApiError(resp.get('msg'))


def query_gdxx(account):
    """
        查询股票账户股东信息
    :param account:
    :return:
        股东信息列表
    """
    url = _BaseUrl+"/query/gdxx"

    params = {
        'account': account,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise TradeApiError(resp.get('msg'))

    lstgdxx = []
    for gdxx in resp.data:
        lstgdxx.append(_Gdxx(**gdxx))

    return lstgdxx


def query_dqzc(account):
    """
        查询股票账户当前资产信息
    :param account:
    :return:
        当前资产信息
    """
    url = _BaseUrl+"/query/dqzc"

    params = {
        'account': account,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise TradeApiError(resp.get('msg'))

    return _Dqcc(**resp.data[0])


def query_dqcc(account):
    """
        查询股票账户当前持仓列表
    :param account:
    :return:
        持仓列表
    """
    url = _BaseUrl+"/query/dqcc"

    params = {
        'account': account,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise TradeApiError(resp.get('msg'))

    lstdqcc = []
    for dqcc in resp.data:
        lstdqcc.append(_Dqcc(**dqcc))

    return lstdqcc


def query_drwt(account):
    """
        查询股票账户当日委托列表
    :param account:
    :return:
        委托列表
    """
    url = _BaseUrl+"/query/drwt"

    params = {
        'account': account,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise TradeApiError(resp.get('msg'))

    items = []
    for item in resp.data:
        items.append(_Dqcc(**item))

    return items


def query_drcj(account):
    """
        查询股票账户当日成交列表
    :param account:
    :return:
        成交列表
    """
    url = _BaseUrl+"/query/drcj"

    params = {
        'account': account,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise TradeApiError(resp.get('msg'))

    items = []
    for item in resp.data:
        items.append(_Drcj(**item))

    return items


def query_kcwt(account):
    """
        查询股票账户当日可撤委托列表
    :param account:
    :return:
        委托列表
    """
    url = _BaseUrl+"/query/kcwt"

    params = {
        'account': account,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise TradeApiError(resp.get('msg'))

    items = []
    for item in resp.data:
        items.append(_Kcwt(**item))

    return items


def query_lswt(account):
    """
        查询股票账户历史委托列表
    :param account:
    :return:
        委托列表
    """
    url = _BaseUrl+"/query/lswt"

    params = {
        'account': account,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise TradeApiError(resp.get('msg'))

    items = []
    for item in resp.data:
        items.append(_Lswt(**item))

    return items


def query_lscj(account):
    """
        查询股票账户历史成交列表
    :param account:
    :return:
        成交列表
    """
    url = _BaseUrl+"/query/lscj"

    params = {
        'account': account,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise TradeApiError(resp.get('msg'))

    items = []
    for item in resp.data:
        items.append(_Lscj(**item))

    return items


def query_jgd(account):
    """
        查询股票账户历史交割单信息
    :param account:
    :return:
        交割单信息列表
    """
    url = _BaseUrl+"/query/jgd"

    params = {
        'account': account,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise TradeApiError(resp.get('msg'))

    items = []
    for item in resp.data:
        items.append(_Jgd(**item))

    return items


def query_gphq(account, code):
    """
        查询股票实时行情
    :param account:
    :return:
        行情
    """
    url = _BaseUrl+"/query/gphq"

    params = {
        'account': account,
        'code': code,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise TradeApiError(resp.get('msg'))

    items = []
    for item in resp.data:
        items.append(_Gphq(**item))

    return items


def order_xjmr(account, gddm, code, price, count):
    """
        限价买入
    :param account:
    :param gddm:
    :param code:
    :param price:
    :param count:
    :return:
        委托编号
    """
    url = _BaseUrl+"/order/xjmr"

    params = {
        'account': account,
        'gddm': gddm,
        'code': code,
        'price': price,
        'count': count,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise TradeApiError(resp.get('msg'))

    items = []
    for item in resp.data:
        items.append(_Xjmr(**item))

    return items


def order_xjmc(account, gddm, code, price, count):
    """
        限价卖出
    :param account:
    :param gddm:
    :param code:
    :param price:
    :param count:
    :return:
        委托编号
    """
    url = _BaseUrl+"/order/xjmc"

    params = {
        'account': account,
        'gddm': gddm,
        'code': code,
        'price': price,
        'count': count,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise TradeApiError(resp.get('msg'))

    items = []
    for item in resp.data:
        items.append(_Xjmc(**item))

    return items


def order_sjmr(account, gddm, code, price, count):
    """
        市价买入
    :param account:
    :param gddm:
    :param code:
    :param price:
    :param count:
    :return:
        委托编号
    """
    url = _BaseUrl+"/order/sjmr"

    params = {
        'account': account,
        'gddm': gddm,
        'code': code,
        'price': price,
        'count': count,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise TradeApiError(resp.get('msg'))

    items = []
    for item in resp.data:
        items.append(_Sjmr(**item))

    return items


def order_sjmc(account, gddm, code, price, count):
    """
        市价卖出
    :param account:
    :param gddm:
    :param code:
    :param price:
    :param count:
    :return:
        委托编号
    """
    url = _BaseUrl+"/order/sjmc"

    params = {
        'account': account,
        'gddm': gddm,
        'code': code,
        'price': price,
        'count': count,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise TradeApiError(resp.get('msg'))

    items = []
    for item in resp.data:
        items.append(_Sjmc(**item))

    return items


def order_cancel(account, seid, orderno):
    """
        限价买入
    :param account:
    :param gddm:
    :param code:
    :param price:
    :param count:
    :return:
        委托编号
    """
    url = _BaseUrl+"/order/cancel"

    params = {
        'account': account,
        'seid': seid,
        'orderno': orderno,
    }
    params = _make_token(params)

    resp = requests.get(url, params=params).json()

    if resp.get('status') != 0:
        raise TradeApiError(resp.get('msg'))

    items = []
    for item in resp.data:
        items.append(_Wtcd(**item))

    return items
