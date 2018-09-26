"""
    form data for order request
"""
from tlib.web import form, field
from .. import suite


class ListForm(form.Form):
    status = field.StringField()


class BuyForm(form.Form):
    pass


class SellForm(form.Form):
    pass


class CancelForm(form.Form):
    pass


class BoughtForm(form.Form):
    pass


class SoldForm(form.Form):
    pass


class CanceledForm(form.Form):
    pass
