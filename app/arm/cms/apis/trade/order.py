"""
    api for cms
"""
import cube, time, datetime
from django.db import transaction
from django.db.models import Q
from adb import models
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

            status, sdate, edate = params['status'], params['sdate'], params['edate']
            ## filters ##
            filters = {}
            if status:
                filters['status'] = status
            if sdate:
                filters['ctime__gte'] = cube.util.time.utime(sdate)
            if edate:
                filters['ctime__lt'] = cube.util.time.utime(edate+datetime.timedelta(days=1))

            ## search words ##
            q = Q()
            words = params['words']
            if words:
                if len(filters) == 0 and len(words) < 10 and words.isdigit():
                    filters['id'] = int(words) # id, not phone number
                else :
                    q = Q(user__user=words) | Q(stock__id=words) | Q(stock__name__contains=words)

            ## get total count ##
            total = models.UserTrade.objects.filter(q, **filters).count()


            # order by#
            sort, order =  params['sort'], params['order']
            orderby = None
            if sort and order:
                order = '-' if order=='desc' else ''
                orderby = order+sort

            ## pagination##
            page, size, start, end = params['page'], params['rows'], None, None
            if page and size:
                start, end = (page-1)*size, page*size

            ## query results ##
            objects = []
            if orderby:
                if start is not None and end is not None:
                    objects = models.UserTrade.objects.filter(q, **filters).order_by(orderby)[start:end]
                else:
                    objects = models.UserTrade.objects.filter(q, **filters).order_by(orderby)
            else:
                if start is not None and end is not None:
                    objects = models.UserTrade.objects.filter(q, **filters)[start:end]
                else:
                    objects = models.UserTrade.objects.filter(q, **filters)

            ## make results ##
            rows = []
            for obj in objects:
                rows.append(obj.dict())

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
def get(request):
    """
        get order
    :param request:
    :return:
    """
    try:
        if request.method != 'GET':
            return resp.failure(message='method not support')

        id = request.GET['id']

        # get order detail
        item = models.UserTrade.objects.get(id=id)

        return resp.success(data=item.dict())
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def add(request):
    """
        add api
    :param request:
    :return:
    """
    try:
        form = forms.trade.order.Add(request.POST)
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


                # take margin


                # add trade
                trade = models.UserTrade(user_id = params['user'],
                                        stock_id = params['stock'],
                                        coupon_id = params['coupon'],
                                        code = cube.util.rand.uuid(),
                                        oprice = params['oprice'],
                                        ocount = params['ocount'],
                                        ctime=int(time.time()));
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
                                               mmax = lever.mmax);
                tradelever.save()

                # add trade order
                tradeorder = models.TradeOrder(trade_id = trade.id,
                                               otype = params['otype'],
                                               ptype = params['ptype'],
                                               ocount = params['ocount'],
                                               oprice = params['oprice'],
                                               otime = int(time.time()),
                                               status = 'todo')
                tradeorder.save()

            return resp.success()
        else:
            return resp.failure(hint.ERR_FORM_DATA, data={'errors':form.errors})
    except Exception as e:
        return resp.failure(str(e))


@auth.need_permit
def modify(request):
    """
        modify api
    :param request:
    :return:
    """
    try:
        if request.method != 'POST':
            return resp.failure(message='method not support')

        form = forms.order.lever.Lever(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            models.Lever.objects.filter(id=id).update(lever=form.cleaned_data['lever'],
                                                     wline=form.cleaned_data['wline'],
                                                     sline=form.cleaned_data['sline'],
                                                     ofmin=form.cleaned_data['ofmin'],
                                                     ofrate=form.cleaned_data['ofrate'],
                                                     dfrate=form.cleaned_data['dfrate'],
                                                     psrate=form.cleaned_data['psrate'],
                                                     mmin=form.cleaned_data['mmin'],
                                                     mmax=form.cleaned_data['mmax'],
                                                     order=form.cleaned_data['order'],
                                                     disable=form.cleaned_data['disable'],
                                                     mtime=int(time.time()));
            item = models.Lever.objects.get(id=id)
            return resp.success(data=item.dict())
        else:
            return resp.failure(hint.ERR_FORM_DATA, data={'errors': form.errors})
    except Exception as e:
        return resp.failure(str(e))


@auth.need_permit
def delete(request):
    """
        delete api
    :param request:
    :return:
    """
    try:
        if request.method != 'POST':
            return resp.failure(message='method not support')

        id = request.POST['id']
        models.Lever.objects.filter(id=id).delete()
        return resp.success()
    except Exception as e:
        return resp.failure(str(e))


@auth.need_permit
def reorder(request):
    """
        order api
    :param request:
    :return:
    """
    try:
        if request.method != 'POST':
            return resp.failure(message='method not support')

        ids = request.POST.getlist('id')
        ords = request.POST.getlist('ord')

        if len(ids) != len(ords):
            return resp.failure(hint.ERR_FORM_DATA)

        iords = []
        for i in range(0, len(ids)):
            iords.append([ids[i], ords[i]])

        for id, ord in iords:
            models.Lever.objects.filter(id=id).update(order=ord)

        return resp.success(data={'iords': iords})
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def orderfees(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        # get order id
        id = request.GET['id']

        # get margin records of order
        items = models.TradeFee.objects.filter(trade__id=id)

        data = []
        for item in items:
            d = item.dict()
            data.append(d)
        return resp.success(data=data)
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def ordermargins(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        # get order id
        id = request.GET['id']

        # get margin records of order
        items = models.TradeMargin.objects.filter(trade__id=id)

        data = []
        for item in items:
            d = item.dict()
            data.append(d)
        return resp.success(data=data)
    except Exception as e:
        return resp.failure(str(e))
