"""
    form data for trade request
"""
from web import form, field
from app.aam import suite


class Buy(form.Form):
    operator = field.EnumField(choices=suite.enum.values(suite.enum.operator))
    user = field.IntegerField()
    stock = field.StringField()
    lever = field.IntegerField()
    coupon = field.IntegerField(null=True)
    price = field.DecimalField(null=True, digits=10, decimals=2)
    count = field.IntegerField()
    ptype = field.EnumField(null=True, choices=suite.enum.values(suite.enum.ptype))


class Sell(form.Form):
    operator = field.EnumField(choices=suite.enum.values(suite.enum.operator))
    trade = field.IntegerField()
    ptype = field.EnumField(enum=True, choices=suite.enum.values(suite.enum.ptype))
    price = field.DecimalField(enum=True, digits=10, decimals=2)
    count = field.IntegerField()


class Close(form.Form):
    operator = field.EnumField(choices=suite.enum.values(suite.enum.operator))
    trade = field.IntegerField()
    ptype = field.EnumField(enum=True, choices=suite.enum.values(suite.enum.ptype))
    price = field.DecimalField(enum=True, digits=10, decimals=2)


class Cancel(form.Form):
    operator = field.EnumField(choices=suite.enum.values(suite.enum.operator))
    order = field.IntegerField()

