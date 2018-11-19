import time, json
from .. import remote, handler, access, protocol, models, error


class List(handler.Handler):
    """
        handler for query timer task list
    """
    @access.exptproc
    @access.needtoken
    def get(self):
        """
        :return:
        """
        # get query params
        status, words = self.cleaned_arguments.get('status'), self.cleaned_arguments.get('words')

        # get cronds status
        cronds = remote.taskmanager.status()

        # filter results
        results = []
        for crond in cronds:
            if status is not None and status != '' and status != crond['status']:
                continue
            if words is not None and words != '' and (not words in crond['name'] or not words == str(crond['id'])):
                continue
            results.append(crond)

        # make response data
        data = {
            'total': len(results),
            'rows': results
        }

        # response data
        self.write(protocol.success(data=data))


class Load(handler.Handler):
    """
        load all tasks from database
    """
    @access.exptproc
    @access.needtoken
    def post(self):
        """

        :return:
        """
        with models.db.create() as d:
            # get all crond tasks from database
            cronds = models.Crond.all(d)

            # add to task manager
            for crond in cronds:
                # skip exists
                if remote.taskmanager.exist(str(crond.id)):
                   continue

                # add new task
                stopped = True if crond.status=='stopped' else False
                remote.taskmanager.add(str(crond.id), crond.code, crond.name, crond.config, crond.method, crond.url,
                                       data=crond.data, json=crond.json, stopped=stopped, exclusive=crond.exclusive, maxkeep=crond.maxkeep)

            # get all tasks
            results = remote.taskmanager.status()

            # make response data
            data = {
                'total': len(results),
                'rows': results
            }

            # response data
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
        code, name, config, url, method = self.get_argument('code'), self.get_argument('name'), self.get_argument('config'), self.get_argument('url'), self.get_argument('method')
        exclusive, maxkeep = self.get_argument('exclusive', True), self.get_argument('maxkeep', 20)

        with models.db.atomic() as d:
            # add new crond object to database if task has exist
            crond = models.Crond.filter(d, code=code).one()
            if crond is None:
                crond = models.Crond(code=code, name=name, config=config, method=method, url=url, data=None, json=None,
                                     status='stopped', exclusive=exclusive, maxkeep=maxkeep,
                                     ctime=int(time.time()), mtime=int(time.time())).save(d)

            id = str(crond.id)
            # add new task to task manager
            if not remote.taskmanager.exist(id):
                remote.taskmanager.add(id, code, name, config, method, url, exclusive=exclusive, maxkeep=maxkeep, ctime=crond.ctime, mtime=crond.mtime)

            # get the new task
            crond = remote.taskmanager.status(id)

            # response data
            self.write(protocol.success(data=crond))


    @access.exptproc
    @access.needtoken
    def post(self):
        # get task id
        code, name, config, url, method = self.get_argument('code'), self.get_argument('name'), self.get_argument('config'), self.get_argument('url'), self.get_argument('method')
        data, jsons, exclusive, maxkeep = self.get_argument('data', None), self.get_argument('json', None), self.get_argument('exclusive', True), self.get_argument('maxkeep', 20)

        data = data.strip() if data is not None else None
        data = data if data!='' else None
        jsons = jsons.strip() if jsons is not None else None
        jsons = json.dumps(json.loads(jsons)) if jsons is not None and jsons!='' else None

        with models.db.atomic() as d:
            # add new crond object to database if task has exist
            crond = models.Crond.filter(d, code=code).one()
            if crond is None:
                crond = models.Crond(code=code, name=name, config=config, method=method, url=url, data=data, json=jsons,
                                     status='stopped', exclusive=exclusive, maxkeep=maxkeep,
                                     ctime=int(time.time()), mtime=int(time.time())).save(d)

            id = str(crond.id)
            # add new task to task manager
            if not remote.taskmanager.exist(id):
                remote.taskmanager.add(id, code, name, config, method, url, data=data, json=jsons, exclusive=exclusive, maxkeep=maxkeep, ctime=crond.ctime, mtime=crond.mtime)

            # get the new task
            crond = remote.taskmanager.status(id)

            # response data
            self.write(protocol.success(data=crond))


class Delete(handler.Handler):
    """
        handler for delete a timer task
    """
    @access.exptproc
    @access.needtoken
    def post(self):
        """
        :return:
        """
        # get task id
        id = self.get_argument('id')
        # check task existence
        if not remote.taskmanager.exist(id):
            self.write(protocol.failed(msg='task with id %s not exist.' % (str(id))))
            return

        with models.db.atomic() as d:
            # delete task from database
            crond = models.Crond.filter(d, id=id).one()
            if crond is not None:
                crond.delete(d)

            # delete task from task manager
            remote.taskmanager.delete(id)

            # response data
            self.write(protocol.success(data=crond))


class Clear(handler.Handler):
    """
        handler for enable a timer task
    """
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            get quote service status
        :return:
        """
        with models.db.atomic() as d:
            # get all cronds
            cronds = models.Crond.all(d)

            # delete from database
            models.Crond.filter(d).delete()

            # clear task in task manager
            remote.taskmanager.clear()

            # response data
            self.write(protocol.success(data=cronds))


class Enable(handler.Handler):
    """
        handler for enable a timer task
    """
    @access.exptproc
    @access.needtoken
    def post(self):
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

        with models.db.atomic() as d:
            # delete task from database
            crond = models.Crond.filter(d, id=id).one()
            if crond is not None:
                crond.update(status='started')
                crond.save(d)

            # enable task
            remote.taskmanager.enable(id)
            # get task
            crond = remote.taskmanager.status(id)

            # response data
            self.write(protocol.success(data=crond))


class Disable(handler.Handler):
    """
        handler for disable a timer task
    """
    @access.exptproc
    @access.needtoken
    def post(self):
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

        with models.db.atomic() as d:
            # delete task from database
            crond = models.Crond.filter(d, id=id).one()
            if crond is not None:
                crond.update(status='stopped')
                crond.save(d)

            # enable task
            remote.taskmanager.disable(id)
            # get task
            crond = remote.taskmanager.status(id)

            # response data
            self.write(protocol.success(data=crond))


class Execute(handler.Handler):
    """
        handler for execute a timer task
    """
    @access.exptproc
    @access.needtoken
    def post(self):
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
        if id is None:
            data = {
                'total': len(results),
                'rows': results
            }
        else:
            data = results[0]

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