"""
    field
"""
from venus import model, field
from . import suite


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
    status = field.EnumField(choices=suite.enum.values(suite.enum.coupon))
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
    status = field.EnumField(max_length=8, default='open', choices=suite.enum.values(suite.enum.stock))
    limit = field.EnumField(max_length=8, default='none', choices=suite.enum.values(suite.enum.risk))
    ctime = field.IntegerField()
    mtime = field.IntegerField()


class TradeAccount(model.Model):
    id = field.IntegerField()
    type = field.StringField(max_length=16)
    account = field.StringField(max_length=16)
    name = field.StringField(max_length=16)
    lmoney = field.DecimalField(digits=10, decimals=2)
    cfmin = field.DecimalField(digits=10, decimals=2)
    cfrate = field.DecimalField(digits=6, decimals=6)
    tfrate = field.DecimalField(digits=6, decimals=6)
    disable = field.BooleanField()
    ctime = field.IntegerField()
    mtime = field.IntegerField()


class UserTrade(model.Model):
    id = field.IntegerField()
    user_id = field.IntegerField()
    stock_id = field.StringField(max_length=8)
    coupon_id = field.IntegerField(null=True)
    account = field.StringField(null=True, max_lenght=16)
    type = field.StringField(max_length=16)
    code = field.StringField(max_length=16)
    optype = field.EnumField(choices=suite.enum.values(suite.enum.ptype))
    oprice = field.DecimalField(digits=10, decimals=2)
    ocount = field.IntegerField()
    hprice = field.DecimalField(null=True, digits=10, decimals=2)
    hcount = field.IntegerField(null=True) # holding count
    fcount = field.IntegerField(null=True) # free count, sell able
    bprice = field.DecimalField(null=True, digits=10, decimals=2)
    bcount = field.IntegerField(null=True)
    sprice = field.DecimalField(null=True, digits=10, decimals=2)
    scount = field.IntegerField(null=True)
    margin = field.DecimalField(null=True, digits=10, decimals=2)
    ofee = field.DecimalField(null=True, digits=10, decimals=2) # open fee
    ddays = field.IntegerField(null=True) # delay days
    dfee = field.DecimalField(null=True, digits=10, decimals=2) # delay fee
    tprofit = field.DecimalField(null=True, digits=10, decimals=2) # total profit
    sprofit = field.DecimalField(null=True, digits=10, decimals=2) # share profit
    status = field.EnumField(choices=suite.enum.values(suite.enum.trade))
    slog = field.StringField(null=True)
    ctime = field.IntegerField()  # create time
    utime = field.IntegerField()  # update time
    btime = field.IntegerField(null=True)  # bought time
    stime = field.IntegerField(null=True)  # sold time
    etime = field.IntegerField(null=True) # end time


class TradeOrder(model.Model):
    id = field.IntegerField()
    account = field.StringField()
    sname = field.StringField(max_length=16)
    scode = field.StringField(max_length=16)
    tcode = field.StringField()
    otype = field.StringField(max_length=16)
    optype = field.StringField(max_length=16)
    ocount = field.IntegerField()
    oprice = field.DecimalField(digits=10, decimals=2, null=True)
    otime = field.IntegerField()
    ocode = field.StringField(max_length=16, null=True)
    dcount = field.IntegerField(null=True)
    dprice = field.DecimalField(digits=10, decimals=2, null=True)
    dtime = field.IntegerField(null=True)
    dcode = field.StringField(max_length=16, null=True)
    status = field.EnumField(choices=suite.enum.values(suite.enum.order))
    slog = field.StringField(null=True)
    ctime = field.IntegerField()
    utime = field.IntegerField()


class TradeLever(model.Model):
    id = field.IntegerField()
    trade_id = field.IntegerField()
    lever = field.IntegerField()
    wline = field.DecimalField(digits=2, decimals=2)
    sline = field.DecimalField(digits=2, decimals=2)
    ofmin = field.DecimalField(digits=10, decimals=2)
    ofrate = field.DecimalField(digits=6, decimals=6)
    dfrate = field.DecimalField(digits=6, decimals=6)
    psrate = field.DecimalField(digits=6, decimals=6)
    mmin = field.DecimalField(digits=10, decimals=2)
    mmax = field.DecimalField(digits=10, decimals=2)
