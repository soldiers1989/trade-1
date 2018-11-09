"""
    api for cms
"""
import time, datetime, json, util
from django.db import transaction
from django.db.models import Q
from adb import models
from cms import auth, resp, hint, forms, error


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
    orderby = None
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


@auth.need_login
def add(request):
    """
        add api
    :param request:
    :return:
    """
    try:
        form = forms.user.trade.Add(request.POST)
        if form.is_valid():
            # clean form data
            params = form.cleaned_data

            with transaction.atomic():
                # get params
                userid, leverid, stockid, couponid = params['user'], params['lever'], params['stock'], params['coupon']

                # get user/lever/stock/coupon
                user = models.User.objects.get(id=userid)
                lever = models.Lever.objects.get(id=leverid)
                stock = models.Stock.objects.get(id=stockid)
                usercoupon = models.UserCoupon.objects.get(id=couponid) if couponid else None

                # compute margin


                # get user


                # take margin


                # add trade
                trade = models.UserTrade(user_id = params['user'],
                                        stock_id = params['stock'],
                                        coupon_id = params['coupon'],
                                        tcode = util.rand.uuid(),
                                        optype = 'xj',
                                        oprice = 0.0 if params['oprice'] is None else params['oprice'],
                                        ocount = params['ocount'],
                                        hprice = 0.0,
                                        hcount = 0,
                                        fcount = 0,
                                        bprice = 0.0,
                                        bcount = 0,
                                        sprice = 0.0,
                                        scount = 0,
                                        margin = 0.0,
                                        ofee = 0.0,
                                        dday = 0,
                                        dfee = 0.0,
                                        tprofit = 0.0,
                                        sprofit = 0.0,
                                        status = 'tobuy',
                                        ctime=int(time.time()),
                                        mtime=int(time.time()))
                trade.save()

                # add lever
                tradelever = models.TradeLever(trade_id = trade.id,
                                               lever = lever.lever,
                                               wline = lever.wline,
                                               sline = lever.sline,
                                               ofmin = lever.ofmin,
                                               ofrate = lever.ofrate,
                                               dfrate = lever.dfrate,
                                               psrate = lever.psrate,
                                               mmin = lever.mmin,
                                               mmax = lever.mmax)
                tradelever.save()

                # add trade order
                tradeorder = models.TradeOrder(tcode = trade.tcode,
                                               account = '10000001',
                                               scode = '000001',
                                               sname = '中国平安',
                                               otype = 'buy',
                                               optype = params['optype'],
                                               ocount = params['ocount'],
                                               oprice = trade.oprice,
                                               odate = '2018-10-02',
                                               otime = int(time.time()),
                                               dprice = 0.0,
                                               dcount = 0,
                                               status = 'notsend',
                                               ctime = int(time.time()),
                                               mtime = int(time.time()))
                tradeorder.save()

            return resp.success()
        else:
            return resp.failure(hint.ERR_FORM_DATA, data={'errors':form.errors})
    except Exception as e:
        return resp.failure(str(e))


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
def deal(request):
    """
        process user trade order
    :param request:
    :return:
    """
    form = forms.user.trade.Deal(request.POST)
    if form.is_valid():
        # trade id
        tradeid, action = form.cleaned_data['id'], form.cleaned_data['act']

        # process user trade order #

        # get new record data #
        obj = models.UserTrade.objects.get(id=tradeid)

        ## response data ##
        data = obj.ddata()

        return resp.success(data=data)
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