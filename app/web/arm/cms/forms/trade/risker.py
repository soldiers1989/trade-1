from django import forms


class Get(forms.Form):
    type = forms.CharField(required=False)
