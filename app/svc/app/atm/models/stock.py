import time

from app.atm import model
from web import sqlhelper


class Stock(model.Model):
    """
        model from stock
    """
    def get(self, **conds):
        """
            get user by username(phone number)
        :param user:
        :return:
        """
        # select query object
        q = sqlhelper \
            .select()\
            .columns('id', 'name', 'jianpin', 'quanpin', 'status', 'limit', 'ctime', 'mtime')\
            .tables('tb_stock')\
            .where(**conds)

        # excute query
        results = self.dbselect(q.sql(), q.args())

        return results

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
        return self.dbinsert(q.sql(), q.args())

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
        return self.dbupdate(sql, args)
