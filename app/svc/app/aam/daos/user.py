"""
    user dao
"""
from web import dao
from app.aam import models


class UserDao(dao.Dao):
    def get(self, id):
        """
            get stock
        :param user:
        :return:
        """
        # select query
        sql = '''
                select id, user, pwd, phone, money, disable, ctime, ltime
                from tb_user
                where id = %s
            '''

        # execute query
        results = self.select(sql, (id,))
        if len(results) > 0:
            return models.User(**results[0])

        return None
