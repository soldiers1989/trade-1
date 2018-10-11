"""
    quote service
"""
import time, threading, logging, decimal


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
        self._subscribers = {}

        # subscribe lower target price
        self.lprice = decimal.Decimal('0.000')
        # subscribe upper target price
        self.uprice = decimal.Decimal('10000.000')

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
        for subscriber in self._subscribers:
            subscriber.callback.on_tick(self.code, price)


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
        self._interval = kwargs.get('interval', 5)

        # subscribe index by symbols
        self._symbols = {}
        # lock for subscribe symbols
        self._lock = threading.RLock()

        # stop flag
        self._stopped = False
        # id counter
        self._nextid = 0

        # init thread
        super().__init__(self)

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
        :param symbols: list, symbol code list
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
                    for symbol, price in quotes:
                        symbolobj = self._symbols.get(symbol)
                        if symbolobj is not None:
                            symbolobj.notify_subscriber(price)

                    logging.info('quote service loop finished')
                # sleep for while
                time.sleep(self._interval)
            except Exception as e:
                logging.error('quote service loop failed, error: %s'%str(e))


class MockQuoteService(QuoteService):
    def __init__(self, **kwargs):
        """
            mock quote
        :param kwargs:
        """
        self._probability = kwargs.get('probability', 0.1)

    def query(self, symbols):
        pass


class SimuQuoteService(QuoteService):
    def __init__(self, **kwargs):
        pass

    def query(self, symbols):
        pass