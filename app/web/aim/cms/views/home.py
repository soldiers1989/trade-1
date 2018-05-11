from cms import ctx, auth

from django.shortcuts import render


@auth.has_login
def index(request):
    """
        administrator index page
    :param request:
    :return:
    """

    return render(request, 'index.html', context=ctx.default(request, 'cms.index'))
