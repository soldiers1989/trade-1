from cms import ctx, auth

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
        return render(request, 'order/order/detail.html', context=ctx.default(request, '*.order.order.*'))
    except Exception as e:
        return str(e)
