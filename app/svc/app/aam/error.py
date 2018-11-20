"""
    error definition
"""
from . import protocol


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


missing_parameters = ProcessError(-1100, '访问参数缺失')
invalid_parameters = ProcessError(-1100, '访问参数非法')
not_trading_time = ProcessError(-1100, '非交易时间段')

server_exception = ProcessError(-1200, '服务器处理异常')
invalid_access = ProcessError(-1201, '访问未授权')

redis_db_not_exist = ProcessError(-1220, '查询DB不存在')
redis_key_not_exist = ProcessError(-1221, '查询健值不存在')

user_not_exist = ProcessError(-1300, '用户不存在')
user_has_disabled = ProcessError(-1300, '用户被禁用')
user_money_not_enough = ProcessError(-1300, '用户余额不足')

lever_not_exist = ProcessError(-1301, '杠杆配置不存在')
lever_has_disabled = ProcessError(-1301, '杠杆配置已禁用')
lever_capital_denied = ProcessError(-1301, '委托金额超出范围')

coupon_not_exist = ProcessError(-1302, '优惠券不存在')

stock_not_exist = ProcessError(-1303, '股票不存在')
stock_is_closed = ProcessError(-1303, '股票已停牌')
stock_is_delisted = ProcessError(-1303, '股票已退市')
stock_buy_limited = ProcessError(-1303, '股票已禁买')
stock_delay_limited = ProcessError(-1303, '股票已禁延')

stock_count_error = ProcessError(-1303, '股票数量需为100整数倍')
stock_price_error = ProcessError(-1303, '股票申报价格超出范围')
stock_count_not_enough = ProcessError(-1303, '股票可用数量不足')
stock_count_not_match = ProcessError(-1303, '股票持仓和可用数量不一致')

account_not_usable = ProcessError(-1304, '无可用股票账户')
account_money_not_enough = ProcessError(-1304, '股票交易账户余额不足')

order_not_exist = ProcessError(-1305, '委托记录不存在')
order_operation_denied = ProcessError(-1305, '委托操作禁止')
order_notify_data_invalid = ProcessError(-1305, '委托回报数据无效')

trade_not_exist = ProcessError(-1306, '交易不存在')
trade_operation_denied = ProcessError(-1306, '交易操作禁止')
trade_lever_not_exist = ProcessError(-1306, '交易杠杆记录不存在')
trade_margin_not_exist = ProcessError(-1306, '交易保证金记录不存在')
trade_user_not_exist = ProcessError(-1306, '交易用户记录不存在')

trade_count_not_match = ProcessError(-1308, '卖出成交数量和委托数量不一致')

