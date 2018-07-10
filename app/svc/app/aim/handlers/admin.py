"""
    service admin
"""
from app.aim import log, access, handler, error, protocol, session, redis, cache


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
        type, name = self.get_argument('t', None), self.get_argument('n')

        if type == 'h': # hash
            data = redis.aim.hgetall(name)
        elif type == 'l': # list
            data = redis.aim.lrange(name, 0, -1)
        elif type == 's': # set
            data = redis.aim.smembers(name)
            data = list(data)
        elif type == 'z': # sorted set
            data = redis.aim.zrange(name, 0, -1)
        else: # string
            data = redis.aim.get(name)

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


class VerifyImgGetHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            log
        :return:
        """
        sid, name = self.get_argument('sid'), self.get_argument('n')
        data = cache.img.get(sid, name)
        self.write(protocol.success(data = data))


class VerifyImgDelHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            log
        :return:
        """
        sid, name = self.get_argument('sid'), self.get_argument('n')
        cache.img.delete(sid, name)
        self.write(protocol.success())


class VerifySmsGetHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            log
        :return:
        """
        phone, name = self.get_argument('p'), self.get_argument('n')
        data = cache.sms.get(phone, name)
        self.write(protocol.success(data = data))


class VerifySmsDelHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            log
        :return:
        """
        phone, name = self.get_argument('p'), self.get_argument('n')
        cache.sms.delete(phone, name)
        self.write(protocol.success())

