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


# 委托下单结果
class _Wtxd(dict):
    def __init__(self, **kwargs):
        self.wtbh = kwargs.get('wtbh')
        super().__init__(self, **kwargs)

# 委托撤单结果
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

    def query_quote(self, account, zqdm):
        """
            查询股票实时行情
        :param account:
        :return:
            行情
        """
        url = self.baseurl+"/quote/query"

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

    def query_account(self, account, type, sdate=None, edate=None):
        """
            查询当前或者历史信息
        :param account:
        :param type: str, 查询类别，dqzc/dqcc/drwt/drcj/kcwt/gdxx/lswt/lscj/jgd
        :param sdate: str, 开始日期，yyyymmdd
        :param edate: str, 结束日期, yyyymmdd
        :return:
            dict/list
        """
        url = self.baseurl+"/account/query"

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

    def place_order(self, account, otype, ptype, zqdm, price, count):
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
        url = self.baseurl+"/order/place"

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
            items.append(_Wtxd(**item))

        return items

    def cancel_order(self, account, zqdm, orderno):
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
