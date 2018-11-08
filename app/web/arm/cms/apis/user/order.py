import time, json, datetime, util
from adb import models
from django.db.models import Q
from cms import auth, resp, hint, forms, enum, state


@auth.need_login
def list(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        form = forms.user.order.List(request.GET)
        if form.is_valid():
            ## form parameters ##
            params = form.cleaned_data

            otype, optype, status, sdate, edate = params['otype'], params['optype'], params['status'], params['sdate'], params['edate']
            ## filters ##
            filters = {}
            if otype:
                filters['otype'] = otype
            if optype:
                filters['optype'] = optype
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
                    q = Q(account=words) | Q(scode=words) | Q(id=words)
                else:
                    q = Q(sname__contains=words) | Q(tcode=words)

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
                rows.append(obj.ddata())

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
    form = forms.user.order.Add(request.POST)
    if form.is_valid():
        params = form.cleaned_data
        # check trade/account
        if not models.UserTrade.objects.filter(id=params['trade']).exists() or \
            not models.TradeAccount.objects.filter(id=params['account']).exists() or \
            not models.Stock.objects.filter(id=params['stock']).exists():
            return resp.failure(hint.ERR_FORM_DATA)

        # add new record
        item = models.TradeOrder(trade_id=params['trade'],
                                 account_id=params['account'],
                                otype=params['otype'],
                                optype=params['optype'],
                                ocount=params['ocount'],
                                oprice=params['oprice'],
                                otime=params['otime'].timestamp(),
                                status=params['status'])
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
    form = forms.user.order.Update(request.POST)
    if form.is_valid():
        # get parameters
        params = form.cleaned_data
        id, dcount, dprice, dtime, status = params['id'], params['dcount'], params['dprice'], params['dtime'], params['status']

        # get order object
        order = models.TradeOrder.objects.get(id=id)
        if order is None:
            return resp.failure(hint.ERR_FORM_DATA)

        # get admin object
        admin = models.Admin.objects.get(id=auth.get_admin_id(request))
        if admin is None:
            return resp.failure(hint.ERR_NOT_AUTHORIZED)

        # update trade

        # update status change log
        logs = [{'user': admin.user, 'action':'修改', 'before': enum.all['order']['status'].get(order.status), 'after': enum.all['order']['status'].get(status), 'time': int(time.time())}]
        if order.slog is not None:
            logs.extend(json.loads(order.slog))

        # update order
        order.dcount, order.dprice, order.dtime, order.status, order.slog = dcount, dprice, dtime.timestamp(), status, json.dumps(logs)
        order.save()

        return resp.success(data=order.ddata())
    else:
        return resp.failure(str(form.errors))


@auth.need_login
def delete(request):
    """
        delete api
    :param request:
    :return:
    """
    form = forms.user.order.Delete(request.POST)
    if form.is_valid():
        id = form.cleaned_data['id']
        models.TradeOrder.objects.filter(id=id).delete()
        return resp.success()
    else:
        return resp.failure(str(form.errors))


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
    item = models.TradeOrder.objects.get(id=id)
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
def nextstatus(request):
    """
        get next status
    :param request:
    :return:
    """
    if request.method != 'GET':
        return resp.failure(msg='method not support')

    id = request.GET['id']

    # get order
    order = models.TradeOrder.objects.get(id=id)
    if not order:
        return resp.failure(hint.ERR_FORM_DATA)

    nstatus = [order.status]
    # get next status
    nstatus.extend(state.order.sys.get(order.status, []))

    options = []
    # next status options
    for s in nstatus:
        txt = enum.all['order']['status'].get(s)
        options.append({'id': s, 'text': txt})

    # response next status options
    return resp.success(data=options)