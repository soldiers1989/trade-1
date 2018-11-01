from django import forms


class List(forms.Form):
    page = forms.IntegerField(initial=1, min_value=1, required=False)
    rows = forms.IntegerField(initial=20, min_value=1, required=False)

    sort = forms.CharField(initial='id', required=False)
    order = forms.CharField(initial='asc', required=False)

    disable = forms.CharField(required=False)
    words = forms.CharField(required=False)


class Add(forms.Form):
    account = forms.CharField(max_length=16)
    name = forms.CharField(max_length=16)
    money = forms.DecimalField(max_digits=10, decimal_places=2)
    cfmin = forms.DecimalField(max_digits=10, decimal_places=2)
    cfrate = forms.DecimalField(max_digits=6, decimal_places=6)
    tfrate = forms.DecimalField(max_digits=6, decimal_places=6)
    disable = forms.BooleanField(initial=True, required=False)


class Update(forms.Form):
    id = forms.IntegerField()
    name = forms.CharField(max_length=16)
    account = forms.CharField(max_length=16)
    money = forms.DecimalField(max_digits=10, decimal_places=2)
    cfmin = forms.DecimalField(max_digits=10, decimal_places=2)
    cfrate = forms.DecimalField(max_digits=6, decimal_places=6)
    tfrate = forms.DecimalField(max_digits=6, decimal_places=6)
    disable = forms.BooleanField(initial=True, required=False)


class Delete(forms.Form):
    id = forms.IntegerField()
