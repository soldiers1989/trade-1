"""
    base class for trade service
"""
import datetime, random, decimal
from . import quote


# dealt probability
DEALT_EFFICIENCY = 0.1


class Otype:
    buy = 'buy'
    sell = 'sell'


class Ptype:
    xj = 'xj'
    sj = 'sj'


class Status:
    notsend = 'notsend'
    tosend = 'tosend'
    sending = 'sending'
    sent = 'sent'
    tocancel = 'tocancel'
    canceling = 'canceling'
    pcanceled = 'pcanceled'
    tcanceled = 'tcanceled'
    fcanceled = 'fcanceled'
    pdeal = 'pdeal'
    tdeal = 'tdeal'
    dropped = 'dropped'
    expired = 'expired'


class TradeServiceError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TradeOrder(quote.Callback):
    def __init__(self, symbol, otype, ptype, oprice, ocount, ocode):
        """
            init a trade order
        :param symbol: str, symbol code
        :param otype: str, order type bull|sell
        :param ptype: str, price type xj|sj
        :param oprice: decimal, order price
        :param ocount: int, order count
        :param ocode: str, order code
        """
        if otype not in [Otype.buy, Otype.sell]:
            raise TradeServiceError('未知的订单类型: %s' % otype)
        if ptype not in [Ptype.xj, Ptype.sj]:
            raise TradeServiceError('未知的报价类型: %s' % ptype)

        self._symbol = symbol
        self._otype = otype
        self._ptype = ptype
        self._oprice = oprice
        self._ocount = ocount
        self._ocode = ocode

        self._dprice = None
        self._dcount = 0
        self._dcode = None
        self._ddate = None
        self._dtime = None

        self._status = Status.sent

    def deal(self, price):
        """
            make deal with price
        :param price: decimal, current price
        :return:
        """
        if self._ptype == Ptype.xj:
            if (self._otype == Otype.buy and price < self._oprice) or (self._otype == Otype.sell and price > self._oprice):
                self.random_dealt(self._oprice)
        else: # market price
            self.random_dealt(price)

        # partially dealt or total dealt
        if self._dcount is not None:
            if self._dcode is None:
                self._dcode = str(random.randint(0, 1000000))
            if self._ddate is None:
                self._ddate = datetime.datetime.today().strftime('%Y-%m-%d')
            if self._dtime is None:
                self._dtime = datetime.datetime.today().strftime('%H:%M:%S')

            if self._dcount < self._ocount:
                self._status = Status.pdeal
            else:
                self._status = Status.tdeal

    def cancel(self):
        """
            cancel order randomly
        :return:
        """
        if self._dcount is None:
            self._status = Status.tcanceled
        elif self._dcount < self._ocount:
            self._status = Status.pcanceled
        else:
            self._status = Status.tdeal

    def random_dealt(self, ptype, price):
        """
            make random dealt count increasingly by dealt efficient
        :param ptype: str, price type
        :param price: decimal, dealt price
        :return:
        """
        if self._dcount is None:
            self._dcount = 0

        dcount = int(random.randint(0, 1)*(self._ocount-self._dcount)*DEALT_EFFICIENCY)

        if ptype == Ptype.xj:
            self._dcount = self._dcount + dcount
            if self._dcount > self._ocount:
                self._dcount = self._ocount
        else:
            if self._dcount + dcount > self._ocount:
                dcount = self._ocount-self._dcount

            self._dprice = (self._dcount*self._dprice + dcount*price)/(self._dcount + dcount)
            self._dcount = self._dcount + dcount

    def on_tick(self, symbol, price):
        """
            snapshot tick data
        :param symbol: str, symbol code
        :param price: decimal, current price of symbol
        :return:
        """
        # make deal by price
        self.deal(price)

        # check status
        if self._status in [Status.tcanceled, Status.pcanceled, Status.tdeal]:
            return False

        # unsubscribe quote
        return True


class TradeAccount:
    def __init__(self, account, pwd, money):
        """
            init  trade account
        :param account: str, account name
        :param pwd: str, account login password
        :param money: decimal, account usable money
        """
        self._account = account
        self._pwd = pwd
        self._money = money

        self._orders = {}
        self._next_order_code = 0

    def place(self, symbol, otype, ptype, oprice, ocount):
        """
            place an order
        :param symbol: str, symbol code
        :param otype: str, order type buy|sell
        :param ptype: str, price type xj|sj
        :param oprice: decimal, order price
        :param ocount: int, order count
        :return:
            str, order code
        """
        ocode = str(self._next_order_code)
        self._next_order_code += 1

        self._orders[ocode] = TradeOrder(symbol, otype, ptype, oprice, ocount, ocode)

        return ocode

    def cancel(self, ocode):
        """
            cancel order
        :param ocode: str, order code
        :return:
        """
        order = self._orders.get(ocode)
        if order is not None:
            order.cancel()




class TradeService:
    def __init__(self, *args, **kwargs):
        """
            init trading service
        """
        # registered accounts
        self._accounts = {}
        # init quote service
        self._quotesvc = quote.create(**kwargs)

    def register(self, **kwargs):
        """
            register a trade account
        :param kwargs: dict, account information
        :return:
        """
        pass

    def login(self, account, pwd):
        """
            trade account login
        :param account:
        :param pwd:
        :return:
        """
        pass

    def logout(self, account):
        """
            trade account logout
        :return:
        """
        pass

    def transfer(self, account, money):
        """
            transfer money in/out from trade account
        :return:
        """
        pass

    def query(self, account, type):
        """
            query account information
        :return:
        """
        pass

    def place(self, account, symbol, otype, ptype, oprice, ocount):
        """
            place an order
        :param account: str, account name
        :param symbol: str, symbol code
        :param otype: str, order type buy|sell
        :param ptype: str, price type xj|sj
        :param oprice: decimal, order price
        :param ocount: int, order count
        :return:
            str, order number
        """
        accountobj = self._accounts.get(account)
        if accountobj is None:
            raise TradeServiceError('未登录的账户: %s' % account)

        accountobj.place(symbol, otype, ptype, oprice, ocount)

    def cancel(self, account, ocode):
        """
            cancel an order
        :param account: str, account name
        :param ocode: str, order code
        :return:
        """
        accountobj = self._accounts.get(account)
        if accountobj is None:
            raise TradeServiceError('未登录的账户: %s' % account)

        accountobj.cancel(ocode)

    def list(self):
        """
            list all account information including orders
        :return:
        """
        pass

    def clear(self):
        """
            clear orders of account
        :return:
        """
        pass

    def dealt(self):
        """
            make dealt of an order
        :return:
        """
        pass

    def canceled(self):
        """
            make canceled of an order
        :return:
        """
        pass
