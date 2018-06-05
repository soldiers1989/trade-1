from django.db  import models


# tb_module
class Module(models.Model):
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='+', null=True)
    name = models.CharField(max_length=32)
    path = models.CharField(max_length=128, blank=True)
    order = models.IntegerField(default=0)
    disable = models.BooleanField(default=False)
    ctime = models.BigIntegerField()

    class Meta:
        db_table = 'tb_module'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['parent'] = items['parent'].id if items['parent'] else None
        return items


# tb_role
class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, blank=True)
    disable = models.BooleanField(default=False)
    ctime = models.BigIntegerField()
    modules = models.ManyToManyField(Module, through='RoleModule', through_fields=('role', 'module'))

    class Meta:
        db_table = 'tb_role'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return items


# tb_admin
class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=32, unique=True)
    pwd = models.CharField(max_length=64)
    name = models.CharField(max_length=32, blank=True)
    phone = models.CharField(max_length=16, blank=True)
    disable = models.BooleanField(default=False)
    ctime = models.BigIntegerField()
    roles = models.ManyToManyField(Role, through='AdminRole', through_fields=('admin', 'role'))

    class Meta:
        db_table = 'tb_admin'

    def dict(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])


# tb_admin_role
class AdminRole(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    ctime = models.BigIntegerField()

    class Meta:
        db_table = 'tb_admin_role'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['role'] = items['role'].id if items['role'] else None
        items['admin'] = items['admin'].id if items['admin'] else None
        return items


# tb_role_module
class RoleModule(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    ctime = models.BigIntegerField()

    class Meta:
        db_table = 'tb_role_module'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['role'] = items['role'].id if items['role'] else None
        items['module'] = items['module'].id if items['module'] else None
        return items


# tb_trade_account
class TradeAccount(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16)
    account = models.CharField(max_length=16, unique=True)
    lmoney = models.DecimalField(max_digits=10, decimal_places=2)
    cfmin = models.DecimalField(max_digits=10, decimal_places=2)
    cfrate = models.DecimalField(max_digits=6, decimal_places=6)
    tfrate = models.DecimalField(max_digits=6, decimal_places=6)
    rfmin = models.DecimalField(max_digits=10, decimal_places=6)
    rfrate = models.DecimalField(max_digits=6, decimal_places=6)
    tpwd = models.CharField(max_length=16)
    cpwd = models.CharField(max_length=16)
    dept = models.CharField(max_length=16)
    version = models.CharField(max_length=16)
    disable = models.BooleanField(default=True)
    ctime = models.BigIntegerField()
    mtime = models.BigIntegerField()

    class Meta:
        db_table = 'tb_trade_account'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return items


# tb_lever
class Lever(models.Model):
    id = models.AutoField(primary_key=True)
    lever = models.IntegerField(unique=True)
    wline = models.DecimalField(max_digits=2, decimal_places=2)
    sline = models.DecimalField(max_digits=2, decimal_places=2)
    ofmin = models.DecimalField(max_digits=10, decimal_places=2)
    ofrate = models.DecimalField(max_digits=6, decimal_places=6)
    dfrate = models.DecimalField(max_digits=6, decimal_places=6)
    psrate = models.DecimalField(max_digits=6, decimal_places=6)
    mmin = models.DecimalField(max_digits=10, decimal_places=2)
    mmax = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.IntegerField(default=0)
    disable = models.BooleanField(default=True)
    ctime = models.BigIntegerField()
    mtime = models.BigIntegerField()

    class Meta:
        db_table = 'tb_lever'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return items


# tb_trade_order
class TradeOrder(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.ForeignKey('TradeAccount', on_delete=models.CASCADE)
    ordern = models.CharField(max_length=16)
    otype = models.CharField(max_length=8)  # order type
    ptype = models.CharField(max_length=8)  # price type
    status = models.CharField(max_length=8)  # order status
    ocode = models.CharField(max_length=16)  # order code
    oprice = models.DecimalField(max_digits=10, decimal_places=2)  # order price
    ocount = models.IntegerField()  # order count
    otime = models.BigIntegerField()  # order time
    dcode = models.CharField(max_length=16, null=True)  # deal code
    dprice = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # deal price
    dcount = models.IntegerField(null=True)  # deal count
    dtime = models.BigIntegerField(null=True)  # deal time

    class Meta:
        db_table = 'tb_trade_order'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return items


# tb_quote_agent
class QuoteAgent(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16)
    ip = models.CharField(max_length=16)
    port = models.IntegerField()
    disable = models.BooleanField(default=True)
    htime = models.BigIntegerField()
    ctime = models.BigIntegerField()

    class Meta:
        db_table = 'tb_quote_agent'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return items


# tb_quote_server
class QuoteServer(models.Model):
    id = models.AutoField(primary_key=True)
    agent = models.ForeignKey('QuoteAgent', on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    ip = models.CharField(max_length=16)
    port = models.IntegerField()
    disable = models.BooleanField(default=False)
    ctime = models.BigIntegerField()

    class Meta:
        db_table = 'tb_quote_server'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return items


# tb_trade_agent
class TradeAgent(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.ForeignKey('TradeAccount', on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    ip = models.CharField(max_length=16)
    port = models.IntegerField()
    disable = models.BooleanField(default=False)
    htime = models.BigIntegerField()
    ctime = models.BigIntegerField()

    class Meta:
        db_table = 'tb_trade_agent'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return items


# tb_trade_server
class TradeServer(models.Model):
    id = models.AutoField(primary_key=True)
    agent = models.ForeignKey('TradeAgent', on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    ip = models.CharField(max_length=16)
    port = models.IntegerField()
    disable = models.BooleanField(default=False)
    ctime = models.BigIntegerField()

    class Meta:
        db_table = 'tb_trade_server'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return items


# tb_stock
class Stock(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=16)
    jianpin = models.CharField(max_length=16)
    quanpin = models.CharField(max_length=32)
    status = models.CharField(max_length=8, default='open')
    limit = models.CharField(max_length=8, default='normal')
    ctime = models.BigIntegerField()
    mtime = models.BigIntegerField()

    class Meta:
        db_table = 'tb_stock'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return items


# tb_user
class User(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=16, unique=True)
    pwd = models.CharField(max_length=32)
    phone = models.CharField(max_length=16)
    money = models.DecimalField(max_digits=10, decimal_places=2)
    disable = models.BooleanField(default=False)
    ctime = models.BigIntegerField() # create time
    ltime = models.BigIntegerField() # last access time

    class Meta:
        db_table = 'tb_user'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return items


# tb_user_coupon
class UserCoupon(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    money = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=16, default='unused') #unused-未使用, used-已使用, deleted-已删除,  expired-已失效
    ctime = models.BigIntegerField()  # create time
    etime = models.BigIntegerField()  # expire time
    utime = models.BigIntegerField(null=True)  # used time

    class Meta:
        db_table = 'tb_user_coupon'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return items


# tb_user_bank
class UserBank(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    bank = models.CharField(max_length=16)
    name = models.CharField(max_length=16)
    account = models.CharField(max_length=32)
    deleted = models.BooleanField(default=False)
    ctime = models.BigIntegerField()  # create time
    mtime = models.BigIntegerField()  # modify time

    class Meta:
        db_table = 'tb_user_bank'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return items


# tb_user_bill
class UserBill(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    code = models.CharField(max_length=16, unique=True)
    item = models.CharField(max_length=16)
    detail = models.CharField(max_length=64)
    bmoney = models.DecimalField(max_digits=10, decimal_places=2) # bill money
    lmoney = models.DecimalField(max_digits=10, decimal_places=2) # left money
    ctime = models.BigIntegerField()  # create time

    class Meta:
        db_table = 'tb_user_bill'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return items


# tb_pay_gateway
class PayGateway(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16)
    icon = models.CharField(max_length=32)
    order = models.IntegerField(default=0)
    disable = models.BooleanField(default=True)
    ctime = models.BigIntegerField()  # create time
    mtime = models.BigIntegerField()  # modify time

    class Meta:
        db_table = 'tb_pay_gateway'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return items


# tb_pay_account
class PayAccount(models.Model):
    id = models.AutoField(primary_key=True)
    gateway = models.ForeignKey('PayGateway', on_delete=models.CASCADE)
    bank = models.CharField(max_length=16)
    name = models.CharField(max_length=16)
    account = models.CharField(max_length=32)
    disable = models.BooleanField(default=True)
    ctime = models.BigIntegerField()  # create time
    mtime = models.BigIntegerField()  # modify time

    class Meta:
        db_table = 'tb_pay_account'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return items


# tb_user_charge
class UserCharge(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    account = models.ForeignKey('PayAccount', on_delete=models.CASCADE)
    code = models.CharField(max_length=16, unique=True)
    money = models.DecimalField(max_digits=10, decimal_places=2)  # bill money
    status = models.CharField(max_length=16, default='paying')
    ctime = models.BigIntegerField()  # create time

    class Meta:
        db_table = 'tb_user_charge'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return items


# tb_user_draw
class UserDraw(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    code = models.CharField(max_length=16, unique=True)
    money = models.DecimalField(max_digits=10, decimal_places=2)
    bank = models.CharField(max_length=16)
    name = models.CharField(max_length=16)
    account = models.CharField(max_length=32)
    status = models.CharField(max_length=16, default='paying')
    ctime = models.BigIntegerField()  # create time

    class Meta:
        db_table = 'tb_user_draw'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return items


# tb_user_stock
class UserStock(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    ctime = models.BigIntegerField()  # create time
    dtime = models.BigIntegerField()  # delete time

    class Meta:
        db_table = 'tb_user_stock'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return items


# tb_user_trade
class UserTrade(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    coupon = models.ForeignKey('UserCoupon', on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=16, unique=True)
    hcount = models.IntegerField(default=0) # holding count
    fcount = models.IntegerField(default=0) # free count, sell able
    oprice = models.DecimalField(max_digits=10, decimal_places=2)
    ocount = models.IntegerField()
    bprice = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    bcount = models.IntegerField(null=True)
    sprice = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    scount = models.IntegerField(null=True)
    margin = models.DecimalField(max_digits=10, decimal_places=2)
    ofee = models.DecimalField(max_digits=10, decimal_places=2) # open fee
    ddays = models.IntegerField(default=0) # delay days
    dfee = models.DecimalField(max_digits=10, decimal_places=2, null=True) # delay fee
    tprofit = models.DecimalField(max_digits=10, decimal_places=2, null=True) # total profit
    sprofit = models.DecimalField(max_digits=10, decimal_places=2, null=True) # share profit
    status = models.CharField(max_length=16, default='tobuy')
    ctime = models.BigIntegerField()  # create time
    ftime = models.BigIntegerField(null=True)  # finish time

    class Meta:
        db_table = 'tb_user_trade'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['user'] = items['user'].user if items['user'] else None
        items['stock'] = items['stock'].name if items['stock'] else None
        items['coupon'] = items['coupon'].money if items['coupon'] else None
        items['lever'] = self.tradelever.dict()
        return items

    @staticmethod
    def cstatus(s):
        cm = {
                'tobuy': '待买入', 'buying': '买入中', 'holding': '持仓中',
                'tosell': '待卖出', 'selling': '卖出中', 'toclose': '待平仓', 'closing': '平仓中',
                'finished': '已结束', 'expired': '已失效'
              }
        return cm[s]


# tb_trade_lever
class TradeLever(models.Model):
    trade = models.OneToOneField('UserTrade', on_delete=models.CASCADE)
    lever = models.IntegerField()
    wline = models.DecimalField(max_digits=2, decimal_places=2)
    sline = models.DecimalField(max_digits=2, decimal_places=2)
    ofmin = models.DecimalField(max_digits=10, decimal_places=2)
    ofrate = models.DecimalField(max_digits=6, decimal_places=6)
    dfrate = models.DecimalField(max_digits=6, decimal_places=6)
    psrate = models.DecimalField(max_digits=6, decimal_places=6)
    mmin = models.DecimalField(max_digits=10, decimal_places=2)
    mmax = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'tb_trade_lever'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        del items['id']
        del items['trade']
        return items


# tb_trade_margin
class TradeMargin(models.Model):
    id = models.AutoField(primary_key=True)
    trade = models.ForeignKey('UserTrade', on_delete=models.CASCADE)
    item = models.CharField(max_length=16)
    money = models.DecimalField(max_digits=10, decimal_places=2)
    ctime = models.BigIntegerField()  # create time

    class Meta:
        db_table = 'tb_trade_margin'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['trade'] = items['trade'].id if items['trade'] else None
        return items


# tb_trade_fee
class TradeFee(models.Model):
    id = models.AutoField(primary_key=True)
    trade = models.ForeignKey('UserTrade', on_delete=models.CASCADE)
    item = models.CharField(max_length=8)
    detail = models.CharField(max_length=64, blank=True)
    nmoney = models.DecimalField(max_digits=10, decimal_places=2) # need pay money
    amoney = models.DecimalField(max_digits=10, decimal_places=2) # actual pay money
    ctime = models.BigIntegerField()  # create time

    class Meta:
        db_table = 'tb_trade_fee'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['trade'] = items['trade'].id if items['trade'] else None
        return items


# tb_file
class File(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=32)
    path = models.CharField(max_length=256)
    size = models.BigIntegerField()
    ctime = models.BigIntegerField()

    class Meta:
        db_table = 'tb_file'