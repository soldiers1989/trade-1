"""
    trade task forms
"""
from tlib.web import form, field


class Start(form.Form):
    callback = field.StringField(null=True)


class Stop(form.Form):
    pass

