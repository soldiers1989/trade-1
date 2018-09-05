"""
    form data for trade request
"""
from web import form, field
from app.aam import suite


class UserBuy(form.Form):
    user = field.IntegerField()
    stock = field.StringField()
    lever = field.IntegerField()
    coupon = field.IntegerField(null=True)
    ptype = field.EnumField(choices=suite.enum.values(suite.enum.ptype))
    price = field.DecimalField(digits=10, decimals=2)
    count = field.IntegerField()


class UserSell(form.Form):
    user = field.IntegerField()
    trade = field.IntegerField()
    ptype = field.EnumField(choices=suite.enum.values(suite.enum.ptype))
    price = field.DecimalField(digits=10, decimals=2)


class UserCancel(form.Form):
    operator = field.EnumField(choices=suite.enum.values(suite.enum.operator))
    user = field.IntegerField()
    order = field.IntegerField()


class SysClose(form.Form):
    operator = field.EnumField(choices=suite.enum.values(suite.enum.operator))
    user = field.IntegerField()
    trade = field.IntegerField()
    ptype = field.EnumField(choices=suite.enum.values(suite.enum.ptype))
    price = field.DecimalField(digits=10, decimals=2)


class SysBought(form.Form):
    operator = field.EnumField(choices=suite.enum.values(suite.enum.operator))
    user = field.IntegerField()
    trade = field.IntegerField()
    count = field.IntegerField()
    price = field.DecimalField(digits=10, decimals=2)


class Sold(form.Form):
    operator = field.EnumField(choices=suite.enum.values(suite.enum.operator))
    user = field.IntegerField()
    trade = field.IntegerField()
    count = field.IntegerField()
    price = field.DecimalField(digits=10, decimals=2)


class Notify(form.Form):
    operator = field.EnumField(choices=suite.enum.values(suite.enum.operator))
    user = field.IntegerField()
    order = field.IntegerField()
    status = field.EnumField(choices=suite.enum.values(suite.enum.order))
    ocode = field.StringField()
    dcount = field.IntegerField()
    dprice = field.IntegerField()
    ccount = field.IntegerField()
