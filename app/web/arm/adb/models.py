import cube

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
    account = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=16)
    lmoney = models.DecimalField(max_digits=10, decimal_places=2)
    cfmin = models.DecimalField(max_digits=10, decimal_places=2)
    cfrate = models.DecimalField(max_digits=6, decimal_places=6)
    tfrate = models.DecimalField(max_digits=6, decimal_places=6)
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


# tb_user
class User(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=16, unique=True)
    pwd = models.CharField(max_length=64)
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


# tb_user_stat
class UserStat(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)

    ctime = models.BigIntegerField(null=True)  # create time
    mtime = models.BigIntegerField(null=True)  # modify time

    tpay = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    tdraw = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ttradec = models.IntegerField(null=True)
    ttradem = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    dpay = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ddraw = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    dtradec = models.IntegerField(null=True)
    dtradem = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    wpay = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    wdraw = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    wtradec = models.IntegerField(null=True)
    wtradem = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    mpay = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    mdraw = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    mtradec = models.IntegerField(null=True)
    mtradem = models.DecimalField(max_digits=10, decimal_places=2, null=True)


    class Meta:
        db_table = 'tb_user_stat'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        del items['user']
        return items

    def properties(self):
        props = []

        items = self.dict()
        del items['id']
        items['ctime'] = cube.util.time.datetms(items['ctime'])
        items['mtime'] = cube.util.time.datetms(items['mtime'])

        for key in items.keys():
            props.append({'name':self.keyname(key), 'value':items[key], "group":self.keygroup(key)})

        return props

    def keyname(self, key):
        key2name = {'dpay':'充值额','ddraw':'提现额','dtradec':'交易数','dtradem':'交易额',
                    'wpay':'充值额','wdraw':'提现额','wtradec':'交易数','wtradem':'交易额',
                    'mpay': '充值额', 'mdraw': '提现额', 'mtradec': '交易数', 'mtradem': '交易额',
                    'tpay': '充值额', 'tdraw': '提现额', 'ttradec': '交易数', 'ttradem': '交易额',
                    'ctime': '创建时间', 'mtime': '更新时间'}
        return key2name[key]

    def keygroup(self, key):
        key2group = {'dpay':'昨日','ddraw':'昨日','dtradec':'昨日','dtradem':'昨日',
                     'wpay':'上周','wdraw':'上周','wtradec':'上周','wtradem':'上周',
                     'mpay': '上月', 'mdraw': '上月', 'mtradec': '上月', 'mtradem': '上月',
                     'tpay': '累计', 'tdraw': '累计', 'ttradec': '累计', 'ttradem': '累计',
                     'ctime': '统计时间', 'mtime': '统计时间'}
        return key2group[key]

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
        del items['user']
        return items


# tb_user_bank
class UserBank(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    bank = models.CharField(max_length=16)
    name = models.CharField(max_length=16)
    idc = models.CharField(max_length=32)
    account = models.CharField(max_length=32)
    deleted = models.BooleanField(default=False)
    ctime = models.BigIntegerField()  # create time
    mtime = models.BigIntegerField()  # modify time

    class Meta:
        db_table = 'tb_user_bank'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        del items['user']
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
        del items['user']
        return items


# tb_user_charge
class UserCharge(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    code = models.CharField(max_length=16, unique=True)
    money = models.DecimalField(max_digits=10, decimal_places=2)  # bill money
    status = models.CharField(max_length=16, default='paying')
    ctime = models.BigIntegerField()  # create time

    class Meta:
        db_table = 'tb_user_charge'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['account'] = items['account'].name if items['account'] else None
        del items['user']
        return items


# tb_user_draw
class UserDraw(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    code = models.CharField(max_length=16, unique=True)
    money = models.DecimalField(max_digits=10, decimal_places=2)
    bank = models.CharField(max_length=16)
    name = models.CharField(max_length=16)
    idc = models.CharField(max_length=32)
    account = models.CharField(max_length=32)
    status = models.CharField(max_length=16, default='paying')
    ctime = models.BigIntegerField()  # create time

    class Meta:
        db_table = 'tb_user_draw'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        del items['user']
        return items


# tb_user_stock
class UserStock(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    ctime = models.BigIntegerField()  # create time
    dtime = models.BigIntegerField(null=True)  # delete time

    class Meta:
        db_table = 'tb_user_stock'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['stock'] = items['stock'].name if items['stock'] else None
        del items['user']
        return items


# tb_user_trade
class UserTrade(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    coupon = models.ForeignKey('UserCoupon', on_delete=models.CASCADE, null=True)
    account = models.ForeignKey('TradeAccount', on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=20, unique=True)
    oprice = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ocount = models.IntegerField()
    hprice = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    hcount = models.IntegerField(null=True) # holding count
    fcount = models.IntegerField(null=True) # free count, sell able
    bprice = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    bcount = models.IntegerField(null=True)
    sprice = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    scount = models.IntegerField(null=True)
    margin = models.DecimalField(max_digits=10, decimal_places=2)
    ofee = models.DecimalField(max_digits=10, decimal_places=2) # open fee
    ddays = models.IntegerField(null=True) # delay days
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
        items['statusd'] = self.statusd(items['status'])
        items['lever'] = self.tradelever.lever
        return items

    def statusd(self, s):
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


# tb_trade_order
class TradeOrder(models.Model):
    id = models.AutoField(primary_key=True)
    trade = models.ForeignKey('UserTrade', on_delete=models.CASCADE)
    account = models.ForeignKey('TradeAccount', on_delete=models.CASCADE, null=True)
    otype = models.CharField(max_length=16)
    ptype = models.CharField(max_length=16)
    ocount = models.IntegerField()
    oprice = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    otime = models.BigIntegerField()
    ocode = models.CharField(max_length=16, null=True)
    ostatus = models.CharField(max_length=16, null=True)
    dcount = models.IntegerField(null=True)
    dprice = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    dtime = models.BigIntegerField(null=True)
    status = models.CharField(max_length=16)

    class Meta:
        db_table = 'tb_trade_order'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['trade'] = items['trade'].id if items['trade'] else None
        items['account'] = items['account'].account if items['account'] else None
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