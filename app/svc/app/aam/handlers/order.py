"""
    order management
"""
from .. import access, handler, forms, protocol, info, beans, suite


class ListHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get trade records
        :return:
        """
        # get arguments
        form = forms.order.List(**self.arguments)

        # list conditions
        conds = {
            'status__in': form.status.split(','),
            'odate': form.date
        }

        # get trade records
        results = beans.order.get_orders(**conds)

        # success
        self.write(protocol.success(data=results))


class BuyHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            order by
        :return:
        """
        # get arguments
        form = forms.order.Order(otype=suite.enum.otype.buy.code, **self.arguments)

        # get trade records
        order = beans.order.place(form)

        # success
        self.write(protocol.success(data=order))


class SellHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            order sell
        :return:
        """
        # get arguments
        form = forms.order.Order(otype=suite.enum.otype.sell.code, **self.arguments)

        # get trade records
        order = beans.order.place(form)

        # success
        self.write(protocol.success(data=order))


class CancelHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            order cancel
        :return:
        """
        # get arguments
        form = forms.order.Cancel(**self.arguments)

        # get trade records
        order = beans.order.cancel(form)

        # success
        self.write(protocol.success(data=order))


class NotifyHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            order notify
        :return:
        """
        # get arguments
        form = forms.order.Notify(**self.arguments)

        # get trade records
        order = beans.order.notify(form)

        # success
        self.write(protocol.success(data=order))
