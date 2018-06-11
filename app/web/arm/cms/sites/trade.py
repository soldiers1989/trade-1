from cms import auth

from django.shortcuts import render


@auth.need_permit
def lever(request):
    """

    :param request:
    :return:
    """
    return render(request, 'trade/lever.html')


@auth.need_permit
def order(request):
    """

    :param request:
    :return:
    """
    return render(request, 'trade/order.html')