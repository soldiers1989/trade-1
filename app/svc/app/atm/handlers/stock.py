import json
from .. import handler, access, tasks, protocol, forms, task, error


class SyncAllHandler(handler.Handler):
    """
        sync stocks from source
    """
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            process sync all stock task
        :param args:
        :param kwargs:
        :return:
        """
        if self.request.body is None:
            raise error.missing_parameters


        # get callback url
        form = forms.task.Task(**self.arguments)

        # get config from post json data
        config = json.loads(self.request.body.decode())

        # start a new sync task
        task.manager.take(tasks.stock.SyncAllService.cname(), tasks.stock.SyncAllService(callback=form.callback, config=config))

        self.write(protocol.success())
