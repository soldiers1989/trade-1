from lib.stock.quote.daily import quotes
from xpinyin import Pinyin

if __name__ == "__main__":
    p = Pinyin()
    print(p.get_initials(u'中国建工', u''))
    exit(0)
    q = quotes.Quotes()
    results = q.fetch('2018-07-24')
    print(len(results))

