"""

"""


# query categories
categories = { "zj" : "0", "gf" : "1", "drwt" : "2", "drcj" : "3", "kcwt" : "4", "gddm" : "5", "rzye" : "6", "rqye" : "7", "krzq" : "8", "lswt" : "0",  "lscj":"1", "jgd":"2"}


class category:
    """
        query category
    """
    # current query category
    zj = categories["zj"]
    gf = categories["gf"]
    drwt = categories["drwt"]
    drcj = categories["drcj"]
    kcwt = categories["kcwt"]
    gddm = categories["gddm"]
    rzye = categories["rzye"]
    rqye = categories["rqye"]
    krzq = categories["krzq"]

    # history query category
    lswt = categories["lswt"]
    lscj = categories["lscj"]
    jgd = categories["jgd"]


# stock exchanges code
ses = {"shanghai" : "0", "shenzhen" : "1", "shenzhenzs" : "2"}


class se:
    """
        stock exchange code
    """
    shanghai = ses["shanghai"]
    shenzhen = ses["shenzhen"]
    shenzhenzs = ses["shenzhenzs"]


# order types
orders = {"mr" : "0", "mc" : "1", "rzmr" : "2", "rqmc" : "3", "mqhq" : "4", "mqhk" : "5", "xqhq" : "6"}


class order:
    """
        order type
    """
    mr = orders["mr"]
    mc = orders["mc"]
    rzmr = orders["rzmr"]
    rqmc = orders["rqmc"]
    mqhq = orders["mqhq"]
    mqhk = orders["mqhk"]
    xqhq = orders["xqhq"]


# price types
prices = {"xjwt" : "0", "sjdfzy" : "1", "sjbfzy" : "2", "sjjscj" : "3", "sj5dcc" : "4", "sjqbcc" : "5", "sj5dcx" : "6"}


class price:
    """
        price type
    """
    xjwt = prices["xjwt"]
    sjdfzy = prices["sjdfzy"]
    sjbfzy = prices["sjbfzy"]
    sjjscj = prices["sjjscj"]
    sj5dcc = prices["sj5dcc"]
    sjqbcc = prices["sjqbcc"]
    sj5dcx = prices["sj5dcx"]
