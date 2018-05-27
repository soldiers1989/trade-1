from cms import ctx, auth, models

from django.shortcuts import render


@auth.protect
def list(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        return render(request, 'order/order/list.html', context=ctx.default(request, '*.order.order.*'))
    except Exception as e:
        return str(e)


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
