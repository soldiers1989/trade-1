import time, util
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
        form = forms.user.charge.List(request.POST)
        if form.is_valid():
            ## form parameters ##
            params = form.cleaned_data

            status = params['status']
            ## filters ##
            filters = {}
            if status:
                filters['status'] = status

            ## search words ##
            words = params['words']
            if words:
                if words.isdigit():
                    if len(words) < 10:
                        filters['id'] = words
                    else:
                        filters['user__user'] = words
                else:
                    filters['code'] = words

            ## get total count ##
            total = models.UserCharge.objects.filter(**filters).count()


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
                    objects = models.UserCharge.objects.filter(**filters).order_by(orderby)[start:end]
                else:
                    objects = models.UserCharge.objects.filter(**filters).order_by(orderby)
            else:
                if start is not None and end is not None:
                    objects = models.UserCharge.objects.filter(**filters)[start:end]
                else:
                    objects = models.UserCharge.objects.filter(**filters)

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
    form = forms.user.charge.Add(request.POST)
    if form.is_valid():
        params = form.cleaned_data

        # check if user has exist
        items = models.User.objects.filter(id=params['user'])
        if not items.exists():
            return resp.failure(hint.ERR_FORM_DATA)

        item = models.UserCharge(code=util.rand.uuid(),
                            money=params['money'],
                            status=params['status'],
                            ctime=int(time.time()),
                            user_id=params['user'])
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
    form = forms.user.charge.Update(request.POST)
    if form.is_valid():
        params = form.cleaned_data

        models.UserCharge.objects.filter(id=params['id']).update(money=params['money'],
                                                                status=params['status'],
                                                                ctime=int(time.time()))
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
    form = forms.user.charge.Delete(request.POST)
    if form.is_valid():
        id = form.cleaned_data['id']
        models.UserCharge.objects.filter(id=id).delete()
        return resp.success()
    else:
        return resp.failure(str(form.errors))
