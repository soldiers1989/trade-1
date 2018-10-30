import json
from .. import handler, access, protocol, error, secex


class StartHandler(handler.Handler):
    """
        start trade service
    """
    @access.exptproc
    @access.needtoken
    def post(self):
        """

        :return:
        """
        if self.request.body is None:
            raise error.missing_parameters

        # get config from post json data
        config = json.loads(self.request.body.decode())
        # start trade service
        secex.trade.default.start(**config)

        self.write(protocol.success())


class StopHandler(handler.Handler):
    """
        start trade service
    """
    @access.exptproc
    @access.needtoken
    def post(self):
        """

        :return:
        """
        secex.trade.default.stop()
        self.write(protocol.success())


class StatusHandler(handler.Handler):
    """
        get trade service status
    """
    @access.exptproc
    @access.needtoken
    def post(self):
        """

        :return:
        """
        result = secex.trade.default.status()
        self.write(protocol.success(data=result))


class RegisterHandler(handler.Handler):
    """
        register an account to broker
    """
    @access.exptproc
    @access.needtoken
    def post(self):
        """

        :return:
        """
        # get config from post json data
        config = self.cleaned_arguments
        # start trade service
        result = secex.trade.default.register(**config)

        self.write(protocol.success(data=result))


class LoginHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """

        :return:
        """
        account, pwd = self.get_argument('account'), self.get_argument('pwd')
        result = secex.trade.default.login(account, pwd)
        self.write(protocol.success(data=result))


class LogoutHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """

        :return:
        """
        account = self.get_argument('account')
        result = secex.trade.default.logout(account)
        self.write(protocol.success(data=result))


class TransferHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """

        :return:
        """
        account, money = self.get_argument('account'), self.get_argument('money')
        result = secex.trade.default.transfer(account, money)
        self.write(protocol.success(data=result))


class QueryHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """

        :return:
        """
        account, type, sdate, edate = self.get_argument('account'), self.get_argument('type'), self.get_argument('sdate', None), self.get_argument('edate', None)
        result = secex.trade.default.query(account, type, sdate, edate)
        self.write(protocol.success(data=result))


class PlaceHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """

        :return:
        """
        account, symbol, otype, ptype, oprice, ocount  = self.get_argument('account'), self.get_argument('symbol'), self.get_argument('otype'), self.get_argument('ptype'), self.get_argument('oprice'), self.get_argument('ocount')
        result = secex.trade.default.place(account, symbol, otype, ptype, oprice, ocount)
        self.write(protocol.success(data=result))


class CancelHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """

        :return:
        """
        account, ocode = self.get_argument('account'), self.get_argument('ocode')
        result = secex.trade.default.cancel(account, ocode)
        self.write(protocol.success(data=result))


class ClearHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
        :return:
        """
        account = self.get_argument('account', None)
        result = secex.trade.default.clear(account)
        self.write(protocol.success(data=result))
