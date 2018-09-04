"""
    trade account dao
"""
from web import dao
from app.aam import models


class AccountDao(dao.Dao):
    def get(self):
        """
            get a usable account for trade
        :return:
        """
        # select query
        sql = '''
                select id, account, name, lmoney, cfmin, cfrate, tfrate, disable, ctime, mtime
                from tb_trade_account
                where disable=%s
                order by lmoney desc
            '''

        # execute query
        results = self.select(sql, (False,))
        if len(results) > 0:
            return models.TradeAccount(**results[0])

        return None
