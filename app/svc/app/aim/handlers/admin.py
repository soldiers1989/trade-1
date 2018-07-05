"""
    service admin
"""
from app.aim import log, access, handler, error, protocol, session


class EchoHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            echo
        :return:
        """
        self.write(protocol.success(msg='success', data='echo'))


class GetLogHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            log
        :return:
        """
        type = self.get_argument('type')
        if type == 'info':
            self.write(protocol.success(msg='success', data=log.getinfo()))
        elif type == 'error':
            self.write(protocol.success(msg='success', data=log.geterror()))
        else:
            self.write(error.invalid_parameters.data)


class DeleteSessionHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            log
        :return:
        """
        sid = self.get_argument('sid')
        session.get(sid).clear()
        self.write(protocol.success())
