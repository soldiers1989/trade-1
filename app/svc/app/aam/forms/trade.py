"""
    form data for trade request
"""
from web import form, field
from app.aam import enum


class Add(form.Form):
    user = field.IntegerField()
    stock = field.StringField()
    lever = field.IntegerField()
    coupon = field.IntegerField(null=True)
    price = field.DecimalField(null=True, digits=10, decimals=2)
    count = field.IntegerField()
    ptype = field.EnumField(choices=enum.values(enum.ptype))
