from django import forms

class AdminLogin(forms.Form):
    username = forms.CharField()