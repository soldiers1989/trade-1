"""
    stock dao
"""
from tlib.web import dao

from .. import models
from tlib.web import sqlhelper


class StockDao(dao.Dao):
    def get(self, **conds):
        """
            get stock
        :param user:
        :return:
        """
        # select query
        q = sqlhelper.select().columns(*models.Stock.fields).tables('tb_stock').where(**conds)

        # execute query
        results = self.select(q.sql(), q.args())
        if len(results) > 0:
            return models.Stock(**results[0])

        return None