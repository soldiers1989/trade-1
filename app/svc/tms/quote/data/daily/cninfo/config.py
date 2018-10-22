# cninfo quote id/name
ID = 'cninfo'
NAME = '巨潮网'

# remote hosts/ips
HOSTS = [
    'webapi.cninfo.com.cn'
]

PATHS = [
    '/api/sysapi/p_sysapi1007?format=json&market=SZE&tdate=%s',
    '/api/sysapi/p_sysapi1007?format=json&market=SHE&tdate=%s',
]

HOST = 'webapi.cninfo.com.cn'
REFERER = 'http://webapi.cninfo.com.cn/'


# sina quote server host

# sina quote request headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Host": HOST,
    "Referer": REFERER
}


# connect timeout in seconds
CONNECT_TIMEOUT = 0.5


# read timeout in seconds
READ_TIMEOUT = 15


# timeout tuple for requests
TIMEOUT = (CONNECT_TIMEOUT, READ_TIMEOUT)


# max hosts continues failed times before disabled
MAXFAILED = 3

# retry count for get quote when failed
RETRY = 3
