#from lib.stock.quote.daily import quotes
from lib.stock.quote.level5 import quotes
import threading, time

class T(threading.Thread):
    id = "abc"
    name = "123"
    def run(self):
        print('hello')


class Stm:
    def __init__(self):
        pass

    def __enter__(self):
        print('enter')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit')


if __name__ == "__main__":
    with Stm():
        print('statement')
        raise Exception('error')
