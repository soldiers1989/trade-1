"""
    error definition
"""
from app.aam import protocol


class ProcessError(Exception):
    def __init__(self, status, msg):
        self._status = status
        self._msg = msg

    @property
    def status(self):
        return self._status

    @property
    def msg(self):
        return self._msg

    @property
    def data(self):
        return protocol.failed(self._status, self._msg)

    def __str__(self):
        return 'status: '+str(self._status)+', msg: '+self._msg


missing_parameters = ProcessError(-1100, '缺少必要的访问参数')
invalid_parameters = ProcessError(-1100, '非法的访问参数')

server_exception = ProcessError(-1200, '服务器处理异常')
invalid_access = ProcessError(-1201, '未授权的非法访问')

redis_db_not_exist = ProcessError(-1220, '查询DB不存在')
redis_key_not_exist = ProcessError(-1221, '查询健值不存在')
