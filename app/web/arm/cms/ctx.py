from cms import auth, cfg


def default(request, mcode=None):
    """
        get global default context
    :param request:
    :param mcode: module code
    :return:
    """
    # user not login
    if not auth.is_login(request):
        return cfg.default_context

    # get mcode from request
    if mcode is None:
        mcode = request.path.replace('/', '.').strip('.')


    # user has login
    ctx = {
        'userid': auth.user.id(request),
        'username': auth.user.name(request),
        'modules': auth.user.modules(request),
        'actives': auth.user.parents(request, mcode)
    }

    ctx.update(cfg.default_context)

    return ctx
