from django import forms


class Add(forms.Form):
    id = forms.IntegerField(required=False)
    parent = forms.IntegerField(required=False)
    name = forms.CharField(max_length=32, min_length=3, required=True)
    path = forms.CharField(max_length=128, initial='', required=False)
    #order = forms.IntegerField(initial=0, required=False)
    disable = forms.BooleanField(initial=False, required=False)


Update = Add

class Get(forms.Form):
    id = forms.IntegerField()

Delete = Get
