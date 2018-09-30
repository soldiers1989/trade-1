"""
    stock task forms
"""
from tlib.web import form, field


class Sync(form.Form):
    callback = field.StringField(null=True)


