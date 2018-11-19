"""
    form data for trade request
"""
from venus.form import form, field
from .. import patterns


class UserExist(form.Form):
    phone = field.StringField(length=11, pattern=patterns.phone)


class UserReg(form.Form):
    phone = field.StringField(length=11, pattern=patterns.phone)
    pwd = field.StringField(max_length=16, min_length=1, null=True)
    vcode = field.StringField(max_length=16)


class UserLogin(form.Form):
    user = field.StringField(max_length=16)
    pwd = field.StringField(max_length=16, min_length=1, null=True)
    vcode = field.StringField(max_length=16, null=True)


class UserPwdChange(form.Form):
    opwd = field.StringField(max_length=16, min_length=1)
    npwd = field.StringField(max_length=16, min_length=1)


class UserPwdReset(form.Form):
    phone = field.StringField(max_length=16)
    vcode = field.StringField(max_length=16)
    npwd = field.StringField(max_length=16, min_length=1)
