from sec.stock.quote import sina
from sec.stock.quote import tdx


if __name__ == "__main__":
    qsina = sina.quote.SinaQuote(['219.142.78.212', '202.108.37.102', '140.249.5.59'])
    res = qsina.gets(['000001'], 2)
    print(res)

    qtdx = tdx.quote.TdxQuote("172.16.21.135", 80, [("175.6.5.153", 7709),("123.125.108.90",7709)])
    res = qtdx.gets(['000001'])
    print(res)