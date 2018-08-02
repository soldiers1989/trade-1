"""
    api for cms
"""
import time, datetime, util
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
                filters['ctime__gte'] = util.time.utime(sdate)
            if edate:
                filters['ctime__lt'] = util.time.utime(edate+datetime.timedelta(days=1))

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
            return resp.failure(msg='method not support')

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


                # get user



                # take margin


                # add trade
                trade = models.UserTrade(user_id = params['user'],
                                        stock_id = params['stock'],
                                        coupon_id = params['coupon'],
                                        code = util.rand.uuid(),
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


@auth.need_login
def lever(request):
    try:
        form = forms.trade.order.Get(request.POST)
        if form.is_valid():
            # trade id
            tradeid = form.cleaned_data['id']

            # get fee records of order
            object = models.TradeLever.objects.get(trade__id=tradeid)

            ## make results ##
            rows = []

            rows.append({'name':'杠杆', 'value':object.lever})
            rows.append({'name':'预警线', 'value':object.wline})
            rows.append({'name':'止损线', 'value':object.sline})
            rows.append({'name':'保底费用', 'value':object.ofmin})
            rows.append({'name':'建仓费率', 'value':object.ofrate})
            rows.append({'name': '延期费率', 'value': object.dfrate})
            rows.append({'name': '盈利分成', 'value': object.psrate})
            rows.append({'name': '本金下限', 'value': object.mmin})
            rows.append({'name': '本金上线限', 'value': object.mmax})

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
        form = forms.trade.order.Get(request.POST)
        if form.is_valid():
            # trade id
            tradeid = form.cleaned_data['id']

            # get fee records of order
            objects = models.TradeFee.objects.filter(trade__id=tradeid)

            ## get total count ##
            total = objects.count()

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
        form = forms.trade.order.Get(request.POST)
        if form.is_valid():
            # trade id
            tradeid = form.cleaned_data['id']

            # get margin records of order
            objects = models.TradeMargin.objects.filter(trade__id=tradeid)

            ## get total count ##
            total = objects.count()

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
        form = forms.trade.order.Get(request.POST)
        if form.is_valid():
            # trade id
            tradeid = form.cleaned_data['id']

            # get margin records of order
            objects = models.TradeOrder.objects.filter(trade__id=tradeid)

            ## get total count ##
            total = objects.count()

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
            return resp.failure(str(form.errors))
    except Exception as e:
        return resp.failure(str(e))