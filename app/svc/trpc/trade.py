"""
    trade api
"""
import requests, datetime
from decimal import Decimal

from . import rpc


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
class _Gphq(dict):
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
class _Xjmr(dict):
    def __init__(self, **kwargs):
        self.wtbh = kwargs.get('wtbh')
        super().__init__(self, **kwargs)


# 限价卖出
class _Xjmc(dict):
    def __init__(self, **kwargs):
        self.wtbh = kwargs.get('wtbh')
        super().__init__(self, **kwargs)


# 市价买入
class _Sjmr(dict):
    def __init__(self, **kwargs):
        self.wtbh = kwargs.get('wtbh')
        super().__init__(self, **kwargs)


# 市价卖出
class _Sjmc(dict):
    def __init__(self, **kwargs):
        self.wtbh = kwargs.get('wtbh')
        super().__init__(self, **kwargs)


# 委托撤单
class _Wtcd(dict):
    def __init__(self, **kwargs):
        self.fhxx = kwargs.get('fhxx')
        super().__init__(self, **kwargs)

_query_cls = {
    'dqzc': _Dqzc,
    'dqcc': _Dqcc,
    'drwt': _Drwt,
    'drcj': _Drcj,
    'kcwt': _Kcwt,
    'gdxx': _Gdxx,
    'lswt':_Lswt,
    'lscj':_Lscj,
    'jgd':_Jgd
}

_order_cls = {
    'buy': {
        'xj': _Xjmr,
        'sj': _Sjmr
    },
    'sell': {
        'xj': _Xjmc,
        'sj': _Sjmc
    }
}


class TradeRpc(rpc.Rpc):
    def __init__(self, baseurl:str, key:str, safety:bool):
        """
            init rpc
        :param baseurl: str, base url for remote http service
        :param key: str, private key for safety verification or None
        :param safety: bool, enable safety key verification with True
        """
        super().__init__(baseurl, key, safety)

    def add_account(self, acnt:dict):
        """
            添加股票账户
        :return:
        """
        url = self.baseurl+"/account/add"

        params = {
        }
        params = self.make_token(params)

        resp = requests.post(url, params=params, json=acnt).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

    def delete_account(self, account):
        """
            删除股票账户
        :param account:
        :return:
        """
        url = self.baseurl+"/account/add"

        params = {
            'account': account,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

    def clear_account(self):
        """
            清除所有股票账户
        :return:
        """
        url = self.baseurl+"/account/clear"

        params = {
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

    def login_account(self, account):
        """
            股票账户登录
        :param account:
        :return:
        """
        url = self.baseurl+"/account/login"

        params = {
            'account': account
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

    def logout_account(self, account):
        """
            股票账户登出
        :param account:
        :return:
        """
        url = self.baseurl+"/account/logout"

        params = {
            'account': account,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

    def status_account(self, account):
        """
            股票账户交易通道状态
        :param account:
        :return:
            通道状态信息
        """
        url = self.baseurl+"/account/status"

        params = {
            'account': account,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

    def quote(self, account, zqdm):
        """
            查询股票实时行情
        :param account:
        :return:
            行情
        """
        url = self.baseurl+"/quote"

        params = {
            'account': account,
            'zqdm': zqdm,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

        items = []
        for item in resp.data:
            items.append(_Gphq(**item))

        return items

    def query(self, account, type, sdate=None, edate=None):
        """
            查询当前或者历史信息
        :param account:
        :param type: str, 查询类别，dqzc/dqcc/drwt/drcj/kcwt/gdxx/lswt/lscj/jgd
        :param sdate: str, 开始日期，yyyymmdd
        :param edate: str, 结束日期, yyyymmdd
        :return:
            dict/list
        """
        url = self.baseurl+"/query"

        params = {
            'account': account,
            'type': type
        }
        if sdate is not None:
            params['sdate'] = sdate
        if edate is not None:
            params['edate'] = edate
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

        items = []
        for item in resp.data:
            items.append(_query_cls[type](**item))

        return items

    def place(self, account, otype, ptype, zqdm, price, count):
        """
            委托下单
        :param account:
        :param otype:
        :param ptype:
        :param zqdm:
        :param price:
        :param count:
        :return:
            委托编号
        """
        url = self.baseurl+"/place"

        params = {
            'account': account,
            'otype': otype,
            'ptype': ptype,
            'zqdm': zqdm,
            'price': price,
            'count': count,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

        items = []
        for item in resp.data:
            items.append(_Xjmc(**item))

        return items

    def cancel(self, account, zqdm, orderno):
        """
            委托撤单
        :param account:
        :param zqdm:
        :param orderno:
        :return:
        """
        url = self.baseurl+"/cancel"

        params = {
            'account': account,
            'zqdm': zqdm,
            'orderno': orderno,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

        items = []
        for item in resp.data:
            items.append(_Wtcd(**item))

        return items

    def query_gdxx(self, account):
        """
            查询股票账户股东信息
        :param account:
        :return:
            股东信息列表
        """
        url = self.baseurl+"/query/gdxx"

        params = {
            'account': account,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

        lstgdxx = []
        for gdxx in resp.data:
            lstgdxx.append(_Gdxx(**gdxx))

        return lstgdxx

    def query_dqzc(self, account):
        """
            查询股票账户当前资产信息
        :param account:
        :return:
            当前资产信息
        """
        url = self.baseurl+"/query/dqzc"

        params = {
            'account': account,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

        return _Dqcc(**resp.data[0])

    def query_dqcc(self, account):
        """
            查询股票账户当前持仓列表
        :param account:
        :return:
            持仓列表
        """
        url = self.baseurl+"/query/dqcc"

        params = {
            'account': account,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

        lstdqcc = []
        for dqcc in resp.data:
            lstdqcc.append(_Dqcc(**dqcc))

        return lstdqcc

    def query_drwt(self, account):
        """
            查询股票账户当日委托列表
        :param account:
        :return:
            委托列表
        """
        url = self.baseurl+"/query/drwt"

        params = {
            'account': account,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

        items = []
        for item in resp.data:
            items.append(_Drwt(**item))

        return items

    def query_drcj(self, account):
        """
            查询股票账户当日成交列表
        :param account:
        :return:
            成交列表
        """
        url = self.baseurl+"/query/drcj"

        params = {
            'account': account,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

        items = []
        for item in resp.data:
            items.append(_Drcj(**item))

        return items

    def query_kcwt(self, account):
        """
            查询股票账户当日可撤委托列表
        :param account:
        :return:
            委托列表
        """
        url = self.baseurl+"/query/kcwt"

        params = {
            'account': account,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

        items = []
        for item in resp.data:
            items.append(_Kcwt(**item))

        return items

    def query_lswt(self, account):
        """
            查询股票账户历史委托列表
        :param account:
        :return:
            委托列表
        """
        url = self.baseurl+"/query/lswt"

        params = {
            'account': account,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

        items = []
        for item in resp.data:
            items.append(_Lswt(**item))

        return items

    def query_lscj(self, account):
        """
            查询股票账户历史成交列表
        :param account:
        :return:
            成交列表
        """
        url = self.baseurl+"/query/lscj"

        params = {
            'account': account,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

        items = []
        for item in resp.data:
            items.append(_Lscj(**item))

        return items

    def query_jgd(self, account):
        """
            查询股票账户历史交割单信息
        :param account:
        :return:
            交割单信息列表
        """
        url = self.baseurl+"/query/jgd"

        params = {
            'account': account,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

        items = []
        for item in resp.data:
            items.append(_Jgd(**item))

        return items

    def query_gphq(self, account, zqdm):
        """
            查询股票实时行情
        :param account:
        :return:
            行情
        """
        url = self.baseurl+"/query/gphq"

        params = {
            'account': account,
            'zqdm': zqdm,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

        items = []
        for item in resp.data:
            items.append(_Gphq(**item))

        return items

    def order_xjmr(self, account, zqdm, price, count):
        """
            限价买入
        :param account:
        :param zqdm:
        :param price:
        :param count:
        :return:
            委托编号
        """
        url = self.baseurl+"/order/xjmr"

        params = {
            'account': account,
            'zqdm': zqdm,
            'price': price,
            'count': count,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

        items = []
        for item in resp.data:
            items.append(_Xjmr(**item))

        return items

    def order_xjmc(self, account, zqdm, price, count):
        """
            限价卖出
        :param account:
        :param zqdm:
        :param price:
        :param count:
        :return:
            委托编号
        """
        url = self.baseurl+"/order/xjmc"

        params = {
            'account': account,
            'zqdm': zqdm,
            'price': price,
            'count': count,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

        items = []
        for item in resp.data:
            items.append(_Xjmc(**item))

        return items

    def order_sjmr(self, account, zqdm, price, count):
        """
            市价买入
        :param account:
        :param zqdm:
        :param price:
        :param count:
        :return:
            委托编号
        """
        url = self.baseurl+"/order/sjmr"

        params = {
            'account': account,
            'zqdm': zqdm,
            'price': price,
            'count': count,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

        items = []
        for item in resp.data:
            items.append(_Sjmr(**item))

        return items

    def order_sjmc(self, account, zqdm, price, count):
        """
            市价卖出
        :param account:
        :param zqdm:
        :param price:
        :param count:
        :return:
            委托编号
        """
        url = self.baseurl+"/order/sjmc"

        params = {
            'account': account,
            'zqdm': zqdm,
            'price': price,
            'count': count,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

        items = []
        for item in resp.data:
            items.append(_Sjmc(**item))

        return items

    def order_cancel(self, account, zqdm, orderno):
        """
            委托撤单
        :param account:
        :param zqdm:
        :param orderno:
        :return:
        """
        url = self.baseurl+"/order/cancel"

        params = {
            'account': account,
            'zqdm': zqdm,
            'orderno': orderno,
        }
        params = self.make_token(params)

        resp = requests.get(url, params=params).json()

        if resp.get('status') != 0:
            raise TradeApiError(resp.get('msg'))

        items = []
        for item in resp.data:
            items.append(_Wtcd(**item))

        return items
