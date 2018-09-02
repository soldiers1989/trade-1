"""
    lever dao
"""
from web import dao
from app.aam import models

class LeverDao(dao.Dao):
    def get(self, id):
        """
            get lever
        :param leverid:
        :return:
        """
        # select query
        sql = '''
                select id, lever, wline, sline, ofmin, ofrate, dfrate, psrate, mmin, mmax, `order`, disable, ctime, mtime
                from tb_lever
                where id = %s
            '''

        # execute query
        results = self.select(sql, (id,))
        if len(results) > 0:
            return models.Lever(results[0])

        return None