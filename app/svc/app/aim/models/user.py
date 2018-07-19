"""
    user model
"""
import time
from app.aim import model
from app.util import sqlhelper


class UserModel(model.Model):
    def get(self, **conds):
        """
            get user by username(phone number)
        :param user:
        :return:
        """
        # select query object
        q = sqlhelper.select().columns('id', 'user', 'pwd', 'phone', 'money', 'disable', 'ctime', 'ltime').tables('tb_user').where(**conds)

        # excute query
        results = self.dbselect(q.sql(), q.args())

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
        return self.dbinsert(sql, (phone, pwd, phone, 0.0, False, tm, tm))

    def update(self, id, **cvals):
        """
            update user with @id
        :param id: int, user id
        :param cvals: dict, update column with values
        :return:
        """
        # update query object
        q = sqlhelper.update().table('tb_user').set(**cvals).where(id=id)

        # execute update
        return self.dbupdate(q.sql(), q.args())


    def getbank(self, **conds):
        """
            get user bank
        :param id:
        :return:
        """
        # select query object
        q = sqlhelper.select().columns('id', 'bank', 'name', 'account', 'deleted', 'ctime', 'mtime', 'user_id').tables('tb_user_bank').where(**conds)

        # excute query
        results = self.dbselect(q.sql(), q.args())

        return results
