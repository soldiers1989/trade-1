"""
    config for get stock detail from sina
"""


# url for stock list
URL = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?sort=symbol&asc=1&symbol=&_s_r_a=page&num=40&page=%d&node=hs_a#"


# headers for request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Host": "vip.stock.finance.sina.com.cn",
    "Referer": "http://vip.stock.finance.sina.com.cn/mkt/"
}

# connect timeout in seconds
CONNECT_TIMEOUT = 0.5


# read timeout in seconds
READ_TIMEOUT = 10


# timeout tuple for requests
TIMEOUT = (CONNECT_TIMEOUT, READ_TIMEOUT)

# max pages
MAX_PAGES = 120

# interval for fetch next page in seconds
INTERVAL = 1