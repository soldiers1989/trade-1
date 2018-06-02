from django import forms


class Login(forms.Form):
    """
        login form
    """
    user = forms.CharField(max_length=16, min_length=3)
    pwd = forms.CharField(max_length=16, min_length=3)
    remember = forms.BooleanField(required=False)

