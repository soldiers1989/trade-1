"""
    form data for trade request
"""
from venus.form import form, field


class Update(form.Form):
    id = field.IntegerField()
    optype = field.EnumField(null=True, choices=('xj', 'sj'))
    oprice = field.DecimalField(null=True, digits=10, decimals=2)
    ocount = field.IntegerField(null=True, )
    hprice = field.DecimalField(null=True, digits=10, decimals=2)
    hcount = field.IntegerField(null=True, default=0) # holding count
    fcount = field.IntegerField(null=True, default=0) # free count, sell able
    bprice = field.DecimalField(null=True, digits=10, decimals=2)
    bcount = field.IntegerField(null=True, default=0)
    sprice = field.DecimalField(null=True, digits=10, decimals=2)
    scount = field.IntegerField(null=True, default=0)
    margin = field.DecimalField(null=True, digits=10, decimals=2)
    ofee = field.DecimalField(null=True, digits=10, decimals=2) # open fee
    dday = field.IntegerField(null=True, default=0) # delay days
    dfee = field.DecimalField(null=True, digits=10, decimals=2) # delay fee
    tprofit = field.DecimalField(null=True, digits=10, decimals=2) # total profit
    sprofit = field.DecimalField(null=True, digits=10, decimals=2) # share profit
    account = field.StringField(null=True, max_lenght=16)
    status = field.EnumField(null=True, choices=('tobuy','buying','cancelbuy','buycanceling','canceled','hold','tosell','selling','cancelsell','sellcanceling','sold','toclose','closing','cancelclose','closecanceling','closed','expired','dropped'))


class UserBuy(form.Form):
    user = field.IntegerField()
    stock = field.StringField(max_length=8)
    lever = field.IntegerField()
    coupon = field.IntegerField(null=True)
    optype = field.EnumField(choices=('xj','sj'))
    oprice = field.DecimalField(digits=10, decimals=2, null=True)
    ocount = field.IntegerField()


class UserSell(form.Form):
    type = field.EnumField(choices=('sell', 'close'))
    user = field.IntegerField()
    trade = field.IntegerField()
    optype = field.EnumField(choices=('xj', 'sj'))
    oprice = field.DecimalField(digits=10, decimals=2)
    ocount = field.IntegerField()


class UserCancel(form.Form):
    user = field.IntegerField()
    trade = field.IntegerField()


class SysBuy(form.Form):
    trade = field.IntegerField()


class SysSell(form.Form):
    trade = field.IntegerField()


class SysCancel(form.Form):
    trade = field.IntegerField()


class SysDrop(form.Form):
    trade = field.IntegerField()


class OrderSent(form.Form):
    id = field.IntegerField()


class OrderCanceling(form.Form):
    id = field.IntegerField()


class OrderBought(form.Form):
    id = field.IntegerField()
    dcount = field.IntegerField()
    dprice = field.DecimalField(digits=10, decimals=2)


class OrderSold(form.Form):
    id = field.IntegerField()
    dcount = field.IntegerField()
    dprice = field.DecimalField(digits=10, decimals=2)


class OrderCanceled(form.Form):
    id = field.IntegerField()


class OrderExpired(form.Form):
    id = field.IntegerField()


class OrderUpdate(form.Form):
    id = field.IntegerField()
    account = field.StringField(null=True, max_lenght=16)
    optype = field.EnumField(null=True, choices=('xj', 'sj'))
    oprice = field.DecimalField(default='0.00', digits=10, decimals=2)
    ocount = field.IntegerField(null=True)
    otime = field.IntegerField(null=True)
    dprice = field.DecimalField(null=True, digits=10, decimals=2)
    dcount = field.IntegerField(null=True)
    dtime = field.IntegerField(null=True)
    status = field.EnumField(null=True, choices=('notsend','tosend','sending','sent','tocancel','canceling','pcanceled','tcanceled','fcanceled','pdeal','tdeal','dropped','expired'))
