"""
    api for cms
"""
import time
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
        items = models.Lever.objects.filter().order_by('order')

        data = []

        seq = 0
        for item in items:
            d = item.dict()
            d['seq'] = seq
            data.append(d)
            seq += 1

        return resp.success(data=data)
    except Exception as e:
        return resp.failure(str(e))


@auth.need_permit
def get(request):
    """
        get api
    :param request:
    :return:
    """
    try:
        if request.method != 'GET':
            return resp.failure(message='method not support')

        id = request.GET['id']
        item = models.Lever.objects.get(id=id)

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