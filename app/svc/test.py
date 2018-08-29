#from lib.stock.quote.daily import quotes
from lib.stock.quote.level5 import quotes
import threading, time

class T(threading.Thread):
    id = "abc"
    name = "123"
    def run(self):
        print('hello')

if __name__ == "__main__":
    print(quotes.get('000100'))
    exit(0)

    t = T()
    t.start()

    t.join()
    print(t.id)
    print(t.name)

    print(T.id)
    print(T.name)

    time.sleep(3)
