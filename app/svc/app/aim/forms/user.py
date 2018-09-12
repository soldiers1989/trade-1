"""
    form data for trade request
"""
from tlib.web import form, field
from .. import suite


class UserExist(form.Form):
    phone = field.StringField(max_length=16)


class UserRegister(form.Form):
    phone = field.StringField(max_length=16)
    pwd = field.StringField(max_length=16)
    vcode = field.StringField(max_length=16)


class UserLogin(form.form):
    user = field.StringField(max_length=16)
    pwd = field.StringField(max_length=16)


class UserChangePwd(form.Form):
    opwd = field.StringField(max_length=16)
    npwd = field.StringField(max_length=16)


class UserResetPwd(form.Form):
    phone = field.StringField(max_length=16)
    vcode = field.StringField(max_length=16)
    npwd = field.StringField(max_length=16)