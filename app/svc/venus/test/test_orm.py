from venus.orm import model, field, db
from venus.orm.query import Q

class User(model.Model):
    __table__ = 'tb_user'

    id = field.IntegerField()
    user = field.StringField(max_length=16)
    pwd = field.StringField(max_length=64)
    phone = field.StringField(max_length=16)
    money = field.DecimalField(digits=10, decimals=2)
    disable = field.BooleanField(default=False)
    ctime = field.IntegerField() # create time
    ltime = field.IntegerField() # last access time


arm = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'root',
        'database': 'arm',
        'port': 3306,
        'charset': 'utf8'
}

db.setup('arm', 'mysql', **arm)

if __name__ == '__main__':
    with db.create() as db:
        objs = User.filter(db, Q(id=1)|Q(id__le=3)).all()
        print(objs)