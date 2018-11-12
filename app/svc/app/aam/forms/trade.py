"""
    form data for trade request
"""
from venus.form import form, field


class UserBuy(form.Form):
    user = field.IntegerField()
    stock = field.StringField(max_length=8)
    lever = field.IntegerField()
    coupon = field.IntegerField(null=True)
    optype = field.EnumField(choices=('xj','sj'))
    oprice = field.DecimalField(digits=10, decimals=2, null=True)
    ocount = field.IntegerField()


class UserSell(form.Form):
    type = field.EnumField(choices=('sell', 'close'))
    user = field.IntegerField()
    trade = field.IntegerField()
    optype = field.EnumField(choices=('xj', 'sj'))
    oprice = field.DecimalField(digits=10, decimals=2)
    ocount = field.IntegerField()


class UserCancel(form.Form):
    user = field.IntegerField()
    trade = field.IntegerField()


class SysBuy(form.Form):
    trade = field.IntegerField()


class SysSell(form.Form):
    trade = field.IntegerField()


class SysCancel(form.Form):
    trade = field.IntegerField()


class SysDrop(form.Form):
    trade = field.IntegerField()


class OrderBought(form.Form):
    id = field.IntegerField()
    dcount = field.IntegerField()
    dprice = field.DecimalField(digits=10, decimals=2)


class OrderSold(form.Form):
    id = field.IntegerField()
    dcount = field.IntegerField()
    dprice = field.DecimalField(digits=10, decimals=2)


class OrderCanceled(form.Form):
    id = field.IntegerField()


class OrderExpired(form.Form):
    id = field.IntegerField()
