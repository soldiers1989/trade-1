from django import forms


class Add(forms.Form):
    name = forms.CharField(min_length=1, max_length=16)
    disable = forms.BooleanField(required=False)


class Update(forms.Form):
    id = forms.IntegerField()
    name = forms.CharField(min_length=1, max_length=16)
    disable = forms.BooleanField(required=False)

class Get(forms.Form):
    id = forms.IntegerField()

Delete = Get

class AddModule(forms.Form):
    id = forms.IntegerField()
    module = forms.IntegerField()

DelModule = AddModule
