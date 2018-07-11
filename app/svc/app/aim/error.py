"""
    error definition
"""
from app.aim import protocol


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


user_not_login = ProcessError(-1000, '用户未登录')
user_or_pwd_invalid = ProcessError(-1001, '用户名或密码错误')
user_disabled = ProcessError(-1002, '用户被禁止，请与平台联系')
user_exists = ProcessError(-1003, '手机号已注册')
user_register = ProcessError(-1004, '用户注册失败')

missing_parameters = ProcessError(-1100, '缺少必要的访问参数')
invalid_parameters = ProcessError(-1100, '非法的访问参数')
invalid_phone = ProcessError(-1100, '错误的手机号')

server_exception = ProcessError(-1200, '服务器处理异常')
invalid_access = ProcessError(-1201, '未授权的非法访问')

wrong_image_verify_code = ProcessError(-1210, '图片验验码错误')
wrong_sms_verify_code = ProcessError(-1211, '短信验验码错误')
wrong_usage_verify_code = ProcessError(-1212, '验证码类型错误')

