"""
    base class for trade service
"""
import datetime, random, decimal
from . import quote

# date/time format
DATE_FORMT = '%Y-%m-%d'
TIME_FORMT = '%H:%M:%S'


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
    def __init__(self, symbol, otype, ptype, oprice, ocount, ocode, account):
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

        self.symbol = symbol
        self.odate = datetime.datetime.today().strftime(DATE_FORMT)
        self.otime = datetime.datetime.today().strftime(TIME_FORMT)
        self.otype = otype
        self.ptype = ptype
        self.oprice = oprice
        self.ocount = ocount
        self.ocode = ocode

        self.dprice = None
        self.dcount = 0
        self.dcode = None
        self.ddate = None
        self.dtime = None

        self.status = Status.sent

        self.account = account # relate account

    def deal(self, price):
        """
            make deal with price
        :param price: decimal, current price
        :return:
        """
        # make deal
        self.dealt(price)

        # partially dealt or total dealt
        if self.dcount is not None:
            if self.dcode is None:
                self.dcode = str(random.randint(0, 1000000))
            if self.ddate is None:
                self.ddate = datetime.datetime.today().strftime('%Y-%m-%d')
            if self.dtime is None:
                self.dtime = datetime.datetime.today().strftime('%H:%M:%S')

            if self.dcount < self.ocount:
                self.status = Status.pdeal
            else:
                self.status = Status.tdeal
                # notify account with dealt message
                self.account.dealt(self.symbol, self.otype, self.dprice, self.dcount)

    def cancel(self):
        """
            cancel order randomly
        :return:
        """
        if self.status in [Status.tcanceled, Status.pcanceled, Status.tdeal]:
            return

        if self.dcount is None:
            self.status = Status.tcanceled
            # notify account with canceled message
            self.account.canceled(self.symbol, self.otype, self.oprice, self.ocount)
        elif self.dcount < self.ocount:
            self.status = Status.pcanceled
            # notify account with dealt message
            self.account.dealt(self.symbol, self.otype, self.dprice, self.dcount)
        else:
            pass

    def dealt(self, price):
        """
            make random dealt count increasingly by dealt efficient
        :param price: decimal, dealt price
        :return:
        """
        if self.ptype == Ptype.xj:
            if (self.otype == Otype.buy and price > self.oprice) or (self.otype == Otype.sell and price < self.oprice):
                return
            else:
                price = self.oprice

        # random deal count
        dcount = int(random.randint(0, 1)*(self.ocount-self.dcount)*DEALT_EFFICIENCY)
        dcount = self.ocount-self.dcount if dcount > self.ocount-self.dcount else dcount

        # compute deal price
        self.dprice = (self.dcount * self.dprice + dcount * price) / (self.dcount + dcount)

        # add deal count
        self.dcount = self.dcount + dcount

    def on_tick(self, symbol, price):
        """
            snapshot tick data
        :param symbol: str, symbol code
        :param price: decimal, current price of symbol
        :return:
        """
        # check status
        if self.status in [Status.tcanceled, Status.pcanceled, Status.tdeal]:
            return False

        # make deal by price
        self.deal(price)

        # unsubscribe quote
        return True

    def detail(self):
        """
            get order detail
        :return:
            dict
        """
        return {
            'wtrq': self.odate,
            'wtsj': self.otime,
            'gddm': '',
            'zqdm': self.symbol,
            'zqmc': '',
            'mmbz': '',
            'wtjg': self.oprice,
            'wtsl': self.ocount,
            'wtbh': self.ocode,
            'cjsl': self.dcount,
            'cjjg': self.dprice,
            'cjje': '0.000' if self.dcount is None else self.dcount*self.dprice,
            'cjrq': self.ddate,
            'cjsj': self.dtime,
            'cdsl': '',
            'cdbz': '',
            'ztsm': self.status
        }


class SymbolPosition:
    def __init__(self, symbol, total=0, usable=0, price=decimal.Decimal('0.000')):
        self.symbol = symbol # 证券代码
        self.total = total # 持仓量
        self.usable = usable # 可用量
        self.price = price # 当前价格

    @property
    def market_value(self):
        return self.total*self.price

    def detail(self):
        return {
            'zqdm': self.symbol,
            'zqmc': '',
            'zqsl': self.total,
            'kmsl': self.usable
        }


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
        self._total_money = money
        self._usable_money = money

        self._holds = {} # 当前持仓, symbol code->account position
        self._orders = {} # 委托记录, date->{ocode->[trade orders]}

        self._login = False

        self._next_order_code = 0

    def login(self, pwd):
        """
            login with password
        :param pwd: str, account password
        :return:
        """
        if pwd != self._pwd:
            raise TradeServiceError('account %s login failed, invalid password' % self._account)
        self._login = True

    def logout(self):
        """
            logout
        :return:
        """
        self._login = False

    def transfer(self, money):
        """
            transfer money in/out from trade account
        :param money: decimal, money to transfer, >0 means money into account, < means money outoff account
        :return:
            decimal, left money
        """
        self._total_money += money
        self._usable_money += money

    def query(self, type, sdate=None, edate=None):
        """
            query account information
        :param type: str, data type: dqzc/dqcc/drwt/lswt/...
        :param sdate: date, start date
        :param edate: date, end date
        :return:
        """
        results = []

        if type == 'dqzc':
            results.append({
                'zzc': self._total_money + sum([position.market_value for position in self._holds.values()]),
                'zjye': self._total_money,
                'kyzj': self._usable_money,
                'kqzj': self._usable_money
            })
        elif type == 'dqcc':
            for position in self._holds.values():
                results.append(position.detail())
        elif type == 'drwt':
            today = datetime.date.today()
            if self._orders.get(today) is not None:
                for order in self._orders[today].values():
                    results.append(order.detail())
        elif type == 'lswt':
            for date, orders in self._orders.items():
                if date >= sdate and date <= edate:
                    for order in orders.values():
                        results.append(order.detail())
        else:
            raise TradeServiceError('查询类别 %s 不支持' % type)

        return results

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
        self.check_login()

        # cost of order
        cost = ocount * oprice

        if otype == Otype.buy:
            # check left money
            if self._usable_money < cost:
                raise TradeServiceError('可用余额不足')
            # change usable money
            self._usable_money -= cost

            # create position record
            if self._holds.get(symbol) is None:
                self._holds[symbol] = SymbolPosition(symbol)
        else:
            # check left position
            position = self._holds.get(symbol)
            if position is None or position.usable < ocount:
                raise TradeServiceError('可用证券不足')

            # freeze hold
            position.usable -= ocount

        # create new order id
        ocode = str(self._next_order_code)
        self._next_order_code += 1

        # add today's order if not exist
        today = datetime.date.today()
        if self._orders.get(today) is None:
            self._orders[today] = {}

        # add new order
        self._orders[today][ocode] = TradeOrder(symbol, otype, ptype, oprice, ocount, ocode, self)

        return ocode

    def cancel(self, ocode):
        """
            cancel order
        :param ocode: str, order code
        :return:
        """
        self.check_login()

        today = datetime.date.today()
        orders = self._orders.get(today)
        if orders is None or orders.get(ocode) is None:
            raise TradeServiceError('委托订单 %s 不存在' % ocode)

        # cancel order
        orders[ocode].cancel()

    def dealt(self, symbol, otype, price, count):
        """
            symbol dealt notify
        :param symbol:
        :param otype:
        :param price:
        :param count:
        :return:
        """
        # dealt order money
        money = count * price

        if otype == Otype.buy:
            # decrease account money
            self._total_money -= money

            # increase account position
            self._holds[symbol].total += count
        else:
            # increase account money
            self._total_money += money
            self._usable_money += money

            # decrease account position
            self._holds[symbol].total -= count

    def canceled(self, symbol, otype, oprice, ocount):
        """
            symbol order totally canceled notify
        :param symbol:
        :param otype:
        :param oprice:
        :param ocount:
        :return:
        """
        # canceled order money
        money = ocount * oprice

        if otype == Otype.buy:
            # free money
            self._usable_money += money
        else:
            # free position
            self._holds[symbol].usable += ocount

    def clear(self):
        """
            clear orders of account
        :return:
        """
        self._orders = {}

    def check_login(self):
        """
            check if account has login
        :return:
        """
        if not self._login:
            raise TradeServiceError('账户 %s 未登录' % self._account)


class TradeService:
    def __init__(self):
        """
            init trading service
        """
        # registered accounts
        self._accounts = {}

        # init quote service
        self._quotesvc = None

        # running flag
        self._running = False

    def start(self, **kwargs):
        """
            start trade service
        :return:
        """
        if self._quotesvc is not None:
            self.stop()

        self._quotesvc = quote.create(**kwargs)
        self._quotesvc.start()
        self._running = True

    def stop(self):
        """
            stop trade service
        :return:
        """
        if self._quotesvc is not None:
            self._quotesvc.stop()
            self._quotesvc = None
        self._running = False

    def register(self, **kwargs):
        """
            register a trade account
        :param kwargs: dict, account information
        :return:
        """
        account, pwd, money = kwargs.get('account'), kwargs.get('pwd'), kwargs.get('money')
        if account is None or pwd is None or money is None:
            raise TradeServiceError('register account failed, error: missing parameters')

        if self._accounts.get(account) is None:
            self._accounts[account] = TradeAccount(account, pwd, money)

    def login(self, account, pwd):
        """
            trade account login
        :param account:
        :param pwd:
        :return:
        """
        accountobj = self._accounts.get(account)
        if accountobj is None:
            raise TradeServiceError('account %s not exist' % account)

        accountobj.login(pwd)

    def logout(self, account):
        """
            trade account logout
        :return:
        """
        accountobj = self._accounts.get(account)
        if accountobj is None:
            raise TradeServiceError('account %s not exist' % account)
        accountobj.logout()

    def transfer(self, account, money):
        """
            transfer money in/out from trade account
        :return:
        """
        self.check_running()
        accountobj = self._accounts.get(account)
        if accountobj is None:
            raise TradeServiceError('account %s not exist' % account)
        return accountobj.transfer(money)

    def query(self, account, type, sdate=None, edate=None):
        """
            query account information
        :param account:
        :param type:
        :param sdate:
        :param edate:
        :return:
        """
        accountobj = self._accounts.get(account)
        if accountobj is None:
            raise TradeServiceError('account %s not exist' % account)
        return accountobj.query(type, sdate, edate)

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
        self.check_running()
        accountobj = self._accounts.get(account)
        if accountobj is None:
            raise TradeServiceError('未登录的账户: %s' % account)

        # check price type
        if ptype == Ptype.sj:
            oprice = self._quotesvc.query([symbol])[0]['dqj']

        accountobj.place(symbol, otype, ptype, oprice, ocount)

    def cancel(self, account, ocode):
        """
            cancel an order
        :param account: str, account name
        :param ocode: str, order code
        :return:
        """
        self.check_running()
        accountobj = self._accounts.get(account)
        if accountobj is None:
            raise TradeServiceError('未登录的账户: %s' % account)

        accountobj.cancel(ocode)

    def clear(self, account):
        """
            clear orders of account
        :return:
        """
        accountobj = self._accounts.get(account)
        if accountobj is None:
            raise TradeServiceError('未登录的账户: %s' % account)

        accountobj.clear()

    def check_running(self):
        """
            check if trade service is running
        :return:
        """
        if not self._running:
            raise TradeServiceError('交易服务未启动')

default = TradeService()
