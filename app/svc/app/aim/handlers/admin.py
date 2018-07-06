"""
    service admin
"""
from app.aim import log, access, handler, error, protocol, session, redis, sms


class EchoHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            echo
        :return:
        """
        self.write(protocol.success(msg='success', data='echo'))


class LogGetHandler(handler.Handler):
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


class RedisGetHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            log
        :return:
        """
        name = self.get_argument('n')

        data = redis.aim.get((name))

        self.write(protocol.success(data=data))


class RedisDelHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            log
        :return:
        """
        name = self.get_argument('n')

        val = redis.aim.delete(name)

        self.write(protocol.success())


class SessionGetHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            log
        :return:
        """
        id = self.get_argument('id')
        data = session.get(id).all()
        self.write(protocol.success(data = data))


class SessionDelHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            log
        :return:
        """
        id = self.get_argument('id')
        session.get(id).clear()
        self.write(protocol.success())


class SessionExtGetHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            log
        :return:
        """
        sid, name = self.get_argument('sid'), self.get_argument('n')
        data = session.get(sid).getext(name)
        self.write(protocol.success(data = data))


class SessionExtDelHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            log
        :return:
        """
        sid, name = self.get_argument('sid'), self.get_argument('n')
        session.get(sid).delext(name)
        self.write(protocol.success())


class SmsGetHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            log
        :return:
        """
        phone, name = self.get_argument('p'), self.get_argument('n')
        data = sms.get(phone, name)
        self.write(protocol.success(data = data))


class SmsDelHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            log
        :return:
        """
        phone, name = self.get_argument('p'), self.get_argument('n')
        sms.delete(phone, name)
        self.write(protocol.success())

