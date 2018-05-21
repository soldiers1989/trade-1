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
