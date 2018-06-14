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


class Add(forms.Form):
    user = forms.IntegerField()
    stock = forms.CharField()
    lever = forms.IntegerField()
    coupon = forms.IntegerField(required=False)
    ptype = forms.CharField()
    ocount = forms.IntegerField(min_value=100)
    oprice = forms.DecimalField(required=False)