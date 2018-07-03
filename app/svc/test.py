from lib.stock.quote import icaopan, emoney, ifeng, sina

class A:
    def __init__(self):
        print('init')

    def __del__(self):
        print('del')

class B:
    def __init__(self):
        self._a = A()

if __name__ == "__main__":
    """q = icaopan.quote.ICaopanQuote()
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
    print(res)"""

    b = B()

    del b