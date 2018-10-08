"""
    trade account dao
"""
from tlib.web import dao

from .. import models
from tlib.web import sqlhelper


class AccountDao(dao.Dao):
    """
        account relate dao
    """
    def list(self, **conds):
        """
            get account list by @conds
        :param conds: dict, select conditions
        :return:
            list
        """
        # select query
        q = sqlhelper.select().columns(*models.TradeAccount.fields).table('tb_trade_account').where(**conds)

        # execute query
        results = self.select(q.sql(), q.args())

        return results
