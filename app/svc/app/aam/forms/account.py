from venus.form import form, field


class Select(form.Form):
    """
        account select form for buy trade order
    """
    stock = field.StringField()
    optype = field.EnumField(choices=('xj', 'sj'))
    oprice = field.DecimalField(digits=10, decimals=2)
    ocount = field.IntegerField()
