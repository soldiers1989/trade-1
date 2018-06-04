"""
    api for cms
"""
import cube, time, datetime

from adb import models

from cms import auth, resp, hint, forms


@auth.need_permit
def list(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        if request.method != 'GET':
            return resp.failure(message='method not support')

        form = forms.order.order.Query(request.GET)
        if form.is_valid():
            # query set
            results = models.UserTrade.objects.all()

            # form parameters
            params = form.cleaned_data

            # filter
            status, sdate, edate, words = params['status'], params['sdate'], params['edate'], params['words']
            if status:
                results = results.filter(status=status)
            if sdate:
                results = results.filter(ctime__gte=cube.time.utime(sdate))
            if edate:
                results = results.filter(ctime__lt=cube.time.utime(edate+datetime.timedelta(days=1)))
            if words:
                results = results.filter(user__user=words) | results.filter(stock__id=words) | results.filter(stock__name__contains=words)

            # order
            orderby, order = params['orderby'], params['order']
            if orderby and order:
                order = '-' if order=='desc' else ''
                results = results.order_by(order+orderby)

            # count
            total = results.count()

            # limit
            start = cube.page.start(params['start'], total)
            count = cube.page.count(params['count'])

            results = results[start:start+count]

            # response
            data = {
                'total': total,
                'start': start,
                'items': [
                ]
            }

            for result in results:
                item = {'id': result.id, 'user': result.user.user, 'stock': result.stock.name,
                        'ocount': result.ocount, 'oprice': result.oprice,
                        'hcount': result.hcount, 'fcount': result.fcount,
                        'bcount': result.bcount, 'bprice': result.bprice,
                        'scount': result.scount, 'sprice': result.sprice,
                        'margin': result.margin, 'ofee': result.ofee,
                        'ddays': result.ddays, 'dfee': result.dfee,
                        'status': models.UserTrade.cstatus(result.status), 'date': cube.time.dates(result.ctime)}
                data['items'].append(item)

            return resp.success(data=data)
        else:
            return resp.failure(hint.ERR_FORM_DATA, data={'errors': form.errors})
    except Exception as e:
        return resp.failure(str(e))


@auth.need_permit
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