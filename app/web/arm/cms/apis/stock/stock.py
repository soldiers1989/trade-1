import time
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
        form = forms.stock.stock.List(request.POST)
        if form.is_valid():
            ## form parameters ##
            params = form.cleaned_data

            status, limit = params['status'], params['limit']
            ## filters ##
            filters = {}
            if status:
                filters['status'] = status
            if limit:
                filters['limit'] = limit


            ## search words ##
            q = Q()
            words = params['words']
            if words:
                if len(filters) == 0 and words.isdigit():
                    filters['id'] = words
                else :
                    q = Q(name=words) | Q(jianpin=words) | Q(quanpin=words)

            ## get total count ##
            total = models.Stock.objects.filter(q, **filters).count()


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
                    objects = models.Stock.objects.filter(q, **filters).order_by(orderby)[start:end]
                else:
                    objects = models.Stock.objects.filter(q, **filters).order_by(orderby)
            else:
                if start is not None and end is not None:
                    objects = models.Stock.objects.filter(q, **filters)[start:end]
                else:
                    objects = models.Stock.objects.filter(q, **filters)

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
def add(request):
    """
        add api
    :param request:
    :return:
    """
    try:
        form = forms.stock.stock.Add(request.POST)
        if form.is_valid():
            params = form.cleaned_data

            item = models.Stock(id=params['id'],
                                name=params['name'],
                                jianpin=params['jianpin'],
                                quanpin=params['quanpin'],
                                status=params['status'],
                                limit=params['limit'],
                                ctime=int(time.time()),
                                mtime=int(time.time()))
            item.save()
            return resp.success(data=item.dict())
        else:
            return resp.failure(form.errors)
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def update(request):
    """
        modify admin
    :param request:
    :return:
    """
    try:
        form = forms.stock.stock.Update(request.POST)
        if form.is_valid():
            params = form.cleaned_data

            models.Stock.objects.filter(id=params['id']).update(name=params['name'],
                                                                jianpin=params['jianpin'],
                                                                quanpin=params['quanpin'],
                                                                status=params['status'],
                                                                limit=params['limit'],
                                                                mtime=int(time.time()))
            return resp.success()
        else:
            return resp.failure(form.errors)
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def delete(request):
    """
        delete api
    :param request:
    :return:
    """
    try:
        form = forms.stock.stock.Delete(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            models.Stock.objects.filter(id=id).delete()
            return resp.success()
        else:
            return resp.failure(form.errors)
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
        form = forms.stock.stock.Query(request.POST)
        if form.is_valid():
            ## form parameters ##
            words = form.cleaned_data['q']

            ## response data ##
            data = []

            ##
            if len(words) > 1:
                objects = models.Stock.objects.filter(id__startswith=words, status='open', limit='none')
                for obj in objects:
                    data.append({'id': obj.id, 'name': obj.name})

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
        form = forms.stock.stock.Has(request.POST)
        if form.is_valid():
            # get stock id
            stock = form.cleaned_data['stock']

            # get order detail
            items = models.Stock.objects.filter(id=stock)
            if(items.exists()):
                return resp.text('true')
            else:
                return resp.text('false')
        else:
            return resp.failure(form.errors)
    except Exception as e:
        return resp.failure(str(e))