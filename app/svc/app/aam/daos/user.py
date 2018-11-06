"""
    user dao
"""
from venus import dao

from .. import models
from venus import sqlhelper


class UserDao(dao.Dao):
    def get(self, **conds):
        """
            get stock
        :param user:
        :return:
        """
        # select query
        q = sqlhelper.select().columns(*models.User.fields).table('tb_user').where(**conds)

        # execute query
        results = self.select(q.sql(), q.args())
        if len(results) > 0:
            return models.User(**results[0])

        return None
