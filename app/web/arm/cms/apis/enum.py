"""
    enum data api
"""
from cms import auth, resp, enum, hint, forms


@auth.catch_exception
@auth.need_login
def list(request):
    form = forms.enum.List(request.GET)
    if not form.is_valid():
        return resp.failure(hint.ERR_FORM_DATA)

    # get parameters
    params = form.cleaned_data
    c, i = params['c'], params['i']

    options = []
    # get item data
    items = enum.all[c][i]
    for k, v in items.items():
        options.append({'id':k, 'text':v})

    return resp.success(data=options)
