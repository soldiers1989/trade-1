"""
    lever dao
"""
from web import dao, sqlhelper
from app.aam import models


class LeverDao(dao.Dao):
    def get(self, **conds):
        """
            get lever
        :param leverid:
        :return:
        """
        # select query
        q = sqlhelper.select().columns(*models.Lever.fields).tables('tb_lever').where(**conds)


        # execute query
        results = self.select(q.sql(), q.args())
        if len(results) > 0:
            return models.Lever(**results[0])

        return None