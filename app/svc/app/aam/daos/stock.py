"""
    stock dao
"""
import time
from .. import models
from venus import dao, sqlhelper


class StockDao(dao.Dao):
    def list(self, **conds):
        """
            get stock list
        :return:
        """
        # select query
        q = sqlhelper.select().columns(*models.Stock.fields).table('tb_stock').where(**conds)

        # execute query
        results = self.select(q.sql(), q.args())

        # stock list
        return results

    def get(self, **conds):
        """
            get stock
        :param user:
        :return:
        """
        # select query
        q = sqlhelper.select().columns(*models.Stock.fields).table('tb_stock').where(**conds)

        # execute query
        results = self.select(q.sql(), q.args())
        if len(results) > 0:
            return models.Stock(**results[0])

        return None

    def add(self, id, name, jianpin, quanpin, status, limit):
        """
            add new user
        :param phone:
        :param pwd:
        :return:
        """
        # get current time
        tm = int(time.time())

        # insert query object
        q = sqlhelper \
            .insert()\
            .columns('id', 'name', 'jianpin', 'quanpin', 'status', 'limit', 'ctime', 'mtime')\
            .table('tb_stock')\
            .values(id, name, jianpin, quanpin, status, limit, tm, tm)

        # insert new records
        return self.insert(q.sql(), q.args())

    def update(self, ids, **cvals):
        """
            update user with @id
        :param id: int, user id
        :param cvals: dict, update column with values
        :return:
        """
        # update query object
        q = sqlhelper.update().table('tb_stock').set(**cvals)

        # create sql
        sql = q.sql() + ' where id in (' + sqlhelper.util.repeat('%s', len(ids), ',') + ')'

        # args
        args = []
        args.extend(q.args())
        args.extend(ids)

        # execute update
        return self.update(sql, args)