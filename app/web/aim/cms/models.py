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

