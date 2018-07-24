from django import forms


class List(forms.Form):
    page = forms.IntegerField(initial=1, min_value=1, required=False)
    rows = forms.IntegerField(initial=20, min_value=1, required=False)

    sort = forms.CharField(initial='id', required=False)
    order = forms.CharField(initial='asc', required=False)

    status = forms.CharField(required=False)
    limit = forms.CharField(required=False)
    words = forms.CharField(required=False)


class Add(forms.Form):
    id = forms.CharField(min_length=6, max_length=6)
    name = forms.CharField(min_length=1, max_length=16)
    jianpin = forms.CharField(min_length=1, max_length=16)
    quanpin = forms.CharField(min_length=1, max_length=32)
    status = forms.CharField(min_length=1, max_length=8)
    limit = forms.CharField(min_length=1, max_length=8)


class Update(forms.Form):
    id = forms.CharField(min_length=6, max_length=6)
    name = forms.CharField(min_length=1, max_length=16)
    jianpin = forms.CharField(min_length=1, max_length=16)
    quanpin = forms.CharField(min_length=1, max_length=32)
    status = forms.CharField(min_length=1, max_length=8)
    limit = forms.CharField(min_length=1, max_length=8)


class Delete(forms.Form):
    id = forms.IntegerField()


class Query(forms.Form):
    q = forms.CharField()


class Has(forms.Form):
    stock = forms.CharField()
