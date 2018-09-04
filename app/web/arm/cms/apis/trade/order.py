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
        form = forms.trade.order.List(request.GET)
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
    form = forms.trade.order.Add(request.POST)
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
                                ptype=params['ptype'],
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
    form = forms.trade.order.Update(request.POST)
    if form.is_valid():
        # get parameters
        params = form.cleaned_data
        id, ocode, dcount, dprice, dtime, status = params['id'], params['ocode'], params['dcount'], params['dprice'], params['dtime'], params['status']

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
        order.ocode, order.dcount, order.dprice, order.dtime, order.status, order.slog = ocode, dcount, dprice, dtime.timestamp(), status, json.dumps(logs)
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
    form = forms.trade.order.Delete(request.POST)
    if form.is_valid():
        id = form.cleaned_data['id']
        models.TradeOrder.objects.filter(id=id).delete()
        return resp.success()
    else:
        return resp.failure(str(form.errors))


@auth.catch_exception
@auth.need_login
def trade(request):
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

    # get trade object
    trade = item.trade

    rows = []
    # make results
    rows.append({'name': '订单ID', 'value': trade.id, 'group': '交易信息'})
    rows.append({'name': '订单编号', 'value': trade.code, 'group': '交易信息'})
    rows.append({'name': '订单类型', 'value': enum.all['order']['price'][trade.ptype] if trade.ptype else '', 'group': '交易信息'})
    rows.append({'name': '订单价格', 'value': trade.oprice, 'group': '交易信息'})
    rows.append({'name': '订单股数', 'value': trade.ocount, 'group': '交易信息'})
    rows.append({'name': '持仓价格', 'value': trade.hprice, 'group': '交易信息'})
    rows.append({'name': '持仓数量', 'value': trade.hcount, 'group': '交易信息'})
    rows.append({'name': '订单状态', 'value': enum.all['trade']['status'][trade.status] if trade.status else '', 'group': '交易信息'})

    rows.append({'name': '保证金', 'value': trade.margin, 'group': '费用信息'})
    rows.append({'name': '服务费', 'value': trade.ofee, 'group': '费用信息'})
    rows.append({'name': '延期天数', 'value': trade.ddays, 'group': '费用信息'})
    rows.append({'name': '延期费', 'value': trade.dfee, 'group': '费用信息'})
    rows.append({'name': '订单盈利', 'value': trade.tprofit, 'group': '费用信息'})
    rows.append({'name': '盈利分成', 'value': trade.sprofit, 'group': '费用信息'})

    rows.append({'name': '用户ID', 'value': trade.user.id, 'group': '用户信息'})
    rows.append({'name': '用户手机', 'value': trade.user.user, 'group': '用户信息'})
    rows.append({'name': '账户余额', 'value': trade.user.money, 'group': '用户信息'})
    rows.append({'name': '禁用标识', 'value': enum.all['common']['disable'][trade.user.disable], 'group': '用户信息'})

    rows.append({'name': '交易账号', 'value': trade.account.account if trade.account else '', 'group': '交易账户'})
    rows.append({'name': '账户名称', 'value': trade.account.name if trade.account else '', 'group': '交易账户'})
    rows.append({'name': '可用余额', 'value': trade.account.lmoney if trade.account else '', 'group': '交易账户'})
    rows.append({'name': '保底佣金', 'value': trade.account.cfmin if trade.account else '', 'group': '交易账户'})
    rows.append({'name': '佣金费率', 'value': trade.account.cfrate if trade.account else '', 'group': '交易账户'})
    rows.append({'name': '印花税率', 'value': trade.account.tfrate if trade.account else '', 'group': '交易账户'})
    rows.append({'name': '禁用标识', 'value': enum.all['common']['disable'][trade.account.disable] if trade.account else '', 'group': '交易账户'})

    ## response data ##
    data = {
        'total': len(rows),
        'rows': rows
    }

    return resp.success(data=data)


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
    rows = []
    if item.slog:
        rows = json.loads(item.slog)

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