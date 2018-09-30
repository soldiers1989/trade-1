"""
    remote task
"""
import requests, logging
from .. import timer, config, error


class RemoteTask(timer.Runnable):
    def __init__(self, id, name, url, method, data, json):
        """
            create a remote task with remote url and crond string
        :param url:
        :param crondstr:
        """
        # check parameters
        if method not in ['get', 'post']:
            raise error.method_not_support

        if data is not None and json is not None:
            raise error.post_data_duplicate

        self._id = id
        self._name = name
        self._url = url
        self._method = method
        self._data = data
        self._json = json

    def execute(self, seq):
        try:
            # prepare local callback url form remote web task
            callback = config.CALLBACK_URL % (str(self._id), str(seq))

            if self._method == 'get':
                requests.get(self._url, params={'callback': callback})
            elif self._method == 'post':
                requests.post(self._url, params={'callback': callback}, data=self._data, json=self._json)
            else:
                raise error.method_not_support
            logging.info('execute: %s %s, callback: %s' % (self._method, self._url, callback))

            return True, 'executed'
        except Exception as e:
            logging.error(str(e))
            return False, str(e)
