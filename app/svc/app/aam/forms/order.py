"""
    form data for order request
"""
from tlib.web import form, field
from .. import suite


class List(form.Form):
    status = field.StringField()
    date = field.DateField()


class Order(form.Form):
    account = field.StringField()
    tcode = field.StringField()
    scode = field.StringField()
    sname = field.StringField()
    optype = field.EnumField(choices=suite.enum.values(suite.enum.ptype))
    ocount = field.IntegerField()
    oprice = field.DecimalField(digits=10, decimals=2)
    callback = field.StringField(null=True)
    operator = field.StringField(default=suite.enum.operator.sys.code)


class Dealt(form.Form):
    id = field.IntegerField()
    dcount = field.IntegerField()
    dprice = field.DecimalField(digits=10, decimals=2)
    dcode = field.StringField(null=True)
    operator = field.StringField(default=suite.enum.operator.sys.code)


Buy = Order
Sell = Order
Bought = Dealt
Sold = Dealt


class Cancel(form.Form):
    id = field.IntegerField()
    operator = field.StringField(default=suite.enum.operator.sys.code)


class Canceled(form.Form):
    id = field.IntegerField()
    operator = field.StringField(default=suite.enum.operator.sys.code)


class Notify(form.Form):
    id = field.IntegerField()
    dcount = field.IntegerField()
    dprice = field.DecimalField(digits=10, decimals=2)
    dcode = field.StringField(null=True)
    status = field.EnumField(choices=suite.enum.values(suite.enum.order))
    operator = field.StringField(default=suite.enum.operator.sys.code)


