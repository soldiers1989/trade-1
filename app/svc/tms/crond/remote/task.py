"""
    remote task
"""
import requests
from .. import timer, config


class RemoteTask(timer.Runnable):
    def __init__(self, id, name, url):
        """
            create a remote task with remote url and crond string
        :param url:
        :param crondstr:
        """
        self._id = id
        self._name = name
        self._url = url

    def execute(self, seq):
        try:
            callback = config.CALLBACK_URL % (str(id), str(seq))
            resp = requests.get(self._url, params={'callback': callback}).json()
            return resp.get('status'), resp.get('msg')
        except Exception as e:
            return False, str(e)
