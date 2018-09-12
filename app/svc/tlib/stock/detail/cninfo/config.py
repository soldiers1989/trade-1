"""
    config for get stock detail from sina
"""


# url for stock list
URL = "http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1007?format=json&market=%s&tdate=%s"

# market codes in url
MARKETS = ['SHE', 'SZE']

# headers for request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Host": "webapi.cninfo.com.cn",
    "Referer": "http://webapi.cninfo.com.cn/"
}

# connect timeout in seconds
CONNECT_TIMEOUT = 0.5


# read timeout in seconds
READ_TIMEOUT = 10


# timeout tuple for requests
TIMEOUT = (CONNECT_TIMEOUT, READ_TIMEOUT)
