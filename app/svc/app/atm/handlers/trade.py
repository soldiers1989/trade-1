import json
from .. import handler, access, tasks, protocol, executor


class TakeHandler(handler.Handler):
    """
        take user trades
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
        executor.submit(tasks.trade.take, config=config['config'], callback=config.get('callback'))

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
        executor.submit(tasks.trade.place, config=config['config'], callback=config.get('callback'))

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
        executor.submit(tasks.trade.notify, config=config['config'], callback=config.get('callback'))

        # response success
        self.write(protocol.success())


class ClearHandler(handler.Handler):
    """
        user trade order daily clear
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
        executor.submit(tasks.trade.clear, config=config['config'], callback=config.get('callback'))

        # response success
        self.write(protocol.success())


class ExpireHandler(handler.Handler):
    """
        user trade order daily expire
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
        executor.submit(tasks.trade.expire, config=config['config'], callback=config.get('callback'))

        # response success
        self.write(protocol.success())