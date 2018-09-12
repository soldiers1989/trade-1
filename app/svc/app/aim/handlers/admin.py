"""
    service admin
"""
from .. import access, handler, protocol, redis, error


class EchoHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            echo
        :return:
        """
        self.write(protocol.success(msg='success', data='echo'))
