from app.atm import handler, access, protocol


class SyncAll(handler.Handler):
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
        pass
