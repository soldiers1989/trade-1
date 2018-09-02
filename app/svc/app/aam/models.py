"""
    field
"""
from web import model, field
from app.aam import enum


class User(model.Model):
    id = field.IntegerField()
    user = field.StringField(max_length=16)
    pwd = field.StringField(max_length=64)
    phone = field.StringField(max_length=16)
    money = field.DecimalField(digits=10, decimals=2)
    disable = field.BooleanField(default=False)
    ctime = field.IntegerField() # create time
    ltime = field.IntegerField() # last access time


class UserCoupon(model.Model):
    id = field.IntegerField()
    user_id = field.IntegerField()
    name = field.StringField()
    money = field.DecimalField(digits=10, decimals=2)
    status = field.EnumField(choices=enum.values(enum.coupon))
    sdate = field.DateField()
    edate = field.DateField()
    ctime = field.IntegerField()
    utime = field.IntegerField(null=True)


class Lever(model.Model):
    id = field.IntegerField()
    lever = field.IntegerField()
    wline = field.DecimalField(digits=2, decimals=2)
    sline = field.DecimalField(digits=2, decimals=2)
    ofmin = field.DecimalField(digits=10, decimals=2)
    ofrate = field.DecimalField(digits=6, decimals=6)
    dfrate = field.DecimalField(digits=6, decimals=6)
    psrate = field.DecimalField(digits=6, decimals=6)
    mmin = field.DecimalField(digits=10, decimals=2)
    mmax = field.DecimalField(digits=10, decimals=2)
    order = field.IntegerField(default=0)
    disable = field.BooleanField(default=True)
    ctime = field.IntegerField()
    mtime = field.IntegerField()


class Stock(model.Model):
    id = field.StringField(max_length=8)
    name = field.StringField(max_length=16)
    jianpin = field.StringField(max_length=16)
    quanpin = field.StringField(max_length=32)
    status = field.EnumField(max_length=8, default='open', choices=enum.values(enum.stock))
    limit = field.EnumField(max_length=8, default='none', choices=enum.values(enum.risk))
    ctime = field.IntegerField()
    mtime = field.IntegerField()