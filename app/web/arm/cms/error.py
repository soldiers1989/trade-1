from . import resp


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
        return resp.failed(self._status, self._msg)

    def __str__(self):
        return 'status: '+str(self._status)+', msg: '+self._msg


missing_parameters = ProcessError(-1100, '缺少必要的访问参数')
invalid_parameters = ProcessError(-1100, '非法的访问参数')
not_trading_time = ProcessError(-1100, '非交易时间段')

server_exception = ProcessError(-1200, '服务器处理异常')
invalid_access = ProcessError(-1201, '未授权的非法访问')

trade_not_exist = ProcessError(-1210, '用户交易订单不存在')
trade_operation_denied = ProcessError(-1210, '禁止当前交易操作')
trade_no_free_position = ProcessError(-1210, '用户交易无可用持仓')
trade_position_confused = ProcessError(-1210, '用户交易持仓和可用不一致')
