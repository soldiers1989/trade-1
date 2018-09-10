from app.quote import handler, quoter, protocol


class QueryStatus(handler.Handler):
    """
        handler for query quote service status
    """
    def get(self):
        """
            get quote service status
        :return:
        """
        try:
            data = quoter.default.status()
            self.write(protocol.success(data=data))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class QueryCurrent(handler.Handler):
    """
        handler for query current quote of stock
    """
    def get(self):
        """
            get quote
        :return:
        """
        try:
            codes = self.get_argument('code').split(',')
            if len(codes) == 1:
                data = quoter.default.get(codes[0])
            else:
                data = quoter.default.gets(codes)

            self.write(protocol.success(data=data))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))
