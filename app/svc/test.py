from lib.stock.quote import icaopan, emoney, ifeng, sina

if __name__ == "__main__":
    q = icaopan.quote.ICaopanQuote()
    res = q.gets(['000100','000001'])
    print(res)

    q = sina.quote.SinaQuote()
    res = q.gets(['000100','000001'])
    print(res)

    q = ifeng.quote.IfengQuote()
    res = q.gets(['000100','000001'])
    print(res)

    q = emoney.quote.EmoneyQuote()
    res = q.gets(['000100','000001'])
    print(res)
