from cms import ctx, auth, models

from django.shortcuts import render


@auth.protect
def mgmt(request):
    """
        module list view
    :param request:
    :return:
    """
    return render(request, 'order/order/mgmt.html', context=ctx.default(request, 'cms.order.order.mgmt'))


@auth.protect
def detail(request):
    """
        detail api
    :param request:
    :return:
    """
    try:
        if request.method != 'GET':
            return 'method not support'

        id = request.GET['id']

        # get order detail
        item = models.UserTrade.objects.get(id=id)

        # set context
        context = ctx.default(request)
        context.update({'item': item})
        return render(request, 'order/order/detail.html', context=context)
    except Exception as e:
        return str(e)
