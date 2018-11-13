from django import forms


class List(forms.Form):
    page = forms.IntegerField(initial=1, min_value=1, required=False)
    rows = forms.IntegerField(initial=20, min_value=1, required=False)

    sort = forms.CharField(initial='id', required=False)
    order = forms.CharField(initial='asc', required=False)

    status = forms.CharField(required=False)
    sdate = forms.DateField(required=False)
    edate = forms.DateField(required=False)
    words = forms.CharField(required=False)


class Get(forms.Form):
    id = forms.IntegerField()
    _t = forms.ChoiceField(choices=(('o','o'), ('d','d'), ('p','p')), required=False)


class GetOrders(forms.Form):
    code = forms.CharField(max_length=16)


class Add(forms.Form):
    user = forms.IntegerField()
    stock = forms.CharField()
    lever = forms.IntegerField()
    coupon = forms.IntegerField(required=False)
    optype = forms.CharField()
    oprice = forms.DecimalField(required=False, initial=0.0, max_digits=10, decimal_places=2)
    ocount = forms.IntegerField(min_value=100)


class Update(forms.Form):
    id = forms.IntegerField()
    optype = forms.ChoiceField(required=False, choices=(('xj','xj'), ('sj','sj')))
    oprice = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    ocount = forms.IntegerField(required=False)
    hprice = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    hcount = forms.IntegerField(required=False) # holding count
    fcount = forms.IntegerField(required=False) # free count, sell able
    bprice = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    bcount = forms.IntegerField(required=False)
    sprice = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    scount = forms.IntegerField(required=False)
    margin = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    ofee = forms.DecimalField(required=False, max_digits=10, decimal_places=2) # open fee
    dday = forms.IntegerField(required=False) # delay days
    dfee = forms.DecimalField(required=False, max_digits=10, decimal_places=2) # delay fee
    tprofit = forms.DecimalField(required=False, max_digits=10, decimal_places=2) # total profit
    sprofit = forms.DecimalField(required=False, max_digits=10, decimal_places=2) # share profit
    account = forms.CharField(required=False, max_length=16)
    status = forms.ChoiceField(required=False, choices=('tobuy','buying','cancelbuy','buycanceling','canceled','hold','tosell','selling','cancelsell','sellcanceling','sold','toclose','closing','cancelclose','closecanceling','closed','expired','dropped'))


class Delete(forms.Form):
    id = forms.IntegerField()


class Process(forms.Form):
    id = forms.IntegerField()
    act = forms.CharField(max_length=16)
    dprice = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    dcount = forms.IntegerField(required=False)
