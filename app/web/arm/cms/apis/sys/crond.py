from cms import auth, resp, forms, remote


@auth.catch_exception
@auth.need_login
def list(request):
    """
        list api
    :param request:
    :return:
    """
    form = forms.sys.crond.List(request.GET)
    if form.is_valid():
        # get params
        params = form.cleaned_data

        # request rpc
        data = remote.crond.list(**params)

        # response data
        return resp.success(data = data)


@auth.catch_exception
@auth.need_login
def load(request):
    """
        clear
    :param request:
    :return:
    """
    # request rpc
    data = remote.crond.load()

    # response data
    return resp.success(data=data)


@auth.catch_exception
@auth.need_login
def get(request):
    """
        get
    :param request:
    :return:
    """
    form = forms.sys.crond.Get(request.GET)
    if form.is_valid():
        # get params
        params = form.cleaned_data

        # request rpc
        data = remote.crond.status(**params)

        # response data
        return resp.success(data = data)


@auth.catch_exception
@auth.need_login
def add(request):
    """
        add
    :param request:
    :return:
    """
    form = forms.sys.crond.Add(request.POST)
    if form.is_valid():
        # get params
        params = form.cleaned_data

        # request rpc
        data = remote.crond.add(**params)

        # response data
        return resp.success(data = data)


@auth.catch_exception
@auth.need_login
def delete(request):
    """
        delete
    :param request:
    :return:
    """
    form = forms.sys.crond.Delete(request.GET)
    if form.is_valid():
        # get params
        params = form.cleaned_data

        # request rpc
        data = remote.crond.delete(**params)

        # response data
        return resp.success(data = data)


@auth.catch_exception
@auth.need_login
def clear(request):
    """
        clear
    :param request:
    :return:
    """
    # request rpc
    data = remote.crond.clear()

    # response data
    return resp.success(data=data)


@auth.catch_exception
@auth.need_login
def enable(request):
    """
        enable
    :param request:
    :return:
    """
    form = forms.sys.crond.Enable(request.GET)
    if form.is_valid():
        # get params
        params = form.cleaned_data

        # request rpc
        data = remote.crond.enable(**params)

        # response data
        return resp.success(data = data)


@auth.catch_exception
@auth.need_login
def disable(request):
    """
        disable
    :param request:
    :return:
    """
    form = forms.sys.crond.Disable(request.GET)
    if form.is_valid():
        # get params
        params = form.cleaned_data

        # request rpc
        data = remote.crond.disable(**params)

        # response data
        return resp.success(data=data)


@auth.catch_exception
@auth.need_login
def execute(request):
    """
        enable
    :param request:
    :return:
    """
    form = forms.sys.crond.Execute(request.GET)
    if form.is_valid():
        # get params
        params = form.cleaned_data

        # request rpc
        data = remote.crond.execute(**params)

        # response data
        return resp.success(data = data)


@auth.catch_exception
@auth.need_login
def detail(request):
    """
        get
    :param request:
    :return:
    """
    form = forms.sys.crond.Detail(request.GET)
    if form.is_valid():
        # get params
        params = form.cleaned_data

        # request rpc
        data = remote.crond.detail(**params)

        # response data
        return resp.success(data = data)