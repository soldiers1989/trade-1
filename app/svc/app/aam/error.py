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
not_trading_time = ProcessError(-1100, '非交易时间段')

server_exception = ProcessError(-1200, '服务器处理异常')
invalid_access = ProcessError(-1201, '未授权的非法访问')

redis_db_not_exist = ProcessError(-1220, '查询DB不存在')
redis_key_not_exist = ProcessError(-1221, '查询健值不存在')

user_not_exist = ProcessError(-1300, '用户不存在')
user_has_disabled = ProcessError(-1300, '用户被禁用')
user_money_not_enough = ProcessError(-1300, '用户余额不足')

lever_not_exist = ProcessError(-1301, '杠杆配置不存在')
lever_has_disabled = ProcessError(-1301, '杠杆配置已禁用')
lever_capital_denied = ProcessError(-1301, '委托金额超出范围')

coupon_not_exist = ProcessError(-1302, '优惠券不存在')
coupon_has_used = ProcessError(-1302, '优惠券已使用')
coupon_has_expired = ProcessError(-1302, '优惠券无效或过期')

stock_not_exist = ProcessError(-1303, '股票不存在')
stock_is_closed = ProcessError(-1303, '股票已停牌')
stock_is_delisted = ProcessError(-1303, '股票已退市')
stock_buy_limited = ProcessError(-1303, '股票已禁买')
stock_delay_limited = ProcessError(-1303, '股票已禁延')

stock_count_error = ProcessError(-1304, '股票数量需为100整数倍')
stock_price_error = ProcessError(-1304, '股票申报价格超出范围')

account_money_not_enough = ProcessError(-1305, '股票交易账户余额不足')
stock_count_not_enough = ProcessError(-1305, '股票可用数量不足')
stock_count_not_match = ProcessError(-1305, '股票持仓和可用数量不一致')

trade_order_cancel_denied = ProcessError(-1306, '当前委托不可撤销')
trade_order_notify_denied = ProcessError(-1306, '当前委托目标状态禁止转换')
trade_operation_denied = ProcessError(-1306, '当前状态不允许该操作')

order_type_not_exists = ProcessError(-1307, '委托类型不存在')

