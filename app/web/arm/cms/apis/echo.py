"""
    echo
"""
from cms import auth, resp


@auth.catch_exception
def echo(request):
    return resp.success(data='echo')