from django.db import models

# Create your models here.


# tb_admin
class Admin(models.Model):
    admin_id = models.IntegerField(primary_key=True)
    user = models.CharField(max_length=32, null=False)
    pwd = models.CharField(max_length=32, null=False)
    name = models.CharField(max_length=32, null=False)
    phone = models.CharField(max_length=16, null=False)
    disable = models.BooleanField(null=False, default=False)
    ctime = models.BigIntegerField(null=False)

    class Meta:
        db_table = 'tb_admin'


# tb_file
class File(models.Model):
    file_id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=32, null=False)
    name = models.CharField(max_length=256, null=False)
    size = models.BigIntegerField(null=False)
    path = models.TextField(null=False)
    ctime = models.BigIntegerField(null=False)

    class Meta:
        db_table = 'tb_file'

