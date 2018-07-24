from lib.stock.quote.daily import quotes

if __name__ == "__main__":
    q = quotes.Quotes()
    results = q.fetch('2018-07-24')
    print(len(results))