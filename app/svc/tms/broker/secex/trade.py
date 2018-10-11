"""
    base class for trade service
"""
import threading
from . import quote


class TradeAccount:
    def __init__(self, user, pwd, money, **kwargs):
        """
            init  trade account
        :param args:
        :param kwargs:
        """
        self._user = user
        self._pwd = pwd
        self._money = money
        self._orders = []


class TradeService(threading.Thread):
    def __init__(self, *args, **kwargs):
        """
            init trading service
        """
        #
        super().__init__(self)

    def register(self):
        """
            register a trade account
        :return:
        """
        pass

    def login(self):
        """
            trade account login
        :return:
        """
        pass

    def logout(self):
        """
            trade account logout
        :return:
        """
        pass

    def transfer(self):
        """
            transfer money in/out from trade account
        :return:
        """
        pass

    def query(self):
        """
            query account information
        :return:
        """
        pass

    def place(self):
        """
            place an order
        :return:
        """
        pass

    def cancel(self):
        """
            cancel an order
        :return:
        """
        pass

    def list(self):
        """
            list all account information including orders
        :return:
        """
        pass

    def clear(self):
        """
            clear orders of account
        :return:
        """
        pass

    def dealt(self):
        """
            make dealt of an order
        :return:
        """
        pass

    def canceled(self):
        """
            make canceled of an order
        :return:
        """
        pass
