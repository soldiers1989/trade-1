"""
    general configure for fetch data from shse
"""


class _Query:
    # base url list for vip stock
    baseurls = [
        'http://query.sse.com.cn'
    ]

    # headers for request
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Host": "query.sse.com.cn",
        "Referer": "http://www.sse.com.cn/"
    }

    # http client init args
    client = {
        'maxfailed': 3,
        'retry': 3,

        'headers': headers,
        'timeout': (2, 15) # timeout for requests in seconds, (connect timeout, read timeout)
    }

query = _Query


