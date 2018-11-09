import util
from cms import enum
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

    def ddata(self):
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

    def ddata(self):
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

    def ddata(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])


# tb_admin_role
class AdminRole(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    ctime = models.BigIntegerField()

    class Meta:
        db_table = 'tb_admin_role'

    def ddata(self):
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

    def ddata(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['role'] = items['role'].id if items['role'] else None
        items['module'] = items['module'].id if items['module'] else None
        return items


# tb_trade_account
class TradeAccount(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=16)
    money = models.DecimalField(max_digits=10, decimal_places=2)
    cfmin = models.DecimalField(max_digits=10, decimal_places=2)
    cfrate = models.DecimalField(max_digits=6, decimal_places=6)
    tfrate = models.DecimalField(max_digits=6, decimal_places=6)
    disable = models.BooleanField(default=True)
    ctime = models.BigIntegerField()
    mtime = models.BigIntegerField()

    class Meta:
        db_table = 'tb_trade_account'

    def ddata(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return items


# tb_account_order
class AccountOrder(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    tcode = models.CharField(max_length=16, verbose_name='交易编号')
    account = models.CharField(max_length=16, verbose_name='证券账户')
    scode = models.CharField(max_length=16, verbose_name='证券代码')
    sname = models.CharField(max_length=16, verbose_name='证券名称')
    ocode = models.CharField(max_length=16, null=True, verbose_name='委托编号')
    otype = models.CharField(max_length=16, verbose_name='委托类型')
    optype = models.CharField(max_length=16, verbose_name='报价类型')
    oprice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='委托价格')
    ocount = models.IntegerField(verbose_name='委托数量')
    odate = models.DateField(verbose_name='委托日期')
    otime = models.BigIntegerField(verbose_name='委托时间')
    dcode = models.CharField(max_length=16, null=True, verbose_name='成交编号')
    dprice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='成交价格')
    dcount = models.IntegerField(verbose_name='成交数量')
    ddate = models.DateField(null=True, verbose_name='成交日期')
    dtime = models.BigIntegerField(null=True, verbose_name='成交时间')
    status = models.CharField(max_length=16, verbose_name='委托状态')
    slog = models.TextField(blank=True, verbose_name='状态变更')
    ctime = models.BigIntegerField(verbose_name='创建时间')
    mtime = models.BigIntegerField(verbose_name='修改时间')

    class Meta:
        db_table = 'tb_account_order'

    def odata(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return items

    def ddata(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['_otype'] = enum.all['order']['type'][items['otype']] if items['otype'] else None
        items['_optype'] = enum.all['order']['price'][items['optype']] if items['optype'] else None
        items['_status'] = enum.all['order']['status'][items['status']] if items['status'] else None

        del items['slog']

        return items

    def pdata(self):
        # get data items & fields
        items, fields = self.ddata(), dict([(f.name, f.verbose_name) for f in self._meta.fields])

        # process status
        items['otype'] = items['_otype']
        items['optype'] = items['_optype']
        items['status'] = items['_status']
        del items['_otype']
        del items['_optype']
        del items['_status']

        # format order/deal time
        items['otime'] = util.time.datetms(items['otime'])
        items['dtime'] = util.time.datetms(items['dtime'])

        # property data rows
        rows = []
        for k, v in items.items():
            rows.append({'name':fields[k], 'value': v, 'group': items['otime']})

        return rows


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

    def ddata(self):
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

    def ddata(self):
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

    def ddata(self):
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

    def ddata(self):
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

    def ddata(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return items


# tb_user_coupon
class UserCoupon(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    type = models.CharField(max_length=16) # 
    name = models.CharField(max_length=64)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    detail = models.CharField(max_length=64)
    status = models.CharField(max_length=16, default='unused') #unused-未使用, used-已使用, deleted-已删除,  expired-已失效
    sdate = models.DateField() # start date
    edate = models.DateField()  # expire date
    ctime = models.BigIntegerField()  # create time
    utime = models.BigIntegerField(null=True)  # used time

    class Meta:
        db_table = 'tb_user_coupon'

    def ddata(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['user'] = items['user'].user if items['user'] else None
        items['_type'] = enum.all['coupon']['type'][items['type']] if items['type'] else None
        items['_status'] = enum.all['coupon']['status'][items['status']] if items['status'] else None
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

    def ddata(self):
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
    money = models.DecimalField(max_digits=10, decimal_places=2) # bill money
    bmoney = models.DecimalField(max_digits=10, decimal_places=2) # before money
    lmoney = models.DecimalField(max_digits=10, decimal_places=2) # left money
    ctime = models.BigIntegerField()  # create time

    class Meta:
        db_table = 'tb_user_bill'

    def ddata(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['user'] = items['user'].user if items['user'] else None
        return items


# tb_user_charge
class UserCharge(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    code = models.CharField(max_length=16, unique=True)
    money = models.DecimalField(max_digits=10, decimal_places=2)  # bill money
    status = models.CharField(max_length=16)
    ctime = models.BigIntegerField()  # create time

    class Meta:
        db_table = 'tb_user_charge'

    def ddata(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['user'] = items['user'].user if items['user'] else None
        items['_status'] = enum.all['charge']['status'][items['status']] if items['status'] else None
        return items


# tb_user_draw
class UserDraw(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    code = models.CharField(max_length=16, unique=True)
    money = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=16)
    idc = models.CharField(max_length=32)
    bank = models.CharField(max_length=16)
    account = models.CharField(max_length=32)
    status = models.CharField(max_length=16, default='topay')
    ctime = models.BigIntegerField()  # create time

    class Meta:
        db_table = 'tb_user_draw'

    def ddata(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['user'] = items['user'].user if items['user'] else None
        items['_status'] = enum.all['draw']['status'][items['status']] if items['status'] else None
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

    def ddata(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['stock'] = items['stock'].name if items['stock'] else None
        items['user'] = items['user'].user if items['user'] else None
        return items


# tb_user_trade
class UserTrade(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='用户ID')
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE, verbose_name='股票ID')
    coupon = models.ForeignKey('UserCoupon', on_delete=models.CASCADE, null=True, verbose_name='优惠券ID')
    tcode = models.CharField(max_length=16, unique=True, verbose_name='交易代码')
    optype = models.CharField(max_length=16, verbose_name='报价类型')
    oprice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='委托价格')
    ocount = models.IntegerField(verbose_name='委托数量')
    hprice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='持仓价格')
    hcount = models.IntegerField(verbose_name='持仓数量') # holding count
    fcount = models.IntegerField(verbose_name='可用数量') # free count, sell able
    bprice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='买入价格')
    bcount = models.IntegerField(verbose_name='买入数量')
    sprice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='卖出价格')
    scount = models.IntegerField(verbose_name='卖出数量')
    margin = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='保证金')
    ofee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='建仓费') # open fee
    dday = models.IntegerField(verbose_name='延期日') # delay days
    dfee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='延期费') # delay fee
    tprofit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='实际盈亏') # total profit
    sprofit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='盈利分成') # share profit
    account = models.CharField(null=True, max_length=16, verbose_name='交易账户')
    status = models.CharField(max_length=16, verbose_name='状态')
    slog = models.TextField(blank=True, verbose_name='状态变更')
    ctime = models.BigIntegerField(verbose_name='创建时间')  # create time
    mtime = models.BigIntegerField(verbose_name='修改时间')  # modify time

    class Meta:
        db_table = 'tb_user_trade'

    def ddata(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['_user'] = items['user'].user if items['user'] else None
        items['_stock'] = items['stock'].name if items['stock'] else None
        items['_optype'] = enum.all['order']['price'][items['optype']] if items['optype'] else None
        items['_status'] = enum.all['trade']['status'][items['status']] if items['status'] else None
        items['_lever'] = self.tradelever.lever

        items['user'], items['stock'], items['coupon'], items['lever'] = self.user_id, self.stock_id, self.coupon_id, self.tradelever.id

        del items['slog']

        return items

    def odata(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['user'], items['stock'], items['coupon'] = self.user_id, self.stock_id, self.coupon_id
        return items;

    def pdata(self):
        # get data items & fields
        items, fields = self.ddata(), dict([(f.name, f.verbose_name) for f in self._meta.fields])

        items['user'], items['stock'], items['optype'], items['status'] = items['_user'], items['_stock'], items['_optype'], items['_status']

        # add lever fields
        #fields['lever'] = '杠杆倍数'

        # format time
        items['ctime'] = util.time.datetms(items['ctime'])
        items['mtime'] = util.time.datetms(items['mtime'])

        # property data rows
        rows = self.tradelever.pdata()
        for k, v in items.items():
            if fields.get(k):
                rows.append({'name':fields[k], 'value': v, 'group': '订单详情'})

        return rows


# tb_trade_lever
class TradeLever(models.Model):
    trade = models.OneToOneField('UserTrade', on_delete=models.CASCADE, verbose_name='交易订单')
    lever = models.IntegerField(verbose_name='杠杆倍数')
    wline = models.DecimalField(max_digits=2, decimal_places=2, verbose_name='预警线')
    sline = models.DecimalField(max_digits=2, decimal_places=2, verbose_name='止损线')
    ofmin = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='保底费用')
    ofrate = models.DecimalField(max_digits=6, decimal_places=6, verbose_name='建仓费率')
    dfrate = models.DecimalField(max_digits=6, decimal_places=6, verbose_name='延期费率')
    psrate = models.DecimalField(max_digits=6, decimal_places=6, verbose_name='盈利分成')
    mmin = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='本金下限')
    mmax = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='本金上限')

    class Meta:
        db_table = 'tb_trade_lever'

    def odata(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['trade'] = self.trade_id
        return items

    def ddata(self):
        return self.odata()

    def pdata(self):
        # get data items & fields
        items, fields = self.ddata(), dict([(f.name, f.verbose_name) for f in self._meta.fields])

        # property data rows
        rows = []
        for k, v in items.items():
            rows.append({'name':fields[k], 'value': v, 'group': '杠杆详情'})

        return rows


# tb_trade_order
class TradeOrder(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    trade = models.ForeignKey('UserTrade', on_delete=models.CASCADE, verbose_name='订单ID')
    ocode = models.CharField(max_length=16, verbose_name='委托编号')
    account = models.CharField(null=True, max_length=16, verbose_name='证券账户')
    scode = models.CharField(max_length=16, verbose_name='证券代码')
    sname = models.CharField(max_length=16, verbose_name='证券名称')
    otype = models.CharField(max_length=16, verbose_name='委托类型')
    optype = models.CharField(max_length=16, verbose_name='报价类型')
    oprice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='委托价格')
    ocount = models.IntegerField(verbose_name='委托数量')
    odate = models.DateField(verbose_name='委托日期')
    otime = models.BigIntegerField(verbose_name='委托时间')
    dprice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='成交价格')
    dcount = models.IntegerField(verbose_name='成交数量')
    ddate = models.DateField(null=True, verbose_name='成交日期')
    dtime = models.BigIntegerField(null=True, verbose_name='成交时间')
    status = models.CharField(max_length=16, verbose_name='委托状态')
    slog = models.TextField(blank=True, verbose_name='状态变更')
    ctime = models.BigIntegerField(verbose_name='创建时间')
    mtime = models.BigIntegerField(verbose_name='修改时间')

    class Meta:
        db_table = 'tb_trade_order'

    def odata(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['trade'] = self.trade_id
        return items

    def ddata(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['trade'] = self.trade_id

        items['_otype'] = enum.all['order']['type'][items['otype']] if items['otype'] else None
        items['_optype'] = enum.all['order']['price'][items['optype']] if items['optype'] else None
        items['_status'] = enum.all['order']['status'][items['status']] if items['status'] else None

        del items['slog']

        return items

    def pdata(self):
        # get data items & fields
        items, fields = self.ddata(), dict([(f.name, f.verbose_name) for f in self._meta.fields])

        # process status
        items['otype'] = items['_otype']
        items['optype'] = items['_optype']
        items['status'] = items['_status']
        del items['_otype']
        del items['_optype']
        del items['_status']

        # format order/deal time
        items['otime'] = util.time.datetms(items['otime'])
        items['dtime'] = util.time.datetms(items['dtime'])

        # property data rows
        rows = []
        for k, v in items.items():
            rows.append({'name':fields[k], 'value': v, 'group': items['otime']})

        return rows


# tb_trade_margin
class TradeMargin(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    trade = models.ForeignKey('UserTrade', on_delete=models.CASCADE, verbose_name='订单ID')
    item = models.CharField(max_length=16, verbose_name='类目')
    money = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='金额')
    detail = models.CharField(max_length=64, verbose_name='详情')
    ctime = models.BigIntegerField(verbose_name='时间')  # create time

    class Meta:
        db_table = 'tb_trade_margin'

    def odata(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['trade'] = self.trade_id
        return items

    def ddata(self):
        return self.odata()

    def pdata(self):
        # get data items & fields
        items, fields = self.ddata(), dict([(f.name, f.verbose_name) for f in self._meta.fields])

        # format ctime
        items['ctime'] = util.time.datetms(items['ctime'])

        # property data rows
        rows = []
        for k, v in items.items():
            rows.append({'name': fields[k], 'value': v, 'group': items['ctime']})

        return rows


# tb_trade_fee
class TradeFee(models.Model):
    id = models.AutoField(primary_key=True)
    trade = models.ForeignKey('UserTrade', on_delete=models.CASCADE)
    item = models.CharField(max_length=8)
    detail = models.CharField(max_length=64, blank=True)
    money = models.DecimalField(max_digits=10, decimal_places=2)
    ctime = models.BigIntegerField()  # create time

    class Meta:
        db_table = 'tb_trade_fee'

    def odata(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        items['trade'] = self.trade_id
        return items

    def ddata(self):
        return self.odata()

    def pdata(self):
        # get data items & fields
        items, fields = self.ddata(), dict([(f.name, f.verbose_name) for f in self._meta.fields])

        # format ctime
        items['ctime'] = util.time.datetms(items['ctime'])

        # property data rows
        rows = []
        for k, v in items.items():
            rows.append({'name': fields[k], 'value': v, 'group': items['ctime']})

        return rows


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