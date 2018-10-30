from .. import smd, protocol, handler, access


class List(handler.Handler):
    """
        get stock list
    """
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get quote service status
        :return:
        """
        # get arguments
        args = self.cleaned_arguments

        # get stock list
        results = smd.api.stock.get_list(**args)

        self.write(protocol.success(data=results))


class Quote(handler.Handler):
    """
        get current stock quote
    """
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get quote
        :return:
        """
        # get arguments
        args = self.cleaned_arguments

        # get current quote data
        results = smd.api.stock.get_quote(**args)

        self.write(protocol.success(data=results))


class Ticks(handler.Handler):
    """
        get tick data
    """
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        # get arguments
        args = self.cleaned_arguments

        # get tick data
        results = smd.api.stock.get_ticks(**args)

        self.write(protocol.success(data=results))


class KLine(handler.Handler):
    """
        get kline-data
    """
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get
        :return:
        """
        # get arguments
        args = self.cleaned_arguments

        # get kline-data
        results = smd.api.stock.get_kline(**args)

        self.write(protocol.success(data=results))