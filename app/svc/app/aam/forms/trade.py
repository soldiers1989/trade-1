"""
    form data for trade request
"""
from app.aam import form, enum


class Add(form.Form):
    def __init__(self, request):
        self.user = request.get_argument('user')
        self.stock = request.get_argument('stock')
        self.lever = request.get_argument('lever')
        self.coupon = request.get_argument('coupon', None)
        self.price = request.get_argument('price', None)
        self.count = request.get_argument('count')

        self.ptype = enum.ptype.xj.code if self.price is not None else enum.ptype.sj.code

    def validate(self):
        """
            validate form data, raise an exception for invalid form data
        :return:
        """
        # check user id
        self.number()

        # stock count must be multipe of 100
        if self.count < 100 or self.count % 100 != 0:
            raise form.error('股票数量应为100的整数倍')

        return self
