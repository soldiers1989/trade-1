from django import forms


class List(forms.Form):
    page = forms.IntegerField(initial=1, min_value=1, required=False)
    rows = forms.IntegerField(initial=20, min_value=1, required=False)

    sort = forms.CharField(initial='id', required=False)
    order = forms.CharField(initial='asc', required=False)

    status = forms.CharField(required=False)
    sdate = forms.DateField(required=False)
    edate = forms.DateField(required=False)
    words = forms.CharField(required=False)


class Get(forms.Form):
    id = forms.IntegerField()
    _t = forms.CharField(required=False)


class Query(forms.Form):
    q = forms.CharField()


class Has(forms.Form):
    user = forms.CharField()


class ResetPwd(forms.Form):
    id = forms.IntegerField()
    pwd = forms.CharField(max_length=16, min_length=3)

