"""
    form data for trade request
"""
from tlib.web import form, field
from .. import suite


class ListForm(form.Form):
    status = field.StringField(null=True)
    stime = field.DateTimeField(null=True)
    etime = field.DateTimeField(null=True)


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


class UserClose(form.Form):
    user = field.IntegerField()
    trade = field.IntegerField()
    ptype = field.EnumField(choices=suite.enum.values(suite.enum.ptype))
    price = field.DecimalField(digits=10, decimals=2)


class UserCancel(form.Form):
    user = field.IntegerField()
    trade = field.IntegerField()


class SysBuy(form.Form):
    user = field.IntegerField()
    trade = field.IntegerField()


class SysSell(form.Form):
    user = field.IntegerField()
    trade = field.IntegerField()


class SysClose(form.Form):
    user = field.IntegerField()
    trade = field.IntegerField()


class SysCancel(form.Form):
    user = field.IntegerField()
    trade = field.IntegerField()


class SysBought(form.Form):
    user = field.IntegerField()
    trade = field.IntegerField()
    count = field.IntegerField()
    price = field.DecimalField(digits=10, decimals=2)


class SysSold(form.Form):
    user = field.IntegerField()
    trade = field.IntegerField()
    count = field.IntegerField()
    price = field.DecimalField(digits=10, decimals=2)


class SysClosed(form.Form):
    user = field.IntegerField()
    trade = field.IntegerField()
    count = field.IntegerField()
    price = field.DecimalField(digits=10, decimals=2)


class SysCanceled(form.Form):
    user = field.IntegerField()
    trade = field.IntegerField()


class SysDropped(form.Form):
    user = field.IntegerField()
    trade = field.IntegerField()


class TradeNotify(form.Form):
    tcode = field.StringField()
    scode = field.StringField()
    otype = field.EnumField(choices=suite.enum.values(suite.enum.otype))
    optype = field.EnumField(choices=suite.enum.values(suite.enum.ptype))
    ocount = field.IntegerField()
    oprice = field.DecimalField(digits=10, decimals=2, null=True)
    ocode = field.StringField(null=True)
    otime = field.IntegerField(null=True)
    dcount = field.IntegerField(null=True)
    dprice = field.DecimalField(null=True, digits=10, decimals=2)
    dcode = field.StringField(null=True)
    dtime = field.IntegerField(null=True)
    status = field.EnumField(choices=suite.enum.values(suite.enum.order))
