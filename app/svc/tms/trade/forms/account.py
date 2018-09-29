from tlib.web import form, field


class Delete(form.Form):
    aid = field.StringField()