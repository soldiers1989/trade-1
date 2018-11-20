import json
from .. import handler, access, tasks, protocol, executor


class CheckHandler(handler.Handler):
    """
        check user hold trade list's rick
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
                        "mds": {
                            "baseurl": "http://localhost:10007",
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
        executor.submit(tasks.risker.check, config=config['config'], callback=config.get('callback'))

        # response success
        self.write(protocol.success())
