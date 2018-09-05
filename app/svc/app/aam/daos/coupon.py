"""
    coupon dao
"""
from web import dao, sqlhelper
from app.aam import models


class CouponDao(dao.Dao):
    def get(self, **conds):
        """
            get coupon
        :param id:
        :return:
        """
        # select query
        q = sqlhelper.select().columns(*models.UserCoupon.fields).tables('tb_user_coupon').where(**conds)


        # execute query
        results = self.select(q.sql(), q.args())
        if len(results) > 0:
            return models.UserCoupon(**results[0])

        return None
