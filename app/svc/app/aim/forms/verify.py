from venus.form import form, field


class VerifyIDGet(form.Form):
    type = field.StringField(max_length=16) # image code type, n - number, s - alpha string, ns - alpha/number string
    length = field.IntegerField() # image code length


class VerifyNormalImageGet(form.Form):
    id = field.StringField(max_length=16)
    width = field.IntegerField()
    height = field.IntegerField()
    fonts = field.StringField(max_length=32)


class VerifyNormalImagePost(form.Form):
    id = field.StringField(max_length=16)
    code = field.StringField(max_length=16)


class VerifySessionImageGet(form.Form):
    type = field.StringField(max_length=16) # image code type, n - number, s - alpha string, ns - alpha/number string
    length = field.IntegerField() # image code length
    width = field.IntegerField()
    height = field.IntegerField()
    fonts = field.StringField(max_length=32)


class VerifySessionImagePost(form.Form):
    code = field.StringField(max_length=16)


class VerifyNormalSmsGet(form.Form):
    phone = field.StringField(max_length=16)
    tpl = field.StringField(max_length=16)
    length = field.IntegerField()


class VerifyNormalSmsPost(form.Form):
    phone = field.StringField(max_length=16)
    code = field.StringField(max_length=16)


class VerifyUserSmsGet(form.Form):
    tpl = field.StringField(max_length=16)
    length = field.IntegerField()


class VerifyUserSmsPost(form.Form):
    code = field.StringField(max_length=16)
