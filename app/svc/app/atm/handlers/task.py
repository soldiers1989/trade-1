from app.atm import timer, handler, access, protocol


class Status(handler.Handler):
    """
        handler for query timer task status
    """
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get quote service status
        :return:
        """
        # get task id
        id = self.get_argument('id', None)

        # get timer task status
        results = timer.default.status(id)

        # make response data
        data = {
            'total': len(results),
            'rows': results
        }

        # response
        self.write(protocol.success(data=data))


class Enable(handler.Handler):
    """
        handler for enable a timer task
    """
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get quote service status
        :return:
        """
        # get task id
        id = self.get_argument('id')

        # enable task
        timer.default.enable(id)

        # response
        self.write(protocol.success())


class Disable(handler.Handler):
    """
        handler for disable a timer task
    """
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get quote service status
        :return:
        """
        # get task id
        id = self.get_argument('id')

        # enable task
        timer.default.disable(id)

        # response
        self.write(protocol.success())


class Execute(handler.Handler):
    """
        handler for execute a timer task
    """
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get quote service status
        :return:
        """
        # get task id
        id = self.get_argument('id')

        # enable task
        timer.default.execute(id)

        # response
        self.write(protocol.success())