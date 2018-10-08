"""
    trade account management
"""
from .. import access, handler, forms, protocol, mysql, daos, beans, error


class ListHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def get(self):
        """
            add new trade request
        :return:
        """
        # connect database
        db = mysql.get()

        # init dao object
        dao = daos.account.AccountDao(db)

        # get accounts
        accounts = dao.list(**self.cleaned_arguments)

        # success
        self.write(protocol.success(data=accounts))


class SelectHandler(handler.Handler):
    @access.exptproc
    @access.needtoken
    def post(self):
        """
            add new trade request
        :return:
        """
        # get arguments
        form = forms.account.Select(**self.arguments)

        # select account
        account = beans.account.select(form)
        if account is None:
            raise error.account_not_usable

        # success
        self.write(protocol.success(data=account))
