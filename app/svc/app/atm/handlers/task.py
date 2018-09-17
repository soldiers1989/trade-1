from .. import handler, access, tasks, protocol


class SyncSinaAllStock(handler.Handler):
    """
        handler for query timer task status
    """
    @access.exptproc
    def get(self):
        """
            get quote service status
        :return:
        """
        # get callback url
        url = self.get_argument('callback', None)

        # start a new sync task
        task = tasks.stock.SyncSinaAllStock(url)
        task.start()

        self.write(protocol.success())


class SyncCNInfoAllStock(handler.Handler):
    """
        handler for query timer task status
    """
    @access.exptproc
    def get(self):
        """
            get quote service status
        :return:
        """
        # get callback url
        url = self.get_argument('callback', None)

        # start a new sync task
        task = tasks.stock.SyncCNInfoAllStock(url)
        task.start()

        self.write(protocol.success())


