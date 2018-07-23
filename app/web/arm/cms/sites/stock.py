from cms import auth

from django.shortcuts import render


@auth.need_permit
def stock(request):
    """

    :param request:
    :return:
    """
    return render(request, 'stock/stock.html')
