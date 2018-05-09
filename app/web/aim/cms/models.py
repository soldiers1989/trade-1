import time
from django.db  import models


# tb_module
class Module(models.Model):
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, null=False)
    path = models.CharField(max_length=128, null=True)
    icon = models.CharField(max_length=32, null=True)
    order = models.IntegerField(null=False, default=0)
    disable = models.BooleanField(null=False, default=False)
    ctime = models.BigIntegerField(null=False)

    class Meta:
        db_table = 'tb_module'


# tb_admin
class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=32, null=False)
    pwd = models.CharField(max_length=32, null=False)
    name = models.CharField(max_length=32, null=False)
    phone = models.CharField(max_length=16, null=False)
    disable = models.BooleanField(null=False, default=False)
    ctime = models.BigIntegerField(null=False, default=int(time.time()))

    class Meta:
        db_table = 'tb_admin'


# tb_authority
class Authority(models.Model):
    id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=False)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, null=False)
    disable = models.BooleanField(null=False, default=False)
    ctime = models.BigIntegerField(null=False)

    class Meta:
        db_table = 'tb_auth'


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
