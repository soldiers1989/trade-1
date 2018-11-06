"""
    lever dao
"""
from venus import dao

from .. import models
from venus import sqlhelper


class LeverDao(dao.Dao):
    def get(self, **conds):
        """
            get lever
        :param leverid:
        :return:
        """
        # select query
        q = sqlhelper.select().columns(*models.Lever.fields).table('tb_lever').where(**conds)


        # execute query
        results = self.select(q.sql(), q.args())
        if len(results) > 0:
            return models.Lever(**results[0])

        return None