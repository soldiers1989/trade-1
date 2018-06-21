from sec.stock.quote.sina import quote

if __name__ == "__main__":
    q = quote.SinaQuote()
    res = q.gets(['000001', '000100'])
    print(res)