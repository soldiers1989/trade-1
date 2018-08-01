from lib.stock.quote.daily import quotes
import threading, time

class T(threading.Thread):
    id = "abc"
    name = "123"
    def run(self):
        print('hello')

if __name__ == "__main__":
    t = T()
    t.start()

    t.join()
    print(t.id)
    print(t.name)

    print(T.id)
    print(T.name)

    time.sleep(3)
