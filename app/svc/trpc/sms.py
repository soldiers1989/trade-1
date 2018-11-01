"""
    remote rpc for send short message
"""
from . import rpc


class SmsRpc(rpc.Rpc):
    def __init__(self, baseurl:str, key:str, safety:bool):
        """
            init rpc
        :param baseurl: str, base url for remote http service
        :param key: str, private key for safety verification or None
        :param safety: bool, enable safety key verification with True
        """
        super().__init__(baseurl, key, safety)

    def send(self, phone, msg):
        """
            send msg to phone
        :param phone:
        :param msg:
        :return:
        """
        pass