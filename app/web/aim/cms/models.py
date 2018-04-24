from django.db  import models

class A(models.Model):
    a_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, blank=False, default='a')

    class Meta:
        db_table = 'tb_a'


class B(models.Model):
    b_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, null=False, default='b')
    # bs = models.ManyToManyField(A, through='E')

    class Meta:
        db_table = 'tb_b'


class C(models.Model):
    c_id = models.AutoField(primary_key=True)
    a = models.ForeignKey(A, on_delete=models.CASCADE)
    b = models.ForeignKey(B, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_c'

"""
class A(models.Model):
    a_id = models.AutoField(primary_key=True)
    namea = models.CharField(max_length=32, blank=False, default='a')

    class Meta:
        db_table = 'tb_a'


class B(models.Model):
    b_id = models.AutoField(primary_key=True)
    nameb = models.CharField(max_length=32, null=False, blank=True)
    bs = models.ManyToManyField(A, through='E')

    class Meta:
        db_table = 'tb_b'


class C(models.Model):
    c_id = models.AutoField(primary_key=True)
    namec = models.CharField(max_length=32, null=False, blank=True)
    #relatea = models.ForeignKey(A, null=True)
    cs = models.ManyToManyField(A, through='E', db_column='ccc')

    class Meta:
        db_table = 'tb_c'


class D(models.Model):
    d_id = models.OneToOneField(A, null=False, db_column='d_id')
    named = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = 'tb_d'


class E(models.Model):
    e_id = models.AutoField(primary_key=True)
    namee = models.CharField(max_length=32, null=False, blank=True)
    a = models.ForeignKey(A)
    b = models.ForeignKey(B)
    c = models.ForeignKey(C)

    class Meta:
        db_table = 'tb_e'
"""