import cube
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
        order = models.UserTrade.objects.get(id=id)
        order.ctime = cube.time.datetms(order.ctime)
        order.ftime = cube.time.datetms(order.ftime)
        order.status = models.UserTrade.cstatus(order.status)
        order.user.ctime = cube.time.datetms(order.user.ctime)
        order.user.ltime = cube.time.datetms(order.user.ltime)

        # get margins of order
        margins = models.TradeMargin.objects.filter(trade__id=id)
        for margin in margins:
            margin.ctime = cube.time.datetms(margin.ctime)

        # get fees of order
        fees = models.TradeFee.objects.filter(trade__id=id)
        for fee in fees:
            fee.ctime = cube.time.datetms(fee.ctime)

        # set context
        context = ctx.default(request)
        context.update({'order': order, 'margins': margins, 'fees': fees})
        return render(request, 'order/order/detail.html', context=context)
    except Exception as e:
        return str(e)
