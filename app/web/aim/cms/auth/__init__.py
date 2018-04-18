
def check(func):
    def _check_auth(request):

        return func(request)

    return _check_auth


def set(request):
    """

    :param request:
    :return:
    """
    pass


def get(request):
    """

    :param request:
    :return:
    """
