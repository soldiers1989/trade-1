from .. import remote, handler, access, protocol, error


class Add(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get quote service status
        :return:
        """
        # get task id
        id, name, cond, url, method = self.get_argument('id'), self.get_argument('name'), self.get_argument('cond'), self.get_argument('url'), self.get_argument('method')
        exclusive, maxkeep = self.get_argument('exclusive', True), self.get_argument('maxkeep', 20)

        # check task existence
        if remote.taskmanager.exist(id):
            self.write(protocol.failed(msg='task with id %s has exist.' % (str(id))))
            return

        # add new task
        remote.taskmanager.add(id, name, cond, url, method, exclusive=exclusive, maxkeep=maxkeep)

        # response
        self.write(protocol.success())


    @access.exptproc
    @access.needtoken
    def post(self):
        # get task id
        id, name, cond, url, method, data = self.get_argument('id'), self.get_argument('name'), self.get_argument('cond'), self.get_argument('url'), self.get_argument('method'), self.get_argument('data', None)
        exclusive, maxkeep = self.get_argument('exclusive', True), self.get_argument('maxkeep', 20)

        # check task existence
        if remote.taskmanager.exist(id):
            self.write(protocol.failed(msg='task with id %s has exist.' % (str(id))))
            return

        # get data from body
        body = self.request.body.decode() if self.request.body is not None else None

        # add new task
        if data == 'json':
            remote.taskmanager.add(id, name, cond, url, method, exclusive=exclusive, maxkeep=maxkeep, json=body)
        elif data == 'data':
            remote.taskmanager.add(id, name, cond, url, method, exclusive=exclusive, maxkeep=maxkeep, data=body)
        else:
            raise error.post_data_not_support

        # response
        self.write(protocol.success())


class Delete(handler.Handler):
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

        # check task existence
        if not remote.taskmanager.exist(id):
            self.write(protocol.failed(msg='task with id %s not exist.' % (str(id))))
            return

        # delete task
        remote.taskmanager.delete(id)

        # response
        self.write(protocol.success())


class Clear(handler.Handler):
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
        # clear task
        remote.taskmanager.clear()

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

        # check task existence
        if not remote.taskmanager.exist(id):
            self.write(protocol.failed(msg='task with id %s not exist.' % (str(id))))
            return

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

        # check task existence
        if not remote.taskmanager.exist(id):
            self.write(protocol.failed(msg='task with id %s not exist.' % (str(id))))
            return

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

        # check task existence
        if not remote.taskmanager.exist(id):
            self.write(protocol.failed(msg='task with id %s not exist.' % (str(id))))
            return

        # enable task
        remote.taskmanager.execute(id)

        # response
        self.write(protocol.success())


class Callback(handler.Handler):
    """
       callbank for remote task execute results
    """
    @access.exptproc
    def get(self):
        """
            remote callback
        :return:
        """
        # get parameters
        id, seq, status, result = self.get_argument('id'), self.get_argument('seq'), self.get_argument('status'), self.get_argument('result')

        # check input parameters
        if not seq.isdigit() or status not in ['0', '1']:
            raise error.invalid_parameters

        # check task existence
        if not remote.taskmanager.exist(id):
            self.write(protocol.failed(msg='task with id %s not exist.' % (str(id))))
            return

        # notify task results
        remote.taskmanager.notify(id, int(seq), bool(int(status)), result)

        self.write(protocol.success())


    @access.exptproc
    def post(self):
        return self.get()


class Status(handler.Handler):
    """
        handler for query timer task status information
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

        # check task existence
        if id is not None and not remote.taskmanager.exist(id):
            self.write(protocol.failed(msg='task with id %s not exist.' % (str(id))))
            return

        # get timer task status
        results = remote.taskmanager.status(id)

        # make response data
        data = {
            'total': len(results),
            'rows': results
        }

        # response
        self.write(protocol.success(data=data))


class Detail(handler.Handler):
    """
        handler for query timer task detail information
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

        # check task existence
        if not remote.taskmanager.exist(id):
            self.write(protocol.failed(msg='task with id %s not exist.' % (str(id))))
            return

        # get timer task status
        results = remote.taskmanager.detail(id)

        # make response data
        data = {
            'total': len(results),
            'rows': results
        }

        # response
        self.write(protocol.success(data=data))