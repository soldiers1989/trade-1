"""
    api for cms
"""
import cube, time, datetime
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
        form = forms.user.user.List(request.POST)
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
                    q = Q(user=words) | Q(phone=words)

            ## get total count ##
            total = models.User.objects.filter(q, **filters).count()


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
                    objects = models.User.objects.filter(q, **filters).order_by(orderby)[start:end]
                else:
                    objects = models.User.objects.filter(q, **filters).order_by(orderby)
            else:
                if start is not None and end is not None:
                    objects = models.User.objects.filter(q, **filters)[start:end]
                else:
                    objects = models.User.objects.filter(q, **filters)

            ## make results ##
            rows = []
            for obj in objects:
                row = obj.dict()

                try:
                    row['userstat__tpay'], row['userstat__tdraw'], row['userstat__ttradec'], row['userstat__ttradem'] = obj.userstat.tpay, obj.userstat.tdraw, obj.userstat.ttradec, obj.userstat.ttradem
                except:
                    row['userstat__tpay'], row['userstat__tdraw'], row['userstat__ttradec'], row['userstat__ttradem'] = None, None, None, None

                rows.append(row)

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
def query(request):
    """
        query api
    :param request:
    :return:
    """
    try:
        form = forms.user.user.Query(request.POST)
        if form.is_valid():
            ## form parameters ##
            words = form.cleaned_data['q']

            ## response data ##
            data = []

            ##
            if len(words) > 3:
                objects = models.User.objects.filter(user__startswith=words, disable=False)
                for obj in objects:
                    data.append({'id': obj.id, 'user': obj.user})

            return resp.success(data=data)
        else:
            return resp.failure(form.errors)
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def has(request):
    """

    :param request:
    :return:
    """
    try:
        form = forms.user.user.Has(request.POST)
        if form.is_valid():
            # get user
            user = form.cleaned_data['user']

            # get order detail
            items = models.User.objects.filter(user=user)
            if(items.exists()):
                return resp.text('true')
            else:
                return resp.text('false')
        else:
            return resp.failure(form.errors)
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def stat(request):
    """
    :param request:
    :return:
    """
    try:
        form = forms.user.user.Get(request.POST)
        if form.is_valid():
            # user id
            userid = form.cleaned_data['id']

            # get record
            object = models.UserStat(user_id=userid)
            try:
                object = models.UserStat.objects.get(user__id=userid)
            except:
                pass

            ## make results ##
            rows = object.properties()

            ## response data ##
            data = {
                'total': len(rows),
                'rows': rows
            }

            return resp.success(data=data)
        else:
            return resp.failure(form.errors, [])
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def banks(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        form = forms.user.user.Get(request.POST)
        if form.is_valid():
            # user id
            userid = form.cleaned_data['id']

            # get fee records of order
            objects = models.UserBank.objects.filter(user__id=userid)

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
def trades(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        form = forms.user.user.Get(request.POST)
        if form.is_valid():
            # user id
            userid = form.cleaned_data['id']

            # get fee records of order
            objects = models.UserTrade.objects.filter(user__id=userid)

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
def bills(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        form = forms.user.user.Get(request.POST)
        if form.is_valid():
            # user id
            userid = form.cleaned_data['id']

            # get fee records of order
            objects = models.UserBill.objects.filter(user__id=userid)

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
def coupons(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        form = forms.user.user.Get(request.POST)
        if form.is_valid():
            # user id
            userid = form.cleaned_data['id']

            # get fee records of order
            objects = models.UserCoupon.objects.filter(user__id=userid)

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
def stocks(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        form = forms.user.user.Get(request.POST)
        if form.is_valid():
            # user id
            userid = form.cleaned_data['id']

            # get fee records of order
            objects = models.UserStock.objects.filter(user__id=userid)

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
def charges(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        form = forms.user.user.Get(request.POST)
        if form.is_valid():
            # user id
            userid = form.cleaned_data['id']

            # get fee records of order
            objects = models.UserCharge.objects.filter(user__id=userid)

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
def draws(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        form = forms.user.user.Get(request.POST)
        if form.is_valid():
            # user id
            userid = form.cleaned_data['id']

            # get fee records of order
            objects = models.UserDraw.objects.filter(user__id=userid)

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