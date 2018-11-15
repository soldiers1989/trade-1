import json
from .. import handler, access, tasks, protocol, executor


class TakeHandler(handler.Handler):
    """
        take account orders wait to send
    """
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            post json data format:
            {
                "config":{
                    "rpc": {
                        "aam": {
                            "baseurl": "http://localhost:9001",
                            "key": "abc",
                            "safety": false
                        }
                    }
                },
                "callback": "callback url to notify sync result, could be None"
            }
        :return:
        """
        # get config from post json data
        config = json.loads(self.request.body.decode())

        # submit task
        executor.submit(tasks.order.take, config=config['config'], callback=config.get('callback'))

        # response success
        self.write(protocol.success())


class PlaceHandler(handler.Handler):
    """
        place user trade orders
    """
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            post json data format:
            {
                "config":{
                    "rpc": {
                        "aam": {
                            "baseurl": "http://localhost:9001",
                            "key": "abc",
                            "safety": false
                        },
                        "trade": {
                            "baseurl": "http://localhost:10003",
                            "key": "abc",
                            "safety": false
                        }
                    }
                },
                "callback": "callback url to notify sync result, could be None"
            }
        :return:
        """
        # get config from post json data
        config = json.loads(self.request.body.decode())

        # submit task
        executor.submit(tasks.order.place, config=config['config'], callback=config.get('callback'))

        # response success
        self.write(protocol.success())


class NotifyHandler(handler.Handler):
    """
        notify trade order results
    """
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            post json data format:
            {
                "config":{
                    "rpc": {
                        "aam": {
                            "baseurl": "http://localhost:9001",
                            "key": "abc",
                            "safety": false
                        },
                        "trade": {
                            "baseurl": "http://localhost:10003",
                            "key": "abc",
                            "safety": false
                        }
                    }
                },
                "callback": "callback url to notify sync result, could be None"
            }
        :return:
        """
        # get config from post json data
        config = json.loads(self.request.body.decode())

        # submit task
        executor.submit(tasks.order.notify, config=config['config'], callback=config.get('callback'))

        # response success
        self.write(protocol.success())
