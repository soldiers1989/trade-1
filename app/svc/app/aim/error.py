"""
    error definition
"""
SERVER_EXCEPTION = {
    'status': -1,
    'msg': '服务器处理异常'
}

MISSING_PARAMETERS = {
    'status': -1,
    'msg': '缺少必须要的访问参数'
}

USER_OR_PASSWORD_INVALID = {
    'status': -1,
    'msg': '用户名或密码错误'
}

USER_DISABLED = {
    'status': -1,
    'msg': '用户被禁用，请与平台联系'
}
