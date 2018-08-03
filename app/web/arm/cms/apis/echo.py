"""
    echo
"""
from cms import auth, resp

@auth.need_permit
def echo(request):
    return resp.success(data='echo')