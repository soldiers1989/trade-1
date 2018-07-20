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
        # sql for add user object
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
        q = sqlhelper.select().columns('id', 'name', 'idc', 'bank', 'account', 'deleted', 'ctime', 'mtime', 'user_id').tables('tb_user_bank').where(**conds)

        # excute query
        results = self.dbselect(q.sql(), q.args())

        return results

    def addbank(self, user, name, idc, bank, account):
        """
            add bank
        :param cvals:
        :return:
        """
        # sql for add user object
        sql = '''
                insert into tb_user_bank
                (`name`, `idc`, `bank`, `account`, `deleted`, `ctime`, `mtime`, `user_id`)
                values
                (%s, %s, %s, %s, %s, %s, %s, %s)
              '''

        # get current time
        tm = int(time.time())

        # insert new records
        return self.dbinsert(sql, (name, idc, bank, account, False, tm, tm, user))

    def delbank(self, user, id):
        """
            delete user bank
        :param user:
        :param id:
        :return:
        """
        # update query object
        q = sqlhelper.update().table('tb_user_bank').set(deleted=True).where(id=id, user_id=user)

        # execute update
        return self.dbupdate(q.sql(), q.args())

    def getcoupon(self, user):
        """
            get user coupon
        :param user:
        :return:
        """
        # select query
        sql = '''
                select id, name, money, status, ctime, etime, utime, user_id
                from tb_user_coupon
                where user_id=%s and status=%s and ctime<=%s and etime>=%s
            '''

        # get current time
        tm = int(time.time())

        # execute query
        results = self.dbselect(sql, (user, 'unused', tm, tm))

        return results

    def usecoupon(self, user, id):
        """
            delete user bank
        :param user:
        :param id:
        :return:
        """
        # update query object
        q = sqlhelper.update().table('tb_user_coupon').set(status='used').where(id=id, user_id=user)

        # execute update
        return self.dbupdate(q.sql(), q.args())

    def getbill(self, user):
        """
            get user bills
        :param user:
        :return:
        """
        # select query
        sql = '''
                select id, code, item, detail, bmoney, lmoney, ctime, user_id
                from tb_user_bill
                where user_id=%s
                order by ctime desc
            '''

        # execute query
        results = self.dbselect(sql, (user,))

        return results

    def getcharge(self, user):
        """
            get user charges
        :param user:
        :return:
        """
        # select query
        sql = '''
                select id, code, money, status, ctime, user_id
                from tb_user_charge
                where user_id=%s
                order by ctime desc
            '''

        # execute query
        results = self.dbselect(sql, (user,))

        return results

    def getdraw(self, user):
        """
            get user draw
        :param user:
        :return:
        """
        # select query
        sql = '''
                select id, code, money, `name`, idc, bank, account, status, ctime, user_id
                from tb_user_draw
                where user_id=%s
                order by ctime desc
            '''

        # execute query
        results = self.dbselect(sql, (user,))

        return results

    def getstock(self, user):
        """
            get user draw
        :param user:
        :return:
        """
        # select query
        sql = '''
                select a.id as id, b.id as code, b.name as name, a.ctime as ctime, a.user_id as user
                from tb_user_stock a, tb_stock b
                where a.user_id=%s and a.stock_id = b.id
                order by a.ctime desc
            '''

        # execute query
        results = self.dbselect(sql, (user,))

        return results
