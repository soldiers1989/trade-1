import time, datetime, util
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
        form = forms.trade.order.List(request.POST)
        if form.is_valid():
            ## form parameters ##
            params = form.cleaned_data

            otype, ptype, status, sdate, edate = params['otype'], params['ptype'], params['status'], params['sdate'], params['edate']
            ## filters ##
            filters = {}
            if otype:
                filters['otype'] = otype
            if ptype:
                filters['ptype'] = ptype
            if status:
                filters['status'] = status
            if sdate:
                filters['ctime__gte'] = util.time.utime(sdate)
            if edate:
                filters['ctime__lt'] = util.time.utime(edate+datetime.timedelta(days=1))

            ## search words ##
            q = Q()
            words = params['words']
            if words:
                if words.isdigit():
                    q = Q(account__account=words) | Q(stock_id=words) | Q(ocode=words) | Q(trade_id=words)
                else:
                    q = Q(stock__name__contains=words) | Q(account__name__contains=words)

            ## get total count ##
            total = models.TradeOrder.objects.filter(q, **filters).count()

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
                    objects = models.TradeOrder.objects.filter(q, **filters).order_by(orderby)[start:end]
                else:
                    objects = models.TradeOrder.objects.filter(q, **filters).order_by(orderby)
            else:
                if start is not None and end is not None:
                    objects = models.TradeOrder.objects.filter(q, **filters)[start:end]
                else:
                    objects = models.TradeOrder.objects.filter(q, **filters)

            ## make results ##
            rows = []
            for obj in objects:
                obj = obj.dict()
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
    form = forms.trade.order.Add(request.POST)
    if form.is_valid():
        params = form.cleaned_data
        # check trade/account
        if not models.UserTrade.objects.filter(id=params['trade']).exists() or \
            not models.TradeAccount.objects.filter(id=params['account']).exists():
            return resp.failure(hint.ERR_FORM_DATA)

        # add new record
        item = models.TradeOrder(trade_id=params['trade'],
                                 account_id=params['account'],
                                otype=params['otype'],
                                ptype=params['ptype'],
                                ocount=params['ocount'],
                                oprice=params['oprice'],
                                otime=params['otime'],
                                ocode=params['ocode'],
                                dcount=params['dcoout'],
                                dprice=params['dprice'],
                                dtime=params['dtime'],
                                status=params['status'])
        item.save()
        return resp.success(data=item.dict())
    else:
        return resp.failure(str(form.errors))


@auth.need_login
def update(request):
    """
        update
    :param request:
    :return:
    """
    form = forms.trade.order.Update(request.POST)
    if form.is_valid():
        params = form.cleaned_data

        models.TradeOrder.objects.filter(id=params['id']).update(trade_id=params['trade'],
                                                                 account_id=params['account'],
                                                                otype=params['otype'],
                                                                ptype=params['ptype'],
                                                                ocount=params['ocount'],
                                                                oprice=params['oprice'],
                                                                otime=params['otime'],
                                                                ocode=params['ocode'],
                                                                dcount=params['dcoout'],
                                                                dprice=params['dprice'],
                                                                dtime=params['dtime'],
                                                                status=params['status'])
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
    form = forms.trade.order.Delete(request.POST)
    if form.is_valid():
        id = form.cleaned_data['id']
        models.TradeOrder.objects.filter(id=id).delete()
        return resp.success()
    else:
        return resp.failure(str(form.errors))
