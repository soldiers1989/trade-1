from django import forms


class List(forms.Form):
    status = forms.ChoiceField(required=False, choices=(('started', 'started'),('stopped', 'stopped')))
    words = forms.CharField(required=False)


class Add(forms.Form):
    code = forms.CharField(min_length=1, max_length=16)
    name = forms.CharField(min_length=1, max_length=16)
    config = forms.CharField(min_length=1, max_length=32)
    method = forms.ChoiceField(choices=(('get','get'), ('post','post')))
    url = forms.CharField(min_length=1, max_length=256)
    data = forms.CharField(required=False)
    json = forms.CharField(required=False)
    status = forms.ChoiceField(choices=(('started','started'), ('stopped','stopped')))
    exclusive = forms.BooleanField()
    maxkeep = forms.IntegerField(required=False)


Update = Add


class Get(forms.Form):
    id = forms.IntegerField()


class Delete(forms.Form):
    id = forms.IntegerField()


class Enable(forms.Form):
    id = forms.IntegerField()


class Disable(forms.Form):
    id = forms.IntegerField()


class Execute(forms.Form):
    id = forms.IntegerField()


class Detail(forms.Form):
    id = forms.IntegerField()