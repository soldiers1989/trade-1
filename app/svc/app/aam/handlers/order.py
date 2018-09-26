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
        form = forms.order.ListForm(**self.arguments)

        # list conditions
        conds = {
            'status__in': form.status.split(',')
        }

        # get trade records
        results = beans.order.get_orders(**conds)

        # success
        self.write(protocol.success(data=results))