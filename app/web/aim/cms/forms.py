from django import forms


class LoginForm(forms.Form):
    """
        login form
    """
    username = forms.CharField(max_length=32, min_length=1)
    password = forms.CharField(max_length=32, min_length=6)
    remember = forms.BooleanField()

