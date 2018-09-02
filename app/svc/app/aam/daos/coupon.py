"""
    coupon dao
"""
import time
from web import dao
from app.aam import models


class CouponDao(dao.Dao):
    def get(self, id):
        """
            get coupon
        :param id:
        :return:
        """
        # select query
        sql = '''
                select id, user_id, name, money, status, sdate, edate, ctime, utime
                from tb_user_coupon
                where id = %s
            '''

        # execute query
        results = self.select(sql, (id,))
        if len(results) > 0:
            return models.UserCoupon(results[0])

        return None

    def use(self, id):
        """
            use coupon
        :param couponid:
        :return:
        """
        # update query
        sql = '''
                update tb_coupon
                set status=%s, utime=%s
                where id=%s
            '''

        # execute update
        self.execute(sql, ('used', int(time.time()), id))
