"""
    tdx trade service api wrapper
"""
from . import error, remote, type


class Tdx:
    def __init__(self, host, port):
        """
            init tdx trade object with remote http service host and port
        :param host: remote http service host
        :param port: remote http service port
        """
        self._remote = remote.Remote(host, port)

    def login(self, account, pwd, ip, port, dept, version):
        """
            account login
        :param account:
        :param pwd:
        :param ip:
        :param port:
        :param dept:
        :param version:
        :return:
            (True|False, result message string)
        """
        # check parameters
        if not (account and pwd and ip and port and dept and version) :
            return False, error.INVALID_PARAMETERS

        try:
            # remote login
            bres, msg = self._remote.login(account, pwd, ip, port, dept, version)

            # login return with remote response
            return bres, msg
        except Exception as e:
            # login failed with exception
            return False, str(e)

    def query_gddm(self, account):
        """
            query gddm
        :param account:
        :return:
        """
        # check parameters
        if not account:
            return False, error.INVALID_PARAMETERS

        try:
            # remote query gddm
            bres, msg, data = self._remote.query1(account, type.category.gddm)

            # remote query failed
            if not bres:
                return False, msg

            # format remote query result


        except Exception as e:
            # query gddm failed with exception
            return False, str(e)



    def query1(self, account, type):
        """
            query current information of account
        :param account:
        :param type:
        :return:
        """
        #check parameters
        if not (account and type):
            return False, error.INVALID_PARAMETERS, []

        #remote query
        status, msg, data = self._remote.query1(account, type);




    def query2(self, account, type, startdate, enddate):
        """
            query history information of account
        :param account:
        :param type:
        :param startdate:
        :param enddate:
        :return:
        """
        pass


    def quote(self, account, code):
        """
            query current quote of code
        :param account:
        :param code:
        :return:
        """
        pass

    def order(self, account, otype, ptype, gddm, zqdm, price, count):
        """
            send an order
        :param account:
        :param otype:
        :param ptype:
        :param gddm:
        :param zqdm:
        :param price:
        :param count:
        :return:
        """
        pass

    def cancel(self, account, seid, orderno):
        """
            cancel an order
        :param account:
        :param seid:
        :param orderno:
        :return:
        """
        pass

    def logout(self, account):
        """
            account logout
        :param account:
        :return:
            (True|False, result message string)
        """
        #check parameters
        if not account:
            return False, error.INVALID_PARAMETERS

        #remote logout
        return self._remote.logout(account)



if __name__ == "__main__":
    from lib.trade.tdx.type import category

    print(category.gddm)