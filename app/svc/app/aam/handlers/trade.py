"""
    trade management
"""
from .. import access, handler, forms, protocol, info, beans


class UserBuyHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            add new trade request
        :return:
        """
        # get arguments
        form = forms.trade.UserBuy(**self.arguments)

        # process user buy
        trade = beans.trade.user_buy(form)

        # success
        self.write(protocol.success(msg=info.msg_user_buy_success, data=trade))


class UserSellHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get arguments
        form = forms.trade.UserSell(**self.arguments)

        # process
        trade = beans.trade.user_sell(form)

        # success
        self.write(protocol.success(msg=info.msg_user_sell_success, data=trade))


class UserCloseHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get arguments
        form = forms.trade.UserClose(**self.arguments)

        # process
        trade = beans.trade.user_close(form)

        # success
        self.write(protocol.success(msg=info.msg_user_close_success, data=trade))


class UserCancelHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get arguments
        form = forms.trade.UserCancel(**self.arguments)

        # process
        trade = beans.trade.user_cancel(form)

        # success
        self.write(protocol.success(msg=info.msg_user_cancel_success, data=trade))


class SysBuyHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get arguments
        form = forms.trade.SysBuy(**self.arguments)

        # process
        trade = beans.trade.sys_buy(form)

        # success
        self.write(protocol.success(msg=info.msg_sys_buy_success, data=trade))


class SysSellHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get arguments
        form = forms.trade.SysSell(**self.arguments)

        # process
        trade = beans.trade.sys_sell(form)

        # success
        self.write(protocol.success(msg=info.msg_sys_sell_success, data=trade))


class SysCloseHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get arguments
        form = forms.trade.SysClose(**self.arguments)

        # process
        trade = beans.trade.sys_close(form)

        # success
        self.write(protocol.success(msg=info.msg_sys_close_success, data=trade))


class SysCancelHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get arguments
        form = forms.trade.UserCancel(**self.arguments)

        #process
        trade = beans.trade.sys_cancel(form)

        # success
        self.write(protocol.success(msg=info.msg_sys_cancel_success, data=trade))


class SysBoughtHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get arguments
        form = forms.trade.SysBought(**self.arguments)

        # process
        trade = beans.trade.sys_bought(form)

        # success
        self.write(protocol.success(msg=info.msg_sys_bought_success, data=trade))


class SysSoldHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get arguments
        form = forms.trade.SysSold(**self.arguments)

        # process
        trade = beans.trade.sys_sold(form)

        # success
        self.write(protocol.success(msg=info.msg_sys_sold_success, data=trade))


class SysClosedHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get arguments
        form = forms.trade.SysClosed(**self.arguments)

        # process
        trade = beans.trade.sys_closed(form)

        # success
        self.write(protocol.success(msg=info.msg_sys_closed_success, data=trade))


class SysCanceledHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get arguments
        form = forms.trade.SysCanceled(**self.arguments)

        # process
        trade = beans.trade.sys_canceled(form)

        # success
        self.write(protocol.success(msg=info.msg_sys_canceled_success, data=trade))


class SysDroppedHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get arguments
        form = forms.trade.SysDropped(**self.arguments)

        # process
        trade = beans.trade.sys_dropped(form)

        # success
        self.write(protocol.success(msg=info.msg_sys_dropped_success, data=trade))


class SysExpiredHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get arguments
        form = forms.trade.SysCanceled(**self.arguments)

        # process
        trade = beans.trade.sys_canceled(form, True)

        # success
        self.write(protocol.success(msg=info.msg_sys_expired_success, data=trade))


class TradeNotifyHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        # get arguments
        form = forms.trade.TradeNotify(**self.arguments)

        # process
        trade = beans.trade.trade_notify(form)

        # success
        self.write(protocol.success(msg=info.msg_trade_notify_success, data=trade))
