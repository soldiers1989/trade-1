from django import forms


class List(forms.Form):
    c = forms.CharField(max_length=32) # enum class
    i = forms.CharField(max_length=32) # enum item for class
