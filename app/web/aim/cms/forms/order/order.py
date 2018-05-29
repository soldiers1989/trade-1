import datetime
from django import forms


class Query(forms.Form):
    status = forms.CharField(required=False)
    sdate = forms.DateField(required=False)
    edate = forms.DateField(required=False)
    words = forms.CharField(required=False)
    orderby = forms.CharField(required=False)
    order = forms.CharField(required=False)
    start = forms.IntegerField(required=False)
    count = forms.IntegerField(required=False)
