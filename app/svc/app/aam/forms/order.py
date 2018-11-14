"""
    form data for order request
"""
from venus.form import form, field


class Place(form.Form):
    ocode = field.StringField(max_length=16)
    account = field.StringField(max_length=16)
    scode = field.StringField(max_length=8)
    sname = field.StringField(max_length=16)
    otype = field.EnumField(choices=('buy','sell'))
    optype = field.EnumField(choices=('sj','xj'))
    ocount = field.IntegerField()
    oprice = field.DecimalField(digits=10, decimals=2)
    operator = field.StringField(default='sys')


class Cancel(form.Form):
    id = field.IntegerField(null=True)
    ocode = field.StringField(null=True)
    operator = field.StringField(default='sys')


class Notify(form.Form):
    id = field.IntegerField()
    ocode = field.StringField()
    dcount = field.IntegerField(default=0)
    dprice = field.DecimalField(default=0.0, digits=10, decimals=2)
    dcode = field.StringField(null=True)
    status = field.EnumField(choices=('notsend','tosend','sending','sent','tocancel','canceling','pcanceled','tcanceled','fcanceled','pdeal','tdeal','dropped','expired'))
    operator = field.StringField(default='sys')


class OCode(form.Form):
    id = field.IntegerField()
    ocode = field.StringField()
