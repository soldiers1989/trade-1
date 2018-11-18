"""

"""
from venus.orm import model, field, db
from . import config

# setup database
db.setup('arm', 'mysql', **config.DATABASES['arm'][config.MODE])


class Crond(model.Model):
    __table__ = 'tb_crond'

    id = field.AutoField()
    code = field.StringField(max_length=16)
    name = field.StringField(max_length=16)
    config = field.StringField(max_length=32)
    method = field.StringField(max_length=16)
    url = field.StringField()
    data = field.StringField(null=True)
    json = field.StringField(null=True)
    status = field.EnumField(choices=('started', 'stopped'))
    exclusive = field.BooleanField()
    maxkeep = field.IntegerField()
    ctime = field.IntegerField()
    mtime = field.IntegerField()
