"""
    remote task
"""
import requests, logging
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
            callback = config.CALLBACK_URL % (str(self._id), str(seq))
            requests.get(self._url, params={'callback': callback})
            logging.info('execute: %s, callback: %s' % (self._url, callback))
            return True, 'executed'
        except Exception as e:
            logging.error(str(e))
            return False, str(e)
