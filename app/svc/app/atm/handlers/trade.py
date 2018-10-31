import json
from .. import handler, access, tasks, protocol, error, task


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

        # get config from post json data
        config = json.loads(self.request.body.decode())

        # get callback url
        callback = config.get('callback')

        # manage task
        task.manager.take(tasks.trade.TradeService.__name__, tasks.trade.TradeService(callback=callback, config=config))

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
        task.manager.free(tasks.trade.TradeService.__name__)

        self.write(protocol.success())