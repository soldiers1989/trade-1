import time
from adb import models
from django.db.models import Q
from cms import auth, resp, hint, forms


@auth.need_login
def list(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        form = forms.trade.account.List(request.POST)
        if form.is_valid():
            ## form parameters ##
            params = form.cleaned_data

            status = params['disable']
            ## filters ##
            filters = {}
            if status:
                filters['disable'] = True if status=='true' else False

            ## q ##
            q = Q()

            ## search words ##
            words = params['words']
            if words:
                if words.isdigit() and len(words) < 5:
                        filters['id'] = words
                else:
                    q = Q(account__startswith=words) | Q(name__startswith=words)

            ## get total count ##
            total = models.TradeAccount.objects.filter(q, **filters).count()

            # order by#
            sort, order =  params['sort'], params['order']
            if sort and order:
                order = '-' if order=='desc' else ''
                orderby = order+sort
            else:
                orderby = '-id'

            ## pagination##
            page, size, start, end = params['page'], params['rows'], None, None
            if page and size:
                start, end = (page-1)*size, page*size

            ## query results ##
            if orderby:
                if start is not None and end is not None:
                    objects = models.TradeAccount.objects.filter(q, **filters).order_by(orderby)[start:end]
                else:
                    objects = models.TradeAccount.objects.filter(q, **filters).order_by(orderby)
            else:
                if start is not None and end is not None:
                    objects = models.TradeAccount.objects.filter(q, **filters)[start:end]
                else:
                    objects = models.TradeAccount.objects.filter(q, **filters)

            ## make results ##
            rows = []
            for obj in objects:
                obj = obj.ddata()
                rows.append(obj)

            ## response data ##
            data = {
                'total': total,
                'rows': rows
            }
            return resp.success(data=data)
        else:
            return resp.failure(hint.ERR_FORM_DATA)
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def add(request):
    """
        add
    :param request:
    :return:
    """
    form = forms.trade.account.Add(request.POST)
    if form.is_valid():
        params = form.cleaned_data

        # check if user has exist
        items = models.TradeAccount.objects.filter(account=params['account'])
        if items.exists():
            return resp.failure(hint.ERR_RECORD_EXISTS)

        item = models.TradeAccount(account=params['account'],
                                name=params['name'],
                                money=params['money'],
                                cfmin=params['cfmin'],
                                cfrate=params['cfrate'],
                                tfrate=params['tfrate'],
                                disable=params['disable'],
                                ctime=int(time.time()),
                                mtime=int(time.time()))
        item.save()
        return resp.success(data=item.ddata())
    else:
        return resp.failure(str(form.errors))


@auth.need_login
def update(request):
    """
        update
    :param request:
    :return:
    """
    form = forms.trade.account.Update(request.POST)
    if form.is_valid():
        params = form.cleaned_data

        models.TradeAccount.objects.filter(id=params['id']).update(account=params['account'],
                                                                name=params['name'],
                                                                money=params['money'],
                                                                cfmin=params['cfmin'],
                                                                cfrate=params['cfrate'],
                                                                tfrate=params['tfrate'],
                                                                disable=params['disable'],
                                                                mtime=int(time.time()))
        return resp.success()
    else:
        return resp.failure(str(form.errors))


@auth.need_login
def delete(request):
    """
        delete api
    :param request:
    :return:
    """
    form = forms.trade.account.Delete(request.POST)
    if form.is_valid():
        id = form.cleaned_data['id']
        models.TradeAccount.objects.filter(id=id).delete()
        return resp.success()
    else:
        return resp.failure(str(form.errors))
