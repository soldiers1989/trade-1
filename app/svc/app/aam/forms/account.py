from tlib.web import form, field
from .. import suite


class Select(form.Form):
    """
        account select form for buy trade order
    """
    stock = field.StringField()
    type = field.EnumField(choices=suite.enum.values(suite.enum.ttype))
    optype = field.EnumField(choices=suite.enum.values(suite.enum.ptype))
    oprice = field.DecimalField(digits=10, decimals=2)
    ocount = field.IntegerField()
