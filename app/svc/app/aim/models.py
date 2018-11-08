"""
    field
"""
from venus.orm import model, field, db
from . import config

# setup database
db.setup('arm', 'mysql', **config.DATABASES['aim'][config.MODE])


class User(model.Model):
    __table__ = 'tb_user'

    id = field.AutoField()
    user = field.StringField(max_length=16)
    pwd = field.StringField(max_length=64)
    phone = field.StringField(max_length=16)
    money = field.DecimalField(digits=10, decimals=2)
    disable = field.BooleanField(default=False)
    ctime = field.IntegerField() # create time
    ltime = field.IntegerField() # last access time


class UserCoupon(model.Model):
    __table__ = 'tb_user_coupon'

    id = field.AutoField()
    user_id = field.IntegerField()
    type = field.StringField(max_length=16)
    name = field.StringField(max_length=64)
    value = field.DecimalField(digits=10, decimals=2)
    status = field.EnumField(choices=('notused', 'used', 'expired'))
    sdate = field.DateField()
    edate = field.DateField()
    ctime = field.IntegerField()
    utime = field.IntegerField(null=True)


class UserBank(model.Model):
    __table__ = 'tb_user_bank'

    id = field.AutoField()
    user_id = field.IntegerField()
    bank = field.StringField(max_length=16)
    name = field.StringField(max_length=16)
    idc = field.StringField(max_length=32)
    account = field.StringField(max_length=32)
    deleted = field.BooleanField(default=False)
    ctime = field.IntegerField()  # create time
    mtime = field.IntegerField()  # modify time


class UserBill(model.Model):
    __table__ = 'tb_user_bill'

    id = field.AutoField()
    user_id = field.IntegerField()
    code = field.StringField(max_length=16)
    item = field.StringField(max_length=16)
    detail = field.StringField(max_length=64)
    money = field.DecimalField(digits=10, decimals=2) # bill money
    bmoney = field.DecimalField(digits=10, decimals=2) # before money
    lmoney = field.DecimalField(digits=10, decimals=2) # left money
    ctime = field.IntegerField()  # create time


# tb_user_charge
class UserCharge(model.Model):
    __table__ = 'tb_user_charge'

    id = field.AutoField()
    user_id = field.IntegerField()
    code = field.StringField(max_length=16)
    money = field.DecimalField(digits=10, decimals=2)  # bill money
    status = field.EnumField(choices=('topay', 'paid', 'expired'))
    ctime = field.IntegerField()  # create time


# tb_user_draw
class UserDraw(model.Model):
    __table__ = 'tb_user_draw'

    id = field.AutoField()
    user_id = field.IntegerField()
    code = field.StringField(max_length=16)
    money = field.DecimalField(digits=10, decimals=2)
    name = field.StringField(max_length=16)
    idc = field.StringField(max_length=32)
    bank = field.StringField(max_length=16)
    account = field.StringField(max_length=32)
    status = field.EnumField(choices=('topay', 'paid', 'denied'))
    ctime = field.IntegerField()  # create time


# tb_user_stock
class UserStock(model.Model):
    __table__ = 'tb_user_stock'

    id = field.AutoField()
    user_id = field.IntegerField()
    stock_id = field.StringField(max_length=16)
    deleted = field.BooleanField(default=False)
    ctime = field.IntegerField()  # create time
    dtime = field.IntegerField(null=True)  # delete time


class Lever(model.Model):
    __table__ = 'tb_lever'

    id = field.AutoField()
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
    __table__ = 'tb_user_charge'

    id = field.StringField(max_length=8)
    name = field.StringField(max_length=16)
    jianpin = field.StringField(max_length=16)
    quanpin = field.StringField(max_length=32)
    status = field.EnumField(max_length=8, choices=('open', 'close', 'delisted'))
    limit = field.EnumField(max_length=8, choices=('none', 'nobuy', 'nodelay'))
    ctime = field.IntegerField()
    mtime = field.IntegerField()


class TradeAccount(model.Model):
    __table__ = 'tb_trade_account'

    id = field.AutoField()
    account = field.StringField(max_length=16)
    name = field.StringField(max_length=16)
    money = field.DecimalField(digits=10, decimals=2)
    cfmin = field.DecimalField(digits=10, decimals=2)
    cfrate = field.DecimalField(digits=6, decimals=6)
    tfrate = field.DecimalField(digits=6, decimals=6)
    disable = field.BooleanField()
    ctime = field.IntegerField()
    mtime = field.IntegerField()


class UserTrade(model.Model):
    __table__ = 'tb_user_trade'

    id = field.AutoField()
    user_id = field.IntegerField()
    stock_id = field.StringField(max_length=8)
    coupon_id = field.IntegerField(null=True)
    type = field.StringField(max_length=16)
    code = field.StringField(max_length=16)
    optype = field.EnumField(choices=('xj', 'sj'))
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
    dday = field.IntegerField(null=True) # delay days
    dfee = field.DecimalField(null=True, digits=10, decimals=2) # delay fee
    tprofit = field.DecimalField(null=True, digits=10, decimals=2) # total profit
    sprofit = field.DecimalField(null=True, digits=10, decimals=2) # share profit
    account = field.StringField(null=True, max_lenght=16)
    status = field.EnumField(choices=('tobuy','buying','cancelbuy','buycanceling','canceled','hold','tosell','selling','cancelsell','sellcanceling','sold','toclose','closing','cancelclose','closecanceling','closed','expired','dropped'))
    slog = field.StringField(default='')
    ctime = field.IntegerField()  # create time
    mtime = field.IntegerField()  # modify time


class TradeOrder(model.Model):
    __table__ = 'tb_trade_order'

    id = field.AutoField()
    tcode = field.StringField(max_length=16)
    scode = field.StringField(max_length=8)
    sname = field.StringField(max_length=16)
    ocode = field.StringField(max_length=16, null=True)
    otype = field.EnumField(choices=('buy', 'sell'))
    optype = field.EnumField(choices=('sj', 'xj'))
    oprice = field.DecimalField(digits=10, decimals=2)
    ocount = field.IntegerField()
    odate = field.DateField()
    otime = field.IntegerField()
    dcode = field.StringField(max_length=16, null=True)
    dprice = field.DecimalField(digits=10, decimals=2)
    dcount = field.IntegerField(null=True)
    ddate = field.DateField()
    dtime = field.IntegerField(null=True)
    status = field.EnumField(choices=('notsend','tosend','sending','sent','tocancel','canceling','pcanceled','tcanceled','fcanceled','pdeal','tdeal','dropped','expired'))
    slog = field.StringField(default='')
    ctime = field.IntegerField()
    mtime = field.IntegerField()


class TradeLever(model.Model):
    __table__ = 'tb_trade_lever'

    id = field.AutoField()
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
