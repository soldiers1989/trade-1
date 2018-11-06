import time
from venus.orm import model, field, db
from venus.orm.query import Q

class User(model.Model):
    __table__ = 'tb_user'

    id = field.AutoField()
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
        'charset': 'utf8',
        'autocommit': False
}

db.setup('arm', 'mysql', **arm)


def select():
    with db.create() as d:
        objs = User.filter(d, Q(id=1)|Q(id__le=3)).all()
        print(objs)

def insert():
    with db.atomic() as d:
        user = User(user='123456788903', pwd='123456', phone='12345678903', money=0.0, ctime=int(time.time()), ltime=int(time.time()))
        n = user.save(d)
        d.commit()
        print(n)

def update():
    with db.atomic() as d:
        n = User.filter(d, id__in=(18,20)).update(disable=True)
        print(n)

def delete():
    with db.atomic() as d:
        n = User.filter(d, id__in=(18,20)).delete()
        print(n)

if __name__ == '__main__':
    select()
    #insert()
    update()
    delete()