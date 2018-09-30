import json
from .. import handler, access, tasks, protocol, forms, error, task


class StartHandler(handler.Handler):
    """
        start robot trade service handler
    """
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            process start robot trade service task
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

        # manage task
        task.manager.take(tasks.trade.TradeService.cname(), tasks.trade.TradeService(callback=form.callback, config=config))

        self.write(protocol.success())


class StopHandler(handler.Handler):
    """
        stop robot trade service handler
    """
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            process start robot trade service task
        :param args:
        :param kwargs:
        :return:
        """
        # manage task
        task.manager.free(tasks.trade.TradeService.cname())

        self.write(protocol.success())