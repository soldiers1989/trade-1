# ease money id/name
ID = 'icaopan'
NAME = '爱操盘'

# eastmoney quote server host
HOSTS = [
    "md.icaopan.com"
]

# request headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Host": "md.icaopan.com",
}

# connect timeout in seconds
CONNECT_TIMEOUT = 0.1


# read timeout in seconds
READ_TIMEOUT = 0.2


# timeout tuple for requests
TIMEOUT = (CONNECT_TIMEOUT, READ_TIMEOUT)


# max hosts continues failed times before disabled
MAXFAILED = 3

# retry count for get quote when failed
RETRY = 3
