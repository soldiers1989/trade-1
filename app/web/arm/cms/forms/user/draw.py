from django import forms


class List(forms.Form):
    page = forms.IntegerField(initial=1, min_value=1, required=False)
    rows = forms.IntegerField(initial=20, min_value=1, required=False)

    sort = forms.CharField(initial='id', required=False)
    order = forms.CharField(initial='asc', required=False)

    status = forms.CharField(required=False)
    words = forms.CharField(required=False)


class Add(forms.Form):
    user = forms.IntegerField()
    money = forms.DecimalField(max_digits=10, decimal_places=2)
    idc = forms.CharField(max_length=32)
    name = forms.CharField(max_length=16)
    bank = forms.CharField(max_length=16)
    account = forms.CharField(max_length=32)
    status = forms.CharField(min_length=1, max_length=16)
    ctime = forms.DateTimeField()


class Update(forms.Form):
    id = forms.IntegerField()
    money = forms.DecimalField(max_digits=10, decimal_places=2)
    idc = forms.CharField(max_length=32)
    name = forms.CharField(max_length=16)
    bank = forms.CharField(max_length=16)
    account = forms.CharField(max_length=32)
    status = forms.CharField(min_length=1, max_length=16)
    ctime = forms.DateTimeField()


class Delete(forms.Form):
    id = forms.IntegerField()
