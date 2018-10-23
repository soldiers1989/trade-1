from .. import quoter, protocol, handler, access


class QueryStatus(handler.Handler):
    """
        handler for query quote service status
    """
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get quote service status
        :return:
        """
        data = {
            'level5': quoter.level5.status(),
            'daily': quoter.daily.status()
        }
        self.write(protocol.success(data=data))


class QueryCurrent(handler.Handler):
    """
        handler for query current quote of stock
    """
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get quote
        :return:
        """
        codes = self.get_argument('code').split(',')
        if len(codes) == 1:
            data = quoter.level5.get(codes[0])
        else:
            data = quoter.level5.gets(codes)

        self.write(protocol.success(data=data))


class QueryLevel5(handler.Handler):
    """
        handler for query current quote of stock
    """
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get quote
        :return:
        """
        codes = self.get_argument('code').split(',')
        if len(codes) == 1:
            data = quoter.level5.get(codes[0])
        else:
            data = quoter.level5.gets(codes)

        self.write(protocol.success(data=data))


class QueryDaily(handler.Handler):
    """
        handler for query current quote of stock
    """
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get quote
        :return:
        """
        # get date
        date = self.get_argument('date')

        # get daily data
        data = quoter.daily.get(date)

        # response daily data
        self.write(protocol.success(data=data))
