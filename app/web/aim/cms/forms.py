from django import forms


class Login(forms.Form):
    """
        login form
    """
    username = forms.CharField(max_length=32, min_length=1)
    password = forms.CharField(max_length=32, min_length=6)
    remember = forms.BooleanField()


class Admin(forms.Form):
    user = forms.CharField(max_length=32, min_length=1)
    pwd = forms.CharField(max_length=32, min_length=6)
    name = forms.CharField(max_length=32, min_length=0)
    phone = forms.CharField(max_length=16, min_length=0)
    disable = forms.BooleanField(required=False)
