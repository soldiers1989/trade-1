"""
    form data for order request
"""
from tlib.web import form, field
from .. import suite


class List(form.Form):
    status = field.StringField(null=True)
    date = field.DateField(null=True)
    sdate = field.DateField(null=True)
    edate = field.DateField(null=True)


class Order(form.Form):
    otype = field.EnumField(choices=suite.enum.values(suite.enum.otype))
    account = field.StringField()
    tcode = field.StringField()
    scode = field.StringField()
    sname = field.StringField()
    optype = field.EnumField(choices=suite.enum.values(suite.enum.ptype))
    ocount = field.IntegerField()
    oprice = field.DecimalField(digits=10, decimals=2)
    callback = field.StringField(null=True)
    operator = field.StringField(default=suite.enum.operator.sys.code)


class Cancel(form.Form):
    id = field.IntegerField()
    operator = field.StringField(default=suite.enum.operator.sys.code)


class Notify(form.Form):
    id = field.IntegerField()
    dcount = field.IntegerField(null=True)
    dprice = field.DecimalField(digits=10, decimals=2, null=True)
    dcode = field.StringField(null=True)
    status = field.EnumField(choices=suite.enum.values(suite.enum.order), null=True)
    operator = field.StringField(default=suite.enum.operator.sys.code)
