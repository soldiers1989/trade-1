"""
    form data for trade request
"""
from venus import form, field


class UserExist(form.Form):
    phone = field.StringField(max_length=16)


class UserReg(form.Form):
    phone = field.StringField(max_length=16)
    pwd = field.StringField(max_length=16, null=True)
    vcode = field.StringField(max_length=16)


class UserLogin(form.Form):
    user = field.StringField(max_length=16)
    pwd = field.StringField(max_length=16, null=True)
    vcode = field.StringField(max_length=16, null=True)


class UserVerifyGet(form.Form):
    type = field.StringField(max_length=16)
    length = field.IntegerField()


class UserVerifyPost(form.Form):
    code = field.StringField(max_length=16)


class UserPwdChange(form.Form):
    opwd = field.StringField(max_length=16)
    npwd = field.StringField(max_length=16)


class UserPwdReset(form.Form):
    phone = field.StringField(max_length=16)
    vcode = field.StringField(max_length=16)
    npwd = field.StringField(max_length=16)