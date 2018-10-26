"""
    general configure for fetch data from ifeng
"""


class _APIFinance:
    # base url list for vip stock
    baseurls = [
        'http://api.finance.ifeng.com'
    ]

    # headers for request
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Host": "api.finance.ifeng.com",
        "Referer": "http://finance.ifeng.com/"
    }

    # http client init args
    client = {
        'maxfailed': 3,
        'retry': 3,
        'timeout': (2, 15) # timeout for requests in seconds, (connect timeout, read timeout)
    }

apifinance = _APIFinance
