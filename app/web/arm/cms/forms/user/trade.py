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
    _t = forms.ChoiceField(choices=(('o','o'), ('d','d'), ('p','p')), required=False)


class GetOrders(forms.Form):
    code = forms.CharField(max_length=16)


class Add(forms.Form):
    user = forms.IntegerField()
    stock = forms.CharField()
    lever = forms.IntegerField()
    coupon = forms.IntegerField(required=False)
    optype = forms.CharField()
    oprice = forms.DecimalField(initial=0.0, required=False)
    ocount = forms.IntegerField(min_value=100)


class Process(forms.Form):
    id = forms.IntegerField()
    act = forms.CharField(max_length=16);
