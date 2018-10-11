"""
    form data for trade request
"""
from tlib.web import form, field


class Place(form.Form):
    zqdm = field.StringField()
    ptype = field.EnumField(choices=['xj','sj'])
    price = field.DecimalField(digits=10, decimals=2)
    count = field.IntegerField()

