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
        data = quoter.default.status()
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
            data = quoter.default.get(codes[0])
        else:
            data = quoter.default.gets(codes)

        self.write(protocol.success(data=data))

