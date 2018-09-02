"""
    stock dao
"""
from web import dao
from app.aam import models

class StockDao(dao.Dao):
    def get(self, id):
        """
            get stock
        :param user:
        :return:
        """
        # select query
        sql = '''
                select id, name, jianpin, quanpin, status, `limit`, ctime, mtime
                from tb_stock
                where id = %s
            '''

        # execute query
        results = self.select(sql, (id,))
        if len(results) > 0:
            return models.Stock(**results[0])

        return None