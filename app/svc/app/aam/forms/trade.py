"""
    form data for trade request
"""
from web import form, field
from app.aam import enum


class Buy(form.Form):
    user = field.IntegerField()
    stock = field.StringField()
    lever = field.IntegerField()
    coupon = field.IntegerField(null=True)
    price = field.DecimalField(null=True, digits=10, decimals=2)
    count = field.IntegerField()
    ptype = field.EnumField(null=True, choices=enum.values(enum.ptype))


class Sell(form.Form):
    trade = field.IntegerField()
    ptype = field.EnumField(enum=True, choices=enum.values(enum.ptype))
    price = field.DecimalField(enum=True, digits=10, decimals=2)
    count = field.IntegerField()


class Cancel(form.Form):
    trade = field.IntegerField()

