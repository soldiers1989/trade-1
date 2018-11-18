from cms import auth

from django.shortcuts import render


@auth.need_permit
def crond(request):
    """

    :param request:
    :return:
    """
    return render(request, 'sys/crond.html')
