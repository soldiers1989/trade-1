from django import forms


class Login(forms.Form):
    """
        login form
    """
    username = forms.CharField(max_length=32, min_length=1)
    password = forms.CharField(max_length=32, min_length=6)
    remember = forms.BooleanField(required=False)


class AdminAdd(forms.Form):
    user = forms.CharField(max_length=32, min_length=1)
    pwd = forms.CharField(max_length=32, min_length=6)
    name = forms.CharField(max_length=32, min_length=0)
    phone = forms.CharField(max_length=16, min_length=0)
    disable = forms.BooleanField(required=False)


class AdminMod(forms.Form):
    id = forms.IntegerField()
    name = forms.CharField(max_length=32, min_length=0)
    phone = forms.CharField(max_length=16, min_length=0)
    disable = forms.BooleanField(required=False)


class ModuleAdd(forms.Form):
    parent = forms.IntegerField(required=False)
    name = forms.CharField(max_length=32, min_length=1, required=True)
    path = forms.CharField(max_length=32, min_length=1, required=False)
    icon = forms.CharField(max_length=32, min_length=1, required=False)
    order = forms.IntegerField(initial=0, required=True)
    disable = forms.BooleanField(initial=False, required=False)


class ModuleMod(forms.Form):
    id = forms.IntegerField(required=True)
    parent = forms.IntegerField(required=False)
    name = forms.CharField(max_length=32, min_length=1, required=True)
    path = forms.CharField(max_length=128, min_length=1, required=False)
    icon = forms.CharField(max_length=32, min_length=1, required=False)
    order = forms.IntegerField(initial=0, required=True)
    disable = forms.BooleanField(initial=False, required=False)
