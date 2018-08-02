"""
    api for cms
"""
import time
from django.db.models import F
from adb import models
from cms import auth, resp, forms


@auth.need_login
def list(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        form = forms.trade.lever.List(request.POST)
        if form.is_valid():
            roles = None

            disable = form.cleaned_data['disable']
            if form.data.get('disable'):
                roles = models.Lever.objects.filter(disable=disable).order_by('order')
            else:
                roles = models.Lever.objects.all().order_by('order')

            rows = []
            for role in roles:
                rows.append(role.dict())

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
def get(request):
    """
        get api
    :param request:
    :return:
    """
    try:
        form = forms.trade.lever.Get(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            item = models.Lever.objects.get(id=id)
            return resp.success(data=item.dict())
        else:
            return resp.failure(str(form.errors))
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
        form = forms.trade.lever.Add(request.POST)
        if form.is_valid():
            params = form.cleaned_data

            order = models.Module.objects.count() + 1

            item = models.Lever(lever=params['lever'],
                                 wline=params['wline'],
                                 sline=params['sline'],
                                 ofmin=params['ofmin'],
                                 ofrate=params['ofrate'],
                                 dfrate=params['dfrate'],
                                 psrate=params['psrate'],
                                 mmin=params['mmin'],
                                 mmax=params['mmax'],
                                 order=order,
                                 disable=params['disable'],
                                 ctime=int(time.time()),
                                 mtime=int(time.time()));
            item.save()
            return resp.success(data=item.dict())
        else:
            return resp.failure(str(form.errors))
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def update(request):
    """
        modify api
    :param request:
    :return:
    """
    try:
        form = forms.trade.lever.Update(request.POST)
        if form.is_valid():
            params = form.cleaned_data
            models.Lever.objects.filter(id=params['id']).update(lever=params['lever'],
                                                     wline=params['wline'],
                                                     sline=params['sline'],
                                                     ofmin=params['ofmin'],
                                                     ofrate=params['ofrate'],
                                                     dfrate=params['dfrate'],
                                                     psrate=params['psrate'],
                                                     mmin=params['mmin'],
                                                     mmax=params['mmax'],
                                                     disable=params['disable'],
                                                     mtime=int(time.time()));
            return resp.success()
        else:
            return resp.failure(str(form.errors))
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
        form = forms.trade.lever.Delete(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            models.Lever.objects.filter(id=id).delete()
            return resp.success()
        else:
            return resp.failure(str(form.errors))
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def reorder(request):
    """
        order api
    :param request:
    :return:
    """
    try:
        form = forms.trade.lever.Order(request.POST)
        if form.is_valid():
            sid, sorder = form.cleaned_data['sid'], form.cleaned_data['sorder']
            tid, torder = form.cleaned_data['tid'], form.cleaned_data['torder']

            if sorder > torder:
                #update region order
                models.Lever.objects.filter(order__gte=torder, order__lte=sorder).update(order=F('order')+1)

                #update source order
                models.Lever.objects.filter(id=sid).update(order=torder)
            else:
                #update region order
                models.Lever.objects.filter(order__gte=sorder, order__lte=torder).update(order=F('order')-1)

                #update source order
                models.Lever.objects.filter(id=sid).update(order=torder)

            return resp.success()
        else:
            return resp.failure(str(form.errors))
    except Exception as e:
        return resp.failure(str(e))
