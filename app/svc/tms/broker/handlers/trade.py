from .. import handler, access, protocol, error


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


class ListHandler(handler.Handler):
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


class DealtHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """

        :return:
        """
        pass


class CanceledHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """

        :return:
        """
        pass
