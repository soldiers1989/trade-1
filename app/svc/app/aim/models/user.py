"""
    user model
"""
from app.aim import model


class UserModel(model.Model):
    def get(self, user):
        """
            get user by username
        :param user:
        :return:
        """
        # sql for get user object
        sql = '''
                select id, `user`, pwd, phone,money,disable,ctime,ltime
                from tb_user
                where `user`=%s
              '''

        # excute query
        results = self._select(sql, (user,))

        return results
