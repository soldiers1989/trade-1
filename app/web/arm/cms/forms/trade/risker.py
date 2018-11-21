from django import forms


class Get(forms.Form):
    type = forms.CharField(required=False)


class Sell(forms.Form):
    id = forms.CharField(required=False)


class Cancel(forms.Form):
    id = forms.CharField()
