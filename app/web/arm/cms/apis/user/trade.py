"""
    api for cms
"""
import datetime, json, util
from django.db.models import Q
from adb import models
from cms import auth, resp, hint, forms, error
from .. import remote


@auth.catch_exception
@auth.need_login
def list(request):
    """
        list api
    :param request:
    :return:
    """
    form = forms.user.trade.List(request.GET)
    if not form.is_valid():
        raise error.invalid_parameters

    ## form parameters ##
    params = form.cleaned_data

    status, sdate, edate = params['status'], params['sdate'], params['edate']
    ## filters ##
    filters = {}
    if sdate:
        filters['ctime__gte'] = util.time.utime(sdate)
    if edate:
        filters['ctime__lt'] = util.time.utime(edate+datetime.timedelta(days=1))

    qs = []
    ## status options ##
    if status:
        qq = Q()
        for q in [(Q(status=s)) for s in status.split(',')]:
            qq = qq | q
        qs.append(qq)


    ## search words ##
    words = params['words']
    if words:
        if len(filters) == 0 and len(words) < 10 and words.isdigit():
            filters['id'] = int(words) # id, not phone number
        else :
            qs.append(Q(user__user=words) | Q(stock__id=words) | Q(stock__name__contains=words))

    ## get total count ##
    total = models.UserTrade.objects.filter(*qs, **filters).count()


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
    objects = []
    if orderby:
        if start is not None and end is not None:
            objects = models.UserTrade.objects.filter(*qs, **filters).order_by(orderby)[start:end]
        else:
            objects = models.UserTrade.objects.filter(*qs, **filters).order_by(orderby)
    else:
        if start is not None and end is not None:
            objects = models.UserTrade.objects.filter(*qs, **filters)[start:end]
        else:
            objects = models.UserTrade.objects.filter(*qs, **filters)

    ## make results ##
    rows = []
    for obj in objects:
        rows.append(obj.ddata())

    ## response data ##
    data = {
        'total': total,
        'rows': rows
    }

    return resp.success(data=data)


@auth.catch_exception
@auth.need_login
def get(request):
    """
        get order
    :param request:
    :return:
    """
    if request.method != 'GET':
        return resp.failure(msg='method not support')

    # get form data
    form = forms.user.trade.Get(request.GET)
    if not form.is_valid():
        return resp.failure(hint.ERR_FORM_DATA)

    # get parameters
    id, type = form.cleaned_data['id'], form.cleaned_data['_t']

    # get user trade detail
    trade = models.UserTrade.objects.get(id=id)

    # data for want
    if type=='d':
        rows = trade.ddata()
    elif type=='p':
        rows = trade.pdata()
    else:
        rows = trade.odata()

    data = {
        'status': trade.status,
        'total': len(rows),
        'rows': rows
    }

    # want formatted data
    return resp.success(data=data)

@auth.catch_exception
@auth.need_login
def add(request):
    """
        add api
    :param request:
    :return:
    """

    form = forms.user.trade.Add(request.POST)
    if form.is_valid():
        # clean form data
        params = form.cleaned_data

        # remote add new order
        data = remote.aam.trade_user_buy(**params)

        # get new trade object
        usertrade = models.UserTrade.objects.filter(id=data['trade']['id']).first()

        # response data
        data = usertrade.ddata()

        return resp.success(data=data)


@auth.catch_exception
@auth.need_login
def update(request):
    """
        update
    :param request:
    :return:
    """
    form = forms.user.trade.Update(request.POST)
    if form.is_valid():
        # get parameters
        params = form.cleaned_data

        # update order
        remote.aam.trade_update(**params)

        # get updated order
        obj = models.UserTrade.objects.get(id=params['id'])

        # response data
        data = obj.ddata()

        return resp.success(data=data)
    else:
        return resp.failure(str(form.errors))


@auth.need_login
def delete(request):
    """
        delete api
    :param request:
    :return:
    """
    form = forms.user.trade.Delete(request.POST)
    if form.is_valid():
        id = form.cleaned_data['id']
        models.UserTrade.objects.filter(id=id).delete()
        return resp.success()
    else:
        return resp.failure(str(form.errors))


@auth.need_login
def lever(request):
    try:
        form = forms.user.trade.Get(request.GET)
        if form.is_valid():
            # trade id
            tradeid = form.cleaned_data['id']

            # get fee records of order
            object = models.TradeLever.objects.get(trade__id=tradeid)

            ## make results ##
            rows = object.pdata()

            ## response data ##
            data = {
                'total': len(rows),
                'rows': rows
            }

            return resp.success(data=data)
        else:
            return resp.failure(str(form.errors))
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def fees(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        form = forms.user.trade.Get(request.GET)
        if form.is_valid():
            # trade id
            tradeid = form.cleaned_data['id']

            # get fee records of order
            objects = models.TradeFee.objects.filter(trade__id=tradeid).order_by('-ctime')

            ## get total count ##
            total = objects.count()

            ## make results ##
            rows = []
            for obj in objects:
                rows.append(obj.ddata())

            ## response data ##
            data = {
                'total': total,
                'rows': rows
            }

            return resp.success(data=data)
        else:
            return resp.failure(form.errors, [])
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def margins(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        form = forms.user.trade.Get(request.GET)
        if form.is_valid():
            # trade id
            tradeid = form.cleaned_data['id']

            # get margin records of order
            objects = models.TradeMargin.objects.filter(trade__id=tradeid).order_by('-ctime')

            ## get total count ##
            total = objects.count()

            ## make results ##
            rows = []
            for obj in objects:
                rows.append(obj.ddata())

            ## response data ##
            data = {
                'total': total,
                'rows': rows
            }

            return resp.success(data=data)
        else:
            return resp.failure(str(form.errors))
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def orders(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        form = forms.user.trade.Get(request.GET)
        if form.is_valid():
            # trade id
            tradeid = form.cleaned_data['id']

            # get margin records of order
            objects = models.TradeOrder.objects.filter(trade__id=tradeid).order_by('-otime')

            ## get total count ##
            #total = objects.count()

            ## make results ##
            rows = []
            for obj in objects:
                rows.extend(obj.pdata())

            ## response data ##
            data = {
                'total': len(rows),
                'rows': rows
            }

            return resp.success(data=data)
        else:
            return resp.failure(str(form.errors))
    except Exception as e:
        return resp.failure(str(e))


@auth.catch_exception
@auth.need_login
def status(request):
    """
        get order
    :param request:
    :return:
    """
    if request.method != 'GET':
        return resp.failure(msg='method not support')

    id = request.GET['id']

    # get order detail
    item = models.UserTrade.objects.get(id=id)
    if not item:
        return resp.failure(hint.ERR_FORM_DATA)

    # logs
    logs = []
    if item.slog:
        logs = json.loads(item.slog)

    # rows
    rows = []
    for log in logs:
        group = util.time.datetms(log['time'])
        del log['time']
        for k, v in log.items():
            rows.append({'name':k, 'value':v, 'group':group})

    ## response data ##
    data = {
        'total': len(rows),
        'rows': rows
    }

    return resp.success(data=data)


@auth.catch_exception
@auth.need_login
def process(request):
    """
        process user trade order
    :param request:
    :return:
    """
    form = forms.user.trade.Process(request.POST)
    if form.is_valid():
        # trade id
        tradeid, action = form.cleaned_data['id'], form.cleaned_data['act']

        # process trade option
        if action == 'buy':
            data = remote.aam.trade_sys_buy(trade=tradeid)
        elif action in ['sell', 'close']:
            data = remote.aam.trade_sys_sell(trade=tradeid)
        elif action == 'cancel':
            data = remote.aam.trade_sys_cancel(trade=tradeid)
        elif action == 'drop':
            data = remote.aam.trade_sys_drop(trade=tradeid)
        else:
            raise error.invalid_parameters

        # get processed trade object
        usertrade = models.UserTrade.objects.filter(id=tradeid).first()

        # response data
        data = usertrade.ddata()

        return resp.success(data=data)
    else:
        return resp.failure(str(form.errors))