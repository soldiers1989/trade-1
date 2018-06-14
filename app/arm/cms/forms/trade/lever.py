from django import forms


class List(forms.Form):
    disable = forms.BooleanField(required=False)


class Get(forms.Form):
    id = forms.IntegerField()

Delete = Get

class Add(forms.Form):
    id = forms.IntegerField(required=False)
    lever = forms.IntegerField(min_value=1.0, max_value=10.0)
    wline = forms.DecimalField(min_value=0.0, max_digits=2, decimal_places=2)
    sline = forms.DecimalField(min_value=0.0, max_digits=2, decimal_places=2)
    ofmin = forms.DecimalField(min_value=0.0, max_digits=10, decimal_places=2)
    ofrate = forms.DecimalField(min_value=0.0, max_digits=7, decimal_places=6)
    dfrate = forms.DecimalField(min_value=0.0, max_digits=7, decimal_places=6)
    psrate = forms.DecimalField(min_value=0.0, max_digits=7, decimal_places=6)
    mmin = forms.DecimalField(min_value=0.0, max_digits=10, decimal_places=2)
    mmax = forms.DecimalField(min_value=0.0, max_digits=10, decimal_places=2)
    disable = forms.BooleanField(initial=True, required=False)

Update = Add


class Order(forms.Form):
    sid = forms.IntegerField()
    tid = forms.IntegerField()
    sorder = forms.IntegerField()
    torder = forms.IntegerField()
