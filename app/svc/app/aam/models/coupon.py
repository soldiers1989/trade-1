"""
    coupon model
"""
from app.aam import model


class Coupon(model.Model):
    def __init__(self, **items):
        """
            init coupon
        :param items:
        """
        pass

    @property
    def id(self, id =None):
        self._id = id
        return self._id