from django import forms


class Add(forms.Form):
    parent = forms.IntegerField(required=False)
    code = forms.CharField(max_length=64, min_length=1, required=False)
    name = forms.CharField(max_length=32, min_length=1, required=True)
    path = forms.CharField(max_length=32, min_length=1, required=False)
    icon = forms.CharField(max_length=32, min_length=1, required=False)
    order = forms.IntegerField(initial=0, required=True)
    disable = forms.BooleanField(initial=False, required=False)


class Modify(forms.Form):
    id = forms.IntegerField(required=True)
    parent = forms.IntegerField(required=False)
    code = forms.CharField(max_length=64, min_length=1, required=False)
    name = forms.CharField(max_length=32, min_length=1, required=True)
    path = forms.CharField(max_length=128, min_length=1, required=False)
    icon = forms.CharField(max_length=32, min_length=1, required=False)
    order = forms.IntegerField(initial=0, required=True)
    disable = forms.BooleanField(initial=False, required=False)
