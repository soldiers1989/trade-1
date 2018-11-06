from tweb import orm
from tweb.orm.query import  Q

class User(orm.model.Model):
    __table__ = 'tb_user'

    id = orm.field.IntegerField()
    user = orm.field.StringField(max_length=16)
    pwd = orm.field.StringField(max_length=64)
    phone = orm.field.StringField(max_length=16)
    money = orm.field.DecimalField(digits=10, decimals=2)
    disable = orm.field.BooleanField(default=False)
    ctime = orm.field.IntegerField() # create time
    ltime = orm.field.IntegerField() # last access time


arm = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'root',
        'database': 'arm',
        'port': 3306,
        'charset': 'utf8'
}

orm.db.setup('arm', 'mysql', **arm)

if __name__ == '__main__':
    with orm.db.create() as db:
        objs = User.filter(db, Q(id=1)|Q(id__le=3)).all()
        print(objs)