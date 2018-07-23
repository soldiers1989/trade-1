"""
    quote recorder
"""
import os, sys, random, math, json, time, threading, requests


class _Config:
    """
        configure for quote recorder
    """
    # test flag
    TEST = False

    # log flag
    LOG = False

    # ifeng quote server host
    HOST = "hq.finance.ifeng.com"

    # request headers
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Host": "hq.finance.ifeng.com",
        "Referer": "http://finance.ifeng.com/app/hq/"
    }

    # connect timeout in seconds
    CONNECT_TIMEOUT = 0.1

    # read timeout in seconds
    READ_TIMEOUT = 0.2

    # timeout tuple for requests
    TIMEOUT = (CONNECT_TIMEOUT, READ_TIMEOUT)


config = _Config


class _Log:
    _lck = threading.Lock()

    @staticmethod
    def log(msg):
        """
            print log
        :param msg:
        :return:
        """
        if config.LOG:
            _Log._lck.acquire()
            print(msg)
            _Log._lck.release()

log = _Log

class _Path:
    """
            make request path
        """

    @staticmethod
    def getse(code):
        """
            get securities exchange of specified stock by code
        :param code: str, stock code
        :return:
            sz, sh or None
        """
        # stock code rules
        codes = {
            "sh": ['600', '601', '603'],
            "sz": ['000', '002', '300']
        }

        if len(code) < 3:
            return None

        code = code[:3]
        for se in codes.keys():
            if code in codes[se]:
                return se

        return None

    @staticmethod
    def addse(codes):
        """
            add securities exchange flag before stock codes, like: 000001->sz000001
        :param codes: array, stock codes
        :return:
            array, stock codes with exchange flag
        """
        ncodes = []
        for code in codes:
            ncodes.append(_Path.getse(code)+code)
        return ncodes

    @staticmethod
    def make(codes):
        """
            make request url by stock codes
        :param codes:
        :return:
        """
        # make path
        path = "/q.php?l="

        return path + ",".join(_Path.addse(codes)) + "&f=json&r=" + str(random.random())


path = _Path


class _Parser:
    """
        parser for ifeng quote response
    """
    @staticmethod
    def tidy(quote):
        """
            tidy quote data
        :param quote:
        :return:
        """
        # prices
        prices = ["jkj", "zsj", "dqj", "zgj", "zdj", "cje", "mrj1", "mrj2", "mrj3", "mrj4", "mrj5", "mcj1", "mcj2", "mcj3", "mcj4", "mcj5"]

        # volumes
        volumes = ["cjl", "mrl1", "mrl2", "mrl3", "mrl4", "mrl5", "mcl1", "mcl2", "mcl3", "mcl4", "mcl5"]

        # tidy prices
        for p in prices:
            if quote.get(p) is not None:
                quote[p] = quote[p]  # str(decimal.Decimal(quote[p]).quantize(decimal.Decimal('0.00')))

        # tidy volumes
        for v in volumes:
            if quote.get(v) is not None:
                quote[v] = math.floor(int(quote[v]) / 100)

        return quote

    def parse(text):
        """
            parse response text
        :param text:
        :return:
        """
        # parse results
        results = []

        # alias for item
        alias = {
            "jkj": 4, "zsj": 1, "dqj": 0, "zgj": 5, "zdj": 6,
            "cjl": 9, "cje": 10,
            "mrl1": 16, "mrj1": 11, "mrl2": 17, "mrj2": 12, "mrl3": 18, "mrj3": 13, "mrl4": 19, "mrj4": 14, "mrl5": 20, "mrj5": 15,
            "mcl1": 26, "mcj1": 21, "mcl2": 27, "mcj2": 22, "mcl3": 28, "mcj3": 23, "mcl4": 29, "mcj4": 24, "mcl5": 30, "mcj5": 25,
            "time": 34,
        }

        # parse all response quotes
        rpos = text.find('=') + 1
        text = text[rpos:].rstrip().rstrip(';')
        quotes = json.loads(text)

        # parse each quote
        for stock in quotes:
            # stock code
            code = stock[-6:]

            # quote items
            items = quotes[stock]

            qte = {}
            # stock quote
            for k in alias:
                qte[k] = items[alias[k]]

            # translate time from unix timestamp to datetime
            qte['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(qte['time']))

            # tidy quote
            qte = _Parser.tidy(qte)

            # compute ztj&dtj
            qte['ztj'] = round(qte['zsj'] * 1.1, 2)
            qte['dtj'] = round(qte['zsj'] * 0.9, 2)

            # add to results
            results.append(qte)

        return results


parser = _Parser


class _Quote:
    """
        get tick quote data
    """
    @staticmethod
    def get(code):
        # base url
        BASEURL = "http://" + config.HOST

        # quote url for @code
        url = BASEURL + path.make([code])

        # request data from url
        resp = requests.get(url, headers=config.HEADERS, timeout=config.TIMEOUT)

        # parse response
        results = parser.parse(resp.text)

        # return result
        return results[0]


quote = _Quote


class _Util:
    @staticmethod
    def now():
        """
            get now time YYYYmmdd HH:MM:SS
        :return:
        """
        return time.strftime('%Y%m%d %H:%M:%S', time.localtime())

    @staticmethod
    def today():
        """
            get today YYYYmmdd string
        :return:
        """
        return time.strftime('%Y%m%d', time.localtime())

    @staticmethod
    def is_trading_day():
        """
            check if current time is trading day, !!!Note: exclude holiday later!!!
        :return:
        """
        if config.TEST:
            return True

        # get current local time
        ltm = time.localtime()

        # trading day week[1~5]
        if ltm.tm_wday < 5:
            return True

        return False


    @staticmethod
    def is_trading_hours():
        """
            check current time is trading hours
        :return:
        """
        if config.TEST:
            return True


        # get current local time
        ltm = time.localtime()

        # trading hours [9:30~11:30, 13:00~15:00]
        if ltm.tm_hour in [10, 13, 14] or (ltm.tm_hour == 9 and ltm.tm_min >= 30 and ltm.tm_min < 60) or (ltm.tm_hour == 11 and ltm.tm_min <=30):
            return True

        return False


util = _Util


class _Quoter(threading.Thread):
    """
        quoter for record tick data
    """
    def __init__(self, stockcode, datadir, interval, finterval):
        """
            init quote recorder
        :param stockcode:
        :param datadir:
        :param interval:
        :param finterval:
        """
        # init parent
        threading.Thread.__init__(self)

        # init arguments
        self._stockcode = stockcode
        self._datadir = datadir + '/' + stockcode
        self._interval = interval
        self._finterval = finterval

        # last flush timestamp
        self._last_flush_tm = time.time()

        # tick data array
        self._data = []

        # make output data directory
        os.makedirs(self._datadir, exist_ok=True)

    def flush(self):
        """

        :return:
        """
        # flush condition
        if len(self._data) == 0:
            log.log('%s:[%s] flush, no records.' % (util.now(), self._stockcode))
            return

        if time.time() - self._last_flush_tm < self._finterval:
            log.log('%s:[%s] flush, interval not satisfied.' % (util.now(), self._stockcode))
            return

        # current data file
        outfile = self._datadir + '/' + util.today()

        # flush tick data to file
        with open(outfile, 'a') as outer:
            outer.writelines(self._data)
            outer.flush()

        # print flush information
        log.log("%s:[%s] flush %d records" % (util.now(), self._stockcode, len(self._data)))

        # clear data
        self._data.clear()

        # update last flush timestamp
        self._last_flush_tm = time.time()

    def fetch(self):
        """

        :return:
        """
        # fetch condition
        if not util.is_trading_day() or not util.is_trading_hours():
            log.log('%s:[%s] fetch, not trading hours.' % (util.now(), self._stockcode))
            return

        # fetch data
        data = quote.get(self._stockcode)

        # save data
        self._data.append(str(data)+"\n")

        # print fetch information
        log.log('%s:[%s] fetch 1 record' % (util.now(), self._stockcode))

    def run(self):
        """
            run quote recorder
        :return:
        """
        while True:
            try:
                # fetch tick data
                self.fetch()

                # flush tick data
                self.flush()
            except Exception as e:
                print(e)

            # sleep for next fetch
            time.sleep(self._interval)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('usage: python quote.py <stock-codes> <data-directory> <tick-interval-seconds> <flush-interval-seconds>\n'
              'example: python quote.py 000100,000320 ./data 5 300\n')
        exit(0)

    # get arguments
    stockcodes, datadir, interval, finterval = sys.argv[1].split(','), sys.argv[2], sys.argv[3], sys.argv[4]

    # run quoter for each stock
    for stockcode in stockcodes:
        # init quoter
        quoter = _Quoter(stockcode, datadir, int(interval), int(finterval))

        # start recording
        quoter.start()

        # sleep a while for next quoter
        time.sleep(1)

    # sleep for ever
    while True:
        time.sleep(100)
