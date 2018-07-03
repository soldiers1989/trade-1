from app.api import access, models, handler, protocol


class UserBuyHandler(handler.Handler):
    """
        handler for query quote service status
    """
    @access.protect
    def get(self):
        """
            get quote service status
        :return:
        """
        try:

            self.write(protocol.success(data=''))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))


class UserSellHandler(handler.Handler):
    """
        handler for query quote service status
    """
    @access.protect
    def get(self):
        """
            get quote service status
        :return:
        """
        try:
            self.write(protocol.success(data=''))
        except Exception as e:
            self.write(protocol.failed(msg=str(e)))
