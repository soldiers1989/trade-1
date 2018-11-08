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
    oprice = field.DecimalField(digits=10, decimals=2)
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
    user = field.IntegerField()
    trade = field.IntegerField()
    account = field.StringField()


class SysSell(form.Form):
    type = field.EnumField(choices=('sell', 'close'))
    user = field.IntegerField()
    trade = field.IntegerField()


class SysCancel(form.Form):
    user = field.IntegerField()
    trade = field.IntegerField()


class Notify(form.Form):
    tcode = field.StringField()
    dcount = field.IntegerField(null=True)
    dprice = field.DecimalField(null=True, digits=10, decimals=2)
    status = field.EnumField(choices=('pcanceled', 'tcanceled', 'tdeal', 'pdeal'))
