from cms import ctx, auth

from django.shortcuts import render


@auth.need_permit
def list(request):
    """
        module list view
    :param request:
    :return:
    """
    return render(request, 'auth/auth/list.html', context=ctx.default(request, 'cms.auth.auth.list'))