"""
    general configure for fetch data from eastmoney
"""


class _Nuff:
    # base url list for md
    baseurls = [
        'http://nuff.eastmoney.com'
    ]

    # headers for request
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Host": "nuff.eastmoney.com",
    }

    # http client init args
    client = {
        'maxfailed': 3,
        'retry': 3,
        'timeout': (2, 15) # timeout for requests in seconds, (connect timeout, read timeout)
    }

nuff = _Nuff


