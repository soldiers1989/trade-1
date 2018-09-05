"""
    trade account dao
"""
from web import dao, sqlhelper
from app.aam import models


class AccountDao(dao.Dao):
    def select_one(self):
        """
            get a usable account for trade
        :return:
        """
        # select query
        q = sqlhelper.select().columns(*models.TradeAccount.fields).tables('tb_trade_account').where(disable=False).orderby('lmoney').desc()

        # execute query
        results = self.select(q.sql(), q.args())
        if len(results) > 0:
            return models.TradeAccount(**results[0])

        return None
