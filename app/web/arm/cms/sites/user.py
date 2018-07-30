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
def coupon(request):
    """

    :param request:
    :return:
    """
    return render(request, 'user/coupon.html')
