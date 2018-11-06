"""
    trade task forms
"""
from venus import form, field


class Start(form.Form):
    callback = field.StringField(null=True)


class Stop(form.Form):
    pass

