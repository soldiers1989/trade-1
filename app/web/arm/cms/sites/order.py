from cms import auth

from django.shortcuts import render


@auth.need_permit
def lever(request):
    """

    :param request:
    :return:
    """
    return render(request, 'order/lever.html')



