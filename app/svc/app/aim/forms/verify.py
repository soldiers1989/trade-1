from venus import form, field


class VerifyIDGet(form.Form):
    type = field.StringField(max_length=16) # image code type, n - number, s - alpha string, ns - alpha/number string
    length = field.IntegerField() # image code length


class VerifyImageGeneralGet(form.Form):
    id = field.StringField(max_length=16)
    width = field.IntegerField()
    height = field.IntegerField()
    fonts = field.StringField(max_length=32)


class VerifyImageGeneralPost(form.Form):
    id = field.StringField(max_length=16)
    code = field.StringField(max_length=16)


class VerifyImageSessionGet(form.Form):
    type = field.StringField(max_length=16) # image code type, n - number, s - alpha string, ns - alpha/number string
    length = field.IntegerField() # image code length
    width = field.IntegerField()
    height = field.IntegerField()
    fonts = field.StringField(max_length=32)


class VerifyImageSessionPost(form.Form):
    code = field.StringField(max_length=16)


class VerifySmsGet(form.Form):
    phone = field.StringField(max_length=16)
    type = field.StringField(max_length=16)
    length = field.IntegerField()


class VerifySmsPost(form.Form):
    phone = field.StringField(max_length=16)
    code = field.StringField(max_length=16)
