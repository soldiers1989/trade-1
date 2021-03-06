from cms import auth

from django.shortcuts import render


@auth.need_permit
def user(request):
    """

    :param request:
    :return:
    """
    return render(request, 'user/user.html')


@auth.need_permit
def trade(request):
    """

    :param request:
    :return:
    """
    return render(request, 'user/trade.html')


@auth.need_permit
def coupon(request):
    """

    :param request:
    :return:
    """
    return render(request, 'user/coupon.html')


@auth.need_permit
def bill(request):
    """

    :param request:
    :return:
    """
    return render(request, 'user/bill.html')


@auth.need_permit
def charge(request):
    """

    :param request:
    :return:
    """
    return render(request, 'user/charge.html')


@auth.need_permit
def draw(request):
    """

    :param request:
    :return:
    """
    return render(request, 'user/draw.html')


@auth.need_permit
def order(request):
    """

    :param request:
    :return:
    """
    return render(request, 'user/order.html')
