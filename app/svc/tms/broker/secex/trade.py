"""
    base class for trade service
"""
import datetime, random, decimal
from . import quote

# date/time format
DATE_FORMT = '%Y%m%d'
TIME_FORMT = '%H:%M:%S'


# dealt probability
DEALT_EFFICIENCY = 0.5


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

        # subscribe quote service
        self.subid = self.account.quotesvc.subscribe(self.symbol, self.oprice, self)

    def deal(self, price):
        """
            make deal with price
        :param price: decimal, current price
        :return:
        """
        # make deal
        self.make_deal(price)

        # partially dealt or total dealt
        self.update_status()

    def make_deal(self, price):
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
        dcount = int(random.randint(0, 1)*self.ocount*DEALT_EFFICIENCY)
        dcount = self.ocount-self.dcount if dcount > self.ocount-self.dcount else dcount
        if dcount == 0:
            return

        # compute deal price
        self.dprice = (self.dmoney + dcount * price) / (self.dcount + dcount)

        # add deal count
        self.dcount = self.dcount + dcount

    def update_status(self):
        """
            update order status
        :return:
        """
        if self.dcount is not None:
            if self.dcode is None:
                self.dcode = str(random.randint(0, 1000000))
            if self.ddate is None:
                self.ddate = datetime.datetime.today().strftime('%Y-%m-%d')
            if self.dtime is None:
                self.dtime = datetime.datetime.today().strftime('%H:%M:%S')

            if 0 < self.dcount < self.ocount:
                self.status = Status.pdeal
            else:
                self.status = Status.tdeal
                # notify account with dealt message
                self.dealt()

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
            self.canceled()
        elif self.dcount < self.ocount:
            self.status = Status.pcanceled
            # notify account with dealt message
            self.dealt()
        else:
            pass

    def dealt(self):
        """
            order dealt
        :return:
        """
        # notify account with dealt message
        self.account.dealt(self.symbol, self.otype, self.dprice, self.dcount)

        # unsubscribe quote service
        self.account.quotesvc.unsubscribe(self.subid)

    def canceled(self):
        """
            order canceled
        :return:
        """
        # notify account with canceled message
        self.account.canceled(self.symbol, self.otype, self.oprice, self.ocount)

        # unsubscribe quote service
        self.account.quotesvc.unsubscribe(self.subid)

    def clear(self):
        """
            order clear after market closed
        :return:
        """
        if self.status in [Status.pdeal]:
            self.dealt()
        elif self.status not in [Status.tcanceled, Status.pcanceled, Status.tdeal]:
            self.status = Status.expired
            self.canceled()
        else:
            pass

        return self.detail()

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

    @property
    def dmoney(self):
        """
            deal money
        :return:
            decimal
        """
        if self.dcount is None or self.dprice is None:
            return decimal.Decimal('0.00')

        return self.dcount*self.dprice

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
            'cjje': self.dmoney,
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

    def clear(self):
        self.usable = self.total

    def detail(self):
        return {
            'zqdm': self.symbol,
            'zqmc': '',
            'zqsl': self.total,
            'kmsl': self.usable
        }


class TradeAccount:
    def __init__(self, account, pwd, money, quotesvc):
        """
            init  trade account
        :param account: str, account name
        :param pwd: str, account login password
        :param money: decimal, account usable money
        :param quotesvc: quote.QuoteService, quote service
        """
        self._account = account
        self._pwd = pwd
        self._total_money = money
        self._usable_money = money

        self._holds = {} # 当前持仓, symbol code->account position
        self._orders = {} # 委托记录, date->{ocode->[trade orders]}

        self._login = False

        self.quotesvc = quotesvc

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
        return self.status()

    def logout(self):
        """
            logout
        :return:
        """
        self._login = False
        return self.status()

    def status(self):
        """
            account status
        :return:
            dict
        """
        return {
            'account': self._account,
            'pwd': self._pwd,
            'money': self._total_money,
            'usable': self._usable_money,
            'login': self._login,
            'holds': len(self._holds),
        }

    def transfer(self, money):
        """
            transfer money in/out from trade account
        :param money: decimal, money to transfer, >0 means money into account, < means money outoff account
        :return:
            decimal, left money
        """
        self._total_money += money
        self._usable_money += money

        return {
            'account': self._account,
            'money': self._total_money,
            'usable': self._usable_money
        }

    def query(self, type, sdate=None, edate=None):
        """
            query account information
        :param type: str, data type: dqzc/dqcc/drwt/lswt/...
        :param sdate: date, start date
        :param edate: date, end date
        :return:
        """
        sdate, edate = self.format_date(sdate), self.format_date(edate)
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
        order = TradeOrder(symbol, otype, ptype, oprice, ocount, ocode, self)
        self._orders[today][ocode] = order

        return order.detail()

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

        # get order
        order = orders.get(ocode)
        # cancel order
        order.cancel()

        return order.detail()

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
            account clear after market closed
        :return:
        """
        # order clear
        today = datetime.date.today()
        orders = self._orders.get(today, {})
        for order in orders.values():
            order.clear()

        # account clear
        self._usable_money = self._total_money
        for position in self._holds.values():
            position.clear()

        return self.status()

    def check_login(self):
        """
            check if account has login
        :return:
        """
        if not self._login:
            raise TradeServiceError('账户 %s 未登录' % self._account)

    @staticmethod
    def format_date(date):
        """
            format date
        :param date: str|date, date string to format
        :return:
            datetime.date
        """
        if date is None or isinstance(date, datetime.date):
            return date

        return datetime.datetime.strptime(str(date), DATE_FORMT).date()


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

    def status(self):
        """
            trade service status
        :return:
            dict
        """
        accounts = [account.status() for account in self._accounts.values()]
        return {
            'running': self._running,
            'accounts': accounts
        }

    def register(self, **kwargs):
        """
            register a trade account
        :param kwargs: dict, account information
        :return:
        """
        self.check_running()

        account, pwd, money = kwargs.get('account'), kwargs.get('pwd'), kwargs.get('money')
        if account is None or pwd is None or money is None:
            raise TradeServiceError('注册账户失败，缺少必要的参数')

        money = decimal.Decimal(money).quantize(decimal.Decimal('0.00'))
        if self._accounts.get(account) is None:
            self._accounts[account] = TradeAccount(account, pwd, money, self._quotesvc)

        return self._accounts[account].status()

    def login(self, account, pwd):
        """
            trade account login
        :param account:
        :param pwd:
        :return:
        """
        accountobj = self._accounts.get(account)
        if accountobj is None:
            raise TradeServiceError('账户 %s 不存在' % account)

        return accountobj.login(pwd)

    def logout(self, account):
        """
            trade account logout
        :return:
        """
        accountobj = self._accounts.get(account)
        if accountobj is None:
            raise TradeServiceError('账户 %s 不存在' % account)
        return accountobj.logout()

    def transfer(self, account, money):
        """
            transfer money in/out from trade account
        :return:
        """
        self.check_running()
        accountobj = self._accounts.get(account)
        if accountobj is None:
            raise TradeServiceError('账户 %s 不存在' % account)

        money = decimal.Decimal(money).quantize(decimal.Decimal('0.00'))
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
            raise TradeServiceError('账户 %s 不存在' % account)
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

        oprice, ocount = decimal.Decimal(oprice), int(ocount)

        # check price type
        if ptype == Ptype.sj:
            quotes = self._quotesvc.query([symbol])
            if quotes.get(symbol) is None:
                raise TradeServiceError('获取证券 %s 行情失败' % symbol)
            oprice = decimal.Decimal(quotes.get(symbol))

        return accountobj.place(symbol, otype, ptype, oprice, ocount)

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

        return accountobj.cancel(ocode)

    def clear(self, account = None):
        """
            clear orders of account
        :return:
        """
        results = []
        if account is None:
            for accountobj in self._accounts.values():
                result = accountobj.clear()
                results.append(result)
        else:
            accountobj = self._accounts.get(account)
            if accountobj is None:
                raise TradeServiceError('未登录的账户: %s' % account)

            result = accountobj.clear()
            results.append(result)
        return results

    def check_running(self):
        """
            check if trade service is running
        :return:
        """
        if not self._running:
            raise TradeServiceError('交易服务未启动')

default = TradeService()
