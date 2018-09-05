"""
    user dao
"""
from web import dao, sqlhelper
from app.aam import models


class UserDao(dao.Dao):
    def get(self, **conds):
        """
            get stock
        :param user:
        :return:
        """
        # select query
        q = sqlhelper.select().columns(*models.User.fields).tables('tb_user').where(**conds)

        # execute query
        results = self.select(q.sql(), q.args())
        if len(results) > 0:
            return models.User(**results[0])

        return None
