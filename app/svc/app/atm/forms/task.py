"""
    task form
"""
from venus import form, field


class Task(form.Form):
    callback = field.StringField(null=True)


