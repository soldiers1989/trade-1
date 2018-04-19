"""
     authority control
"""
from pub import models


def do_login(username, password, remember):
    """
        administrator login
    :param username:
    :param password:
    :param remember:
    :return:
    """
    try:
        admin = models.Admin.objects.get(user=username)
        if admin.pwd == password:
            return True

        return False
    except:
        pass



def has_login(request):
    """
        check login status
    :param request:
    :return:
    """
    return False


def has_auth(func):
    """

    :param request:
    :return:
    """
    def _has_auth(request):
        return func(request)
    return _has_auth


def do_logout(request):
    """
        administrator logout
    :param username:
    :return:
    """
    pass
