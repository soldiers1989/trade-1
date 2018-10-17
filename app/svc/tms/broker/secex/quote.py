"""
    quote service
"""
import time, threading, logging, decimal, random
from trpc import quote


class QuoteServiceError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class Callback:
    """
        callback for quote service
    """
    def on_tick(self, symbol, price):
        """
            snapshot tick data
        :param symbol: str, symbol code
        :param price: decimal, current price of symbol
        :return:
        """
        pass


class Subscriber:
    """
        subscriber
    """
    def __init__(self, id, symbol, price, callback):
        """
            init a subscriber object
        :param id: str, subscriber id
        :param symbol: str, symbol code
        :param price: decimal, target price
        :param callback: obj, callback object
        """
        self.id = id
        self.symbol = symbol
        self.price = price
        self.callback = callback


class Symbol:
    """
        symbol
    """
    def __init__(self, code):
        """
            init a symbol object
        :param code: str, symbol code
        """
        self.code = code
        self._subscribers = {} # id->subscriber

        # subscribe lower target price
        self.lprice = decimal.Decimal('1000.000')
        # subscribe upper target price
        self.uprice = decimal.Decimal('0.000')

    def add_subscriber(self, subscriber: Subscriber):
        """
            add a new subscriber
        :param subscriber: obj, subscriber object
        :return:
        """
        if self._subscribers.get(subscriber.id) is None:
            self._subscribers[subscriber.id] = subscriber

            # update target lower/upper price
            self.update_price()

    def del_subscriber(self, id):
        """
            delete a subscriber by id
        :param id: str, subsciber id
        :return:
        """
        if self._subscribers.get(id) is not None:
            del self._subscribers[id]
            # update target lower/upper price
            self.update_price()
            return True

        return False

    def notify_subscriber(self, price):
        """
            notify subscriber with new symbol price
        :param price: decimal, current symbol price
        :return:
        """
        unsubs = []
        for subscriber in self._subscribers.values():
            if not subscriber.callback.on_tick(self.code, price):
                unsubs.append(subscriber.id)

        for id in unsubs:
            del self._subscribers[id]

    def update_price(self):
        """
            update subscriber lower and upper price
        :return:
        """
        for subscriber in self._subscribers.values():
            if subscriber.price > self.uprice:
                self.uprice = subscriber.price

            if subscriber.price < self.lprice:
                self.lprice = subscriber.price


class QuoteService(threading.Thread):
    """
        quote service
    """
    def __init__(self, **kwargs):
        """
            init
        """
        # quote tick interval
        self._interval = kwargs.get('interval', 3)

        # subscribe index by symbols
        self._symbols = {}
        # lock for subscribe symbols
        self._lock = threading.RLock()

        # stop flag
        self._stopped = False
        # id counter
        self._nextid = 0

        # init thread
        super().__init__()

    def start(self):
        """

        :return:
        """
        super().start()

    def stop(self):
        """
            stop quote service
        :return:
        """
        if not self.is_alive():
            return

        self._stopped = True
        self.join()

    def subscribe(self, symbol, price, callback):
        """
            subscribe an symbol quote with callback object
        :param symbol: str, symbol code
        :param target_price: decimal, target price
        :param callback: obj, callback object
        :return:
            str, id
        """
        with self._lock:
            # generate subscribe id
            id = self._nextid
            self._nextid += 1

            # add subscriber to relate symbol subscriber list
            if self._symbols.get(symbol) is None:
                self._symbols[symbol] = Symbol(symbol)

            price = decimal.Decimal(price).quantize(decimal.Decimal('0.000'))
            self._symbols[symbol].add_subscriber(Subscriber(id, symbol, price, callback))

            # return subscriber's id
            return str(id)

    def unsubscribe(self, id):
        """
            unsubscribe with subscriber id
        :param id: str, subscriber id
        :return:
        """
        with self._lock:
            for symbolobj in self._symbols.values():
                if symbolobj.del_subscriber(id):
                    break

    def query(self, symbols)->list:
        """
            query current quote of symbols
        :param symbols: list, list of symbol object
        :return:
            dict - symbol->price
        """
        pass

    def run(self):
        """
            thread run function
        :return:
        """
        while not self._stopped:
            try:
                # update price
                with self._lock:
                    logging.info('quote service loop start')
                    # query quotes
                    quotes = self.query(self._symbols.values())

                    # notify subscribers
                    for symbol, price in quotes.items():
                        symbolobj = self._symbols.get(symbol)
                        if symbolobj is not None:
                            symbolobj.notify_subscriber(price)

                    logging.info('quote service loop finished')
            except Exception as e:
                logging.error('quote service loop failed, error: %s'%str(e))

            # sleep for while
            time.sleep(self._interval)


class MockQuoteService(QuoteService):
    def __init__(self, **kwargs):
        """
            mock quote
        :param kwargs:
        """
        # hit probability with the symbol's target price range
        self._probability = int(100*(kwargs.get('probability', 0.1)))
        # volatility beside the targe price
        self._volatility = kwargs.get('volatility', 0.01)

        # init super
        super().__init__(**kwargs)

    def query(self, symbols):
        """
            get current quote of symbols, price probability:
            ----(1-probability)/2-----|--------probability--------|-----(1-probability)/2-----
            --less than target price--|--equal with target price--|--large than target price--
        :param symbols: list,
        :return:
            dict
        """
        quotes = {}
        for symbol in symbols:
            if self.hittarget():
                quotes[symbol.code] = self.random_ine_price(symbol.lprice, symbol.uprice)
            else:
                quotes[symbol.code] = self.random_out_price(symbol.lprice, symbol.uprice)
        return quotes

    def hittarget(self):
        """
            hit symbol's target price
        :return:
        """
        return random.randint(0, 100) < self._probability

    def random_ine_price(self, lprice, uprice):
        """
            generate a random lprice<=price<=uprice
        :param lprice: decimal, lower price
        :param uprice: decimal, upper price
        :return:
            decimal
        """
        a, b = int(1000*lprice), int(1000*uprice)
        price = random.randint(a, b) / 1000
        return decimal.Decimal(price).quantize(decimal.Decimal('0.000'))

    def random_out_price(self, lprice, uprice):
        """
            generate a random price>=uprice or price<=lprice, limit by volatility
        :param lprice: decimal, lower price
        :param uprice: decimal, upper price
        :return:
            price
        """
        if random.randint(0, 99) < 50:
            a, b = int(1000 * lprice * decimal.Decimal(1-self._volatility)), int(1000 * lprice)
        else:
            a, b = int(1000 * uprice), int(1000 * uprice * decimal.Decimal(1+self._volatility))

        price = random.randint(a, b) / 1000

        return decimal.Decimal(price).quantize(decimal.Decimal('0.000'))


class SimuQuoteService(QuoteService):
    def __init__(self, **kwargs):
        """
            init simulation quote service with remote address
        :param kwargs:
        """
        baseurl, key, safety = kwargs.get('baseurl'), kwargs.get('key'), kwargs.get('safety')
        if baseurl is None:
            raise QuoteServiceError('未知的远程行情服务地址')
        if safety is None:
            safety = False
        else:
            if key is None:
                raise QuoteServiceError('未知的远程行情服务key')

        self._quoterpc = quote.QuoteRpc(baseurl, key, safety)

        # init super
        super().__init__(**kwargs)

    def query(self, symbols):
        """
            query symbol price from real quote api
        :param symbols: list
        :return:
            dict
        """
        quotes = {}
        for symbol in symbols:
            try:
                scode = symbol
                if isinstance(symbol, Symbol):
                    scode = symbol.code

                quotes[scode] = decimal.Decimal(self._quoterpc.get_quote(scode)['dqj']).quantize(decimal.Decimal('0.000'))
            except Exception as e:
                logging.error('query quote of symbol: %s failed, error: %s' % (scode, str(e)))

        return quotes


def create(**kwargs):
    """
        create a quote service object
    :param kwargs: dict,
    :return:
    """
    # get quote service mode
    mode = kwargs.get('mode', 'mock')
    if mode not in ['mock', 'simu']:
        raise QuoteServiceError('未知的行情服务模式: %s' % str(mode))

    # create new quote service object
    if mode == 'mock':
        return MockQuoteService(**kwargs)
    else:
        return SimuQuoteService(**kwargs)


class _DemoObserver:
    """
        demo observer of quote service
    """
    def on_tick(self, symbol, price):
        """
            snapshot tick data
        :param symbol: str, symbol code
        :param price: decimal, current price of symbol
        :return:
        """
        print('%s, %s' % (symbol, str(price)))


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        #qs = SimuQuoteService(baseurl='http://localhost:10002', key='abc', safety=False, interval=2)
        qs = MockQuoteService(interval=2)
    else:
        if sys.argv[1] == 'mock':
            qs = MockQuoteService(interval=2)
        else:
            qs = SimuQuoteService('http://localhost:10002', key='abc', safety=False, interval=2)

    qs.start()

    do = _DemoObserver()
    qs.subscribe('000100', 2.50, do)
    qs.subscribe('000100', 2.70, do)

    while True:
        time.sleep(1)