from django import forms

class Add(forms.Form):
    user = forms.CharField(max_length=32, min_length=1)
    pwd = forms.CharField(max_length=32, min_length=6)
    name = forms.CharField(max_length=32, initial='', required=False)
    phone = forms.CharField(max_length=16, initial='', required=False)
    disable = forms.BooleanField(required=False)


class Modify(forms.Form):
    id = forms.IntegerField()
    name = forms.CharField(max_length=32, initial='')
    phone = forms.CharField(max_length=16, initial='')
    disable = forms.BooleanField(required=False)
