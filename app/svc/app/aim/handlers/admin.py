"""
    service admin
"""
from app.aim import access, handler, protocol, redis, error


class EchoHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            echo
        :return:
        """
        self.write(protocol.success(msg='success', data='echo'))


class RedisGetHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            log
        :return:
        """
        # get arguments
        db, type, name = self.get_argument('db'), self.get_argument('t', None), self.get_argument('n')

        # get redis db
        db = redis.all.get(db)
        if db is None:
            raise error.redis_db_not_exist

        # get data from redis db
        if type == 'h': # hash
            data = db.hgetall(name)
        elif type == 'l': # list
            data = db.lrange(name, 0, -1)
        elif type == 's': # set
            data = db.smembers(name)
            data = list(data)
        elif type == 'z': # sorted set
            data = db.zrange(name, 0, -1)
        else: # string
            data = db.get(name)

        if data is None:
            raise error.redis_key_not_exist

        self.write(protocol.success(data=data))


class RedisDelHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            log
        :return:
        """
        # get arguments
        db, name = self.get_argument('db'), self.get_argument('n')

        # get redis db
        db = redis.all.get(db)
        if db is None:
            raise error.redis_db_not_exist

        # delete data
        db.delete(name)

        self.write(protocol.success())

