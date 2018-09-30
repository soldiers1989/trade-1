"""
    task form
"""
from tlib.web import form, field


class Task(form.Form):
    callback = field.StringField(null=True)


