from django import forms


class Add(forms.Form):
    admin = forms.IntegerField(required=True)
    module = forms.IntegerField(required=True)
    disable = forms.BooleanField(initial=False, required=False)


class Modify(forms.Form):
    id = forms.IntegerField(required=True)
    admin = forms.IntegerField(required=True)
    module = forms.IntegerField(required=True)
    disable = forms.BooleanField(initial=False, required=False)
