"""

"""
from venus.form import form, field


class TestForm1(form.Form):
    id = field.IntegerField(min_value=10, max_value=20)
    name = field.StringField(default='default', min_length=6, max_length=16)
    phone = field.StringField(length=11, pattern='^1\d{10}$')
    money = field.DecimalField(min_value=0.0, max_value=100.0, digits=10, decimals=2)
    disable = field.BooleanField(default=True)
    cdate = field.DateField(format='%Y/%m/%d')
    ctime = field.TimeField(format='%H-%M-%S')
    cdatetime = field.DateTimeField(format='%Y/%m/%d %H-%M-%S')


if __name__ == '__main__':
    form1 = TestForm1(id=10, phone='13126886633', money='0.23', cdate='2018/10/10', ctime='09-02-01', cdatetime='2018/10/10 09-02-01')
    print(form1)