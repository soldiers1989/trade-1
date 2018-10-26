"""
    general configure for fetch data from sina
"""


class _VSFSina:
    # base url list for vip stock
    baseurls = [
        'http://vip.stock.finance.sina.com.cn'
    ]

    # headers for request
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Host": "vip.stock.finance.sina.com.cn",
        "Referer": "http://vip.stock.finance.sina.com.cn/mkt/"
    }

    # http client init args
    client = {
        'maxfailed': 3,
        'retry': 3,
        'timeout': (2, 15) # timeout for requests in seconds, (connect timeout, read timeout)
    }

    # next page request interval, in seconds
    page_interval = 1

vsf = _VSFSina


class _HQSinajs:
    # base url list for quote
    baseurls = [
        'http://hq.sinajs.cn'
    ]

    # headers for request
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Host": "hq.sinajs.cn",
        "Referer": "http://vip.stock.finance.sina.com.cn/mkt/"
    }

    # http client init args
    client = {
        'maxfailed': 3,
        'retry': 3,
        'timeout': (2, 15) # timeout for requests in seconds, (connect timeout, read timeout)
    }

hqjs = _HQSinajs

