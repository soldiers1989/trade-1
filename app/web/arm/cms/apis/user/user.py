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

@auth.need_permit
def add(request):
    """
        add api
    :param request:
    :return:
    """
    try:
        if request.method != 'POST':
            return resp.failure(message='method not support')

        form = forms.order.lever.Lever(request.POST)
        if form.is_valid():
            item = models.Lever(lever=form.cleaned_data['lever'],
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
                                 ctime=int(time.time()),
                                 mtime=int(time.time()));
            item.save()
            return resp.success(data=item.dict())
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
