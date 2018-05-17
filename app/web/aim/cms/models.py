from django.db  import models


# tb_module
class Module(models.Model):
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=64, null=True)
    name = models.CharField(max_length=32, null=False)
    path = models.CharField(max_length=128, null=True)
    icon = models.CharField(max_length=32, null=True)
    order = models.IntegerField(null=False, default=0)
    disable = models.BooleanField(null=False, default=False)
    ctime = models.BigIntegerField(null=False)

    class Meta:
        db_table = 'tb_module'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        if items['parent'] is not None:
            items['parent'] = items['parent'].id
        return items


# tb_admin
class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=32, null=False, unique=True)
    pwd = models.CharField(max_length=32, null=False)
    name = models.CharField(max_length=32, null=False)
    phone = models.CharField(max_length=16, null=False)
    disable = models.BooleanField(null=False, default=False)
    ctime = models.BigIntegerField(null=False, default=0)

    class Meta:
        db_table = 'tb_admin'

    def dict(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])


# tb_authority
class Authority(models.Model):
    id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=False)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, null=False)
    disable = models.BooleanField(null=False, default=False)
    ctime = models.BigIntegerField(null=False)

    class Meta:
        db_table = 'tb_auth'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])

        items['admin'] = items['admin'].id if items['admin'] is not None else None
        items['module'] = items['module'].id if items['module'] is not None else None

        return items


# tb_file
class File(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=32, null=False)
    name = models.CharField(max_length=256, null=False)
    size = models.BigIntegerField(null=False)
    path = models.TextField(null=False)
    ctime = models.BigIntegerField(null=False)

    class Meta:
        db_table = 'tb_file'


#tb_lever
class Lever(models.Model):
    id = models.AutoField(primary_key=True)
    lever = models.IntegerField(null=True)
    wline = models.DecimalField(max_digits=2, decimal_places=2, null=True)
    sline = models.DecimalField(max_digits=2, decimal_places=2, null=True)
    ofmin = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    ofrate = models.DecimalField(max_digits=6, decimal_places=6, null=True)
    dfrate = models.DecimalField(max_digits=6, decimal_places=6, null=True)
    psrate = models.DecimalField(max_digits=6, decimal_places=6, null=True)
    mmin = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    mmax = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    order = models.IntegerField(null=True, default=0)
    disable = models.BooleanField(null=False, default=True)
    ctime = models.BigIntegerField(null=True)
    mtime = models.BigIntegerField(null=True)

    class Meta:
        db_table = 'tb_lever'

    def dict(self):
        items = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])
        return items

# tb_stock
class Stock(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=16)
    jianpin = models.CharField(max_length=16)
    quanpin = models.CharField(max_length=32)
    status = models.IntegerField()
    tstatus = models.IntegerField()
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
    user = models.CharField(max_length=16)
    pwd = models.CharField(max_length=32)
    phone = models.CharField(max_length=16)
    money = models.DecimalField(max_digits=10, decimal_places=2)
    disable = models.BooleanField(default=False)
    ctime = models.BigIntegerField() # create time
    atime = models.BigIntegerField() # last access time

    class Meta:
        db_table = 'tb_user'


# tb_coupon
class Coupon(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.IntegerField()
    name = models.CharField(max_length=64)
    money = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField()
    ctime = models.BigIntegerField()  # create time
    etime = models.BigIntegerField()  # expire time
    utime = models.BigIntegerField(null=True)  # used time

    class Meta:
        db_table = 'tb_coupon'

# tb_user_bank
class UserBank(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.IntegerField()
    bank = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    account = models.CharField(max_length=32)
    deleted = models.BooleanField(default=False)
    ctime = models.BigIntegerField()  # create time
    mtime = models.BigIntegerField()  # modify time

    class Meta:
        db_table = 'tb_user_bank'


# tb_user_bill
class UserBill(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.IntegerField()
    name = models.CharField(max_length=32)
    bmoney = models.DecimalField(max_digits=10, decimal_places=2) # bill money
    lmoney = models.DecimalField(max_digits=10, decimal_places=2) # left money
    detail = models.CharField(max_length=128)
    ctime = models.BigIntegerField()  # create time

    class Meta:
        db_table = 'tb_user_bill'

# tb_user_stock
class UserStock(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.IntegerField()
    stock = models.CharField(max_length=8)
    deleted = models.BooleanField(default=False)
    ctime = models.BigIntegerField()  # create time
    dtime = models.BigIntegerField()  # delete time

    class Meta:
        db_table = 'tb_user_bank'


# tb_user_trade
class UserTrade(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.IntegerField()
    tacnt = models.IntegerField(null=True) # trade account
    stock = models.CharField(max_length=8)
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
    dfee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) # delay fee
    tprofit = models.DecimalField(max_digits=10, decimal_places=2, null=True) # total profit
    sprofit = models.DecimalField(max_digits=10, decimal_places=2, null=True) # share profit
    status = models.IntegerField()
    ctime = models.BigIntegerField()  # create time
    ftime = models.BigIntegerField(null=True)  # finish time

    class Meta:
        db_table = 'tb_user_trade'


# tb_trade_order
class TradeOrder(models.Model):
    id = models.AutoField(primary_key=True)
    trade = models.IntegerField()
    otype = models.CharField(max_length=8) # order type
    ptype = models.CharField(max_length=8) # price type
    status = models.CharField(max_length=8) # order status
    ocode = models.CharField(max_length=16) # order code
    oprice = models.DecimalField(max_digits=10, decimal_places=2) # order price
    ocount = models.IntegerField() # order count
    otime = models.BigIntegerField() # order time
    dcode = models.CharField(max_length=16, null=True) # deal code
    dprice = models.DecimalField(max_digits=10, decimal_places=2, null=True) # deal price
    dcount = models.IntegerField(null=True) # deal count
    dtime = models.BigIntegerField(null=True) # deal time

    class Meta:
        db_table = 'tb_trade_order'


# tb_trade_lever
class TradeLever(models.Model):
    order = models.IntegerField()
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


# tb_trade_margin
class TradeMargin(models.Model):
    id = models.AutoField(primary_key=True)
    trade = models.IntegerField()
    name = models.CharField(max_length=8)
    money = models.DecimalField(max_digits=10, decimal_places=2)
    ctime = models.BigIntegerField()  # create time

    class Meta:
        db_table = 'tb_trade_margin'


# tb_trade_fee
class TradeFee(models.Model):
    id = models.AutoField(primary_key=True)
    trade = models.IntegerField()
    name = models.CharField(max_length=8)
    nmoney = models.DecimalField(max_digits=10, decimal_places=2) # need pay money
    amoney = models.DecimalField(max_digits=10, decimal_places=2) # actual pay money
    detail = models.CharField(max_length=64)
    ctime = models.BigIntegerField()  # create time

    class Meta:
        db_table = 'tb_trade_fee'
