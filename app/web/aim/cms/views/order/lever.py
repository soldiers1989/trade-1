from cms import ctx, auth

from django.shortcuts import render


@auth.protect
def list(request):
    """
        module list view
    :param request:
    :return:
    """
    return render(request, 'order/lever/list.html', context=ctx.default(request, 'cms.order.lever.list'))
