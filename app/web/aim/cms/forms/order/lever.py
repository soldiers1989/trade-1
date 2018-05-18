from django import forms


class Lever(forms.Form):
    id = forms.IntegerField(required=False)
    lever = forms.IntegerField(min_value=1.0, max_value=10.0)
    wline = forms.DecimalField(min_value=0.0, max_digits=2, decimal_places=2)
    sline = forms.DecimalField(min_value=0.0, max_digits=2, decimal_places=2)
    ofmin = forms.DecimalField(min_value=0.0, max_digits=10, decimal_places=2)
    ofrate = forms.DecimalField(min_value=0.0, max_digits=6, decimal_places=6)
    dfrate = forms.DecimalField(min_value=0.0, max_digits=6, decimal_places=6)
    psrate = forms.DecimalField(min_value=0.0, max_digits=6, decimal_places=6)
    mmin = forms.DecimalField(min_value=0.0, max_digits=10, decimal_places=2)
    mmax = forms.DecimalField(min_value=0.0, max_digits=10, decimal_places=2)
    order = forms.IntegerField(initial=0, required=False)
    disable = forms.BooleanField(initial=True, required=False)
