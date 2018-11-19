import time
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
    form = forms.sys.crond.Delete(request.POST)
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
    form = forms.sys.crond.Enable(request.POST)
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
    form = forms.sys.crond.Disable(request.POST)
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
    form = forms.sys.crond.Execute(request.POST)
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

        rows, newrows = data['rows'], []
        rows.sort(key=lambda x: x['seq'], reverse=True)
        names = {'status':'执行状态', 'estime':'开始时间', 'eetime':'结束时间', 'eresult':'执行结果'}
        # convert data
        for row in rows:
            group = '执行序号-'+str(row['seq'])
            for k, v in row.items():
                if names.get(k) is not None:
                    v = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(v)) if 'time' in k else v
                    newrows.append({'name':names[k], 'value':str(v), 'group':group})

        data = {
            'total': len(newrows),
            'rows': newrows
        }

        # response data
        return resp.success(data = data)