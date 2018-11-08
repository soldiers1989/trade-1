from django import forms


class List(forms.Form):
    page = forms.IntegerField(initial=1, min_value=1, required=False)
    rows = forms.IntegerField(initial=20, min_value=1, required=False)

    sort = forms.CharField(initial='id', required=False)
    order = forms.CharField(initial='asc', required=False)

    sdate = forms.DateField(required=False)
    edate = forms.DateField(required=False)

    otype = forms.CharField(required=False)
    optype = forms.CharField(required=False)
    status = forms.CharField(required=False)
    words = forms.CharField(required=False)


class Add(forms.Form):
    trade = forms.IntegerField()
    account = forms.IntegerField()
    stock = forms.CharField(max_length=8)
    otype = forms.CharField(max_length=16)
    optype = forms.CharField(max_length=16)
    ocount = forms.IntegerField()
    oprice = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    otime = forms.DateTimeField()
    status = forms.CharField(max_length=16)


class Update(forms.Form):
    id = forms.IntegerField()
    dcount = forms.IntegerField(required=False)
    dprice = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    dtime = forms.DateTimeField(required=False)
    status = forms.CharField(max_length=16)


class Delete(forms.Form):
    id = forms.IntegerField()
