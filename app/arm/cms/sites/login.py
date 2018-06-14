from django.shortcuts import render


def login(request):
    """
        administrator index page
    :param request:
    :return:
    """
    return render(request, 'login.html')

