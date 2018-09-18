from .. import handler, access, tasks, protocol


class SyncAllHandler(handler.Handler):
    """
        sync stocks from source
    """
    @access.exptproc
    def get(self, *args, **kwargs):
        # get callback url
        url = self.get_argument('callback', None)

        # start a new sync task
        task = tasks.stock.SyncAll(url)
        task.start()

        self.write(protocol.success())
