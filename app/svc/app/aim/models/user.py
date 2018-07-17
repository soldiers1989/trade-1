"""
    user model
"""
import time
from app.aim import model


class UserModel(model.Model):
    id = 'id'

    def get(self, user):
        """
            get user by username(phone number)
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
        results = self.select(sql, (user,))

        return results

    def add(self, phone, pwd):
        """
            add new user
        :param phone:
        :param pwd:
        :return:
        """
        # sql for get user object
        sql = '''
                insert into tb_user
                (`user`, pwd, phone,money,disable,ctime,ltime)
                values
                (%s, %s, %s, %s, %s, %s, %s)
              '''

        # get current time
        tm = int(time.time())

        # insert new records
        return self.insert(sql, (phone, pwd, phone, 0.0, False, tm, tm))
