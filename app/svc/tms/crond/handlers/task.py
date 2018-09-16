from .. import remote, handler, access, protocol


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
        results = remote.taskmanager.status(id)

        # make response data
        data = {
            'total': len(results),
            'rows': results
        }

        # response
        self.write(protocol.success(data=data))


class Add(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get quote service status
        :return:
        """
        # get task id
        id, name, cond, url = self.get_argument('id'), self.get_argument('name'), self.get_argument('cond'), self.get_argument('url')

        # add new task
        remote.taskmanager.add(id, name, cond, url)

        # response
        self.write(protocol.success())


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
        remote.taskmanager.enable(id)

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
        remote.taskmanager.disable(id)

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
        remote.taskmanager.execute(id)

        # response
        self.write(protocol.success())


class Callback(handler.Handler):
    """
       callbank for remote task execute results
    """
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            remote callback
        :return:
        """
        id, seq, status, result = self.get_argument('id'), self.get_argument('seq'), self.get_argument('status'), self.get_argument('result')

        remote.taskmanager.notify(id, seq, status, result)

        self.write(protocol.success())


    @access.exptproc
    @access.needtoken
    def post(self):
        return self.get()