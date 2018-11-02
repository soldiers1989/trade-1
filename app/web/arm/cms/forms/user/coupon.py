from django import forms


class List(forms.Form):
    page = forms.IntegerField(initial=1, min_value=1, required=False)
    rows = forms.IntegerField(initial=20, min_value=1, required=False)

    sort = forms.CharField(initial='id', required=False)
    order = forms.CharField(initial='asc', required=False)

    type = forms.CharField(required=False)
    status = forms.CharField(required=False)
    words = forms.CharField(required=False)


class Add(forms.Form):
    user = forms.IntegerField()
    type = forms.CharField(min_length=1, max_length=16)
    name = forms.CharField(min_length=1, max_length=64)
    value = forms.DecimalField(max_digits=10, decimal_places=2)
    status = forms.CharField(min_length=1, max_length=16)
    sdate = forms.DateField()
    edate = forms.DateField()


class Update(forms.Form):
    id = forms.IntegerField()
    type = forms.CharField(min_length=1, max_length=16)
    name = forms.CharField(min_length=1, max_length=64)
    value = forms.DecimalField(max_digits=10, decimal_places=2)
    status = forms.CharField(min_length=1, max_length=16)
    sdate = forms.DateField()
    edate = forms.DateField()


class Delete(forms.Form):
    id = forms.IntegerField()
