from sec.stock.quote import sina
from sec.stock.quote import ifeng
from sec.stock.quote import emoney

from sec.stock.quote import quotes

if __name__ == "__main__":
    qsina = sina.quote.SinaQuote(['219.142.78.212', '202.108.37.102', '140.249.5.59'])
    res = qsina.gets(['000001'])
    print(res)

    qifeng = ifeng.quote.IfengQuote()
    res = qifeng.gets(['000001'])
    print(res)

    qemoney = emoney.quote.EmoneyQuote()
    res = qemoney.gets(['000001'])
    print(res)

    qs = quotes.Quotes()
    res = qs.gets(['000001', '600036'])
    print(res)

    a = qs.status('sina')
    print(a)