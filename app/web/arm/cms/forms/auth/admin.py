from django import forms


class Login(forms.Form):
    """
        login form
    """
    user = forms.CharField(min_length=3, max_length=16)
    pwd = forms.CharField(min_length=3, max_length=16)
    remember = forms.BooleanField(required=False)


class Pwd(forms.Form):
    """
        change password
    """
    pwd = forms.CharField(min_length=3, max_length=16)


class List(forms.Form):
    page = forms.IntegerField(initial=1, min_value=1, required=False)
    rows = forms.IntegerField(initial=20, min_value=1, required=False)
    sort = forms.CharField(initial='id', required=False)
    order = forms.CharField(initial='asc', required=False)
    sdate = forms.DateField(required=False)
    edate = forms.DateField(required=False)
    words = forms.CharField(required=False)


class Get(forms.Form):
    id = forms.IntegerField()


Delete = Get


class Add(forms.Form):
    user = forms.CharField(min_length=3, max_length=16)
    pwd = forms.CharField(min_length=3, max_length=16)
    name = forms.CharField(initial='', max_length=16, required=False)
    phone = forms.CharField(initial='', max_length=16, required=False)
    disable = forms.BooleanField(required=False)


class Update(forms.Form):
    id = forms.IntegerField()
    name = forms.CharField(initial='', min_length=3, max_length=16)
    phone = forms.CharField(initial='', max_length=16)
    disable = forms.BooleanField(required=False)


class ResetPwd(forms.Form):
    id = forms.IntegerField()
    pwd = forms.CharField(min_length=3, max_length=16)


class GetRoles(forms.Form):
    id = forms.IntegerField(required=False)


class AddRoles(forms.Form):
    id = forms.IntegerField()
    roles = forms.CharField()

DelRoles = AddRoles
