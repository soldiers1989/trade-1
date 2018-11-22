from .. import protocol, handler, access


class NotifyHandler(handler.Handler):
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
        results = None

        self.write(protocol.success(data=results))

