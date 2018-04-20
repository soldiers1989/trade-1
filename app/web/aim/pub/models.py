from django.db import models


# tb_module
class Module(models.Model):
    module_id = models.AutoField(primary_key=True)
    parent = models.ForeignKey('self', null=True)
    name = models.CharField(max_length=32, null=False)
    path = models.CharField(max_length=128, null=True)
    icon = models.CharField(max_length=32, null=True)
    disable = models.BooleanField(null=False, default=False)
    ctime = models.BigIntegerField(null=False)

    class Meta:
        db_table = 'tb_module'


# tb_admin
class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=32, null=False)
    pwd = models.CharField(max_length=32, null=False)
    name = models.CharField(max_length=32, null=False)
    phone = models.CharField(max_length=16, null=False)
    disable = models.BooleanField(null=False, default=False)
    ctime = models.BigIntegerField(null=False)

    class Meta:
        db_table = 'tb_admin'


# tb_authority
class Authority(models.Model):
    auth_id = models.AutoField(primary_key=True)
    module_id = models.ForeignKey(Module, null=False)
    admin_id = models.ForeignKey(Admin, null=False)
    disable = models.BooleanField(null=False, default=False)
    ctime = models.BigIntegerField(null=False)

    class Meta:
        db_table = 'tb_auth'


# tb_file
class File(models.Model):
    file_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=32, null=False)
    name = models.CharField(max_length=256, null=False)
    size = models.BigIntegerField(null=False)
    path = models.TextField(null=False)
    ctime = models.BigIntegerField(null=False)

    class Meta:
        db_table = 'tb_file'
