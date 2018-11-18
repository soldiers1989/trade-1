"""
    trade account management
"""
from .. import access, handler, protocol, error, models


class ListHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            get account list
        :return:
        """
        with models.db.create() as d:
            # get accounts
            accounts = models.TradeAccount.filter(d, **self.cleaned_arguments).all()

            # success
            self.write(protocol.success(data=accounts))


class SelectHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            add new trade request
        :return:
        """
        with models.db.create() as d:
            # select account
            account = models.TradeAccount.filter(d, disable=False).orderby('money').desc().one()
            if account is None:
                raise error.account_not_usable

            # success
            self.write(protocol.success(data=account))
