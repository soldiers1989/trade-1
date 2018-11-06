"""
    stock task forms
"""
from venus import form, field


class Sync(form.Form):
    callback = field.StringField(null=True)


