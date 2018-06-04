from django import forms


class Login(forms.Form):
    """
        login form
    """
    user = forms.CharField(max_length=16, min_length=3)
    pwd = forms.CharField(max_length=16, min_length=3)
    remember = forms.BooleanField(required=False)


class Pwd(forms.Form):
    """
        change password
    """
    pwd = forms.CharField(max_length=16, min_length=3)


class List(forms.Form):
    page = forms.IntegerField(initial=1, min_value=1, required=False)
    rows = forms.IntegerField(initial=20, min_value=1, required=False)
    sort = forms.CharField(initial='id', required=False)
    order = forms.CharField(initial='asc', required=False)
    sdate = forms.DateField(required=False)
    edate = forms.DateField(required=False)
    words = forms.CharField(required=False)


class Add(forms.Form):
    user = forms.CharField(max_length=32, min_length=1)
    pwd = forms.CharField(max_length=32, min_length=6)
    name = forms.CharField(max_length=32, initial='', required=False)
    phone = forms.CharField(max_length=16, initial='', required=False)
    disable = forms.BooleanField(required=False)


class Modify(forms.Form):
    id = forms.IntegerField()
    name = forms.CharField(max_length=32, initial='')
    phone = forms.CharField(max_length=16, initial='')
    disable = forms.BooleanField(required=False)
