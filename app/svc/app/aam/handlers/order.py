"""
    order management
"""
from .. import access, handler, forms, protocol, info, beans


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
            get trade records
        :return:
        """
        # get arguments
        form = forms.order.Buy(**self.arguments)

        # get trade records
        order = beans.order.buy(form)

        # success
        self.write(protocol.success(data=order))


class SellHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            get trade records
        :return:
        """
        # get arguments
        form = forms.order.Sell(**self.arguments)

        # get trade records
        order = beans.order.sell(form)

        # success
        self.write(protocol.success(data=order))


class CancelHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            get trade records
        :return:
        """
        # get arguments
        form = forms.order.Cancel(**self.arguments)

        # get trade records
        order = beans.order.cancel(form)

        # success
        self.write(protocol.success(data=order))
