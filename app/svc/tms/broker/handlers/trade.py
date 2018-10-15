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

        secex.trade.default.start(**config)


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
        pass


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
        pass


class LoginHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """

        :return:
        """
        pass


class LogoutHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """

        :return:
        """
        pass


class TransferHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """

        :return:
        """
        pass


class QueryHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """

        :return:
        """
        pass


class PlaceHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """

        :return:
        """
        pass


class CancelHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """

        :return:
        """
        pass


class ClearHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """

        :return:
        """
        pass
