from django.shortcuts import render

from django.db.models import Q

from adb import models
from cms import auth


@auth.need_login
def index(request):
    """
        index
    """
    return render(request, 'index.html')
