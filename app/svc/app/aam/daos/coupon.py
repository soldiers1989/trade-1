"""
    coupon dao
"""
from tlib.web import dao

from .. import models
from tlib.web import sqlhelper


class CouponDao(dao.Dao):
    def get(self, **conds):
        """
            get coupon
        :param id:
        :return:
        """
        # select query
        q = sqlhelper.select().columns(*models.UserCoupon.fields).table('tb_user_coupon').where(**conds)


        # execute query
        results = self.select(q.sql(), q.args())
        if len(results) > 0:
            return models.UserCoupon(**results[0])

        return None
