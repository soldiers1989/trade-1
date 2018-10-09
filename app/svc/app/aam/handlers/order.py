"""
    order management
"""
from .. import access, handler, forms, protocol, beans, suite, mysql


class ListHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get trade records
        :return:
        """
        # list conditions
        conds = self.cleaned_arguments

        # get trade records
        results = beans.order.list(**conds)

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


class UpdateHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            order notify
        :return:
        """
        # get arguments
        form = forms.order.Update(**self.arguments)

        # get trade records
        order = beans.order.update(form)

        # success
        self.write(protocol.success(data=order))

