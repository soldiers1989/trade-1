"""
    error definition
"""
from app.aim import protocol


class _Error:
    def __init__(self, status, msg):
        self._status = status
        self._msg = msg

    @property
    def data(self):
        return protocol.failed(status=self._status, msg=self._msg)


user_not_login = _Error(-1000, '用户未登录')
user_or_pwd_invalid = _Error(-1001, '用户名或密码错误')
user_disabled = _Error(-1002, '用户被禁止，请与平台联系')
user_exists = _Error(-1003, '手机号已注册')
user_register = _Error(-1004, '用户注册失败')

missing_parameters = _Error(-1100, '缺少必要的访问参数')
invalid_parameters = _Error(-1100, '非法的访问参数')
invalid_phone = _Error(-1100, '错误的手机号')

server_exception = _Error(-1200, '服务器处理异常')
invalid_access = _Error(-1201, '未授权的非法访问')

wrong_image_verify_code = _Error(-1210, '图片验验码错误')
wrong_sms_verify_code = _Error(-1211, '短信验验码错误')
wrong_usage_verify_code = _Error(-1212, '验证码类型错误')
