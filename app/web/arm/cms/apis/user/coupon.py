import cube, datetime
from django.db.models import Q
from adb import models
from cms import auth, resp, hint, forms


@auth.need_login
def list(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        form = forms.user.coupon.List(request.POST)
        if form.is_valid():
            ## form parameters ##
            params = form.cleaned_data

            status, sdate, edate = params['status'], params['sdate'], params['edate']
            ## filters ##
            filters = {}
            if status:
                filters['status'] = status
            if sdate:
                filters['ctime__gte'] = cube.util.time.utime(sdate)
            if edate:
                filters['ctime__lt'] = cube.util.time.utime(edate+datetime.timedelta(days=1))

            ## search words ##
            user = params['user']
            if user:
                filters['user__id'] = user

            ## get total count ##
            total = models.UserCoupon.objects.filter(**filters).count()


            # order by#
            sort, order =  params['sort'], params['order']
            orderby = None
            if sort and order:
                order = '-' if order=='desc' else ''
                orderby = order+sort

            ## pagination##
            page, size, start, end = params['page'], params['rows'], None, None
            if page and size:
                start, end = (page-1)*size, page*size

            ## query results ##
            objects = []
            if orderby:
                if start is not None and end is not None:
                    objects = models.UserCoupon.objects.filter(**filters).order_by(orderby)[start:end]
                else:
                    objects = models.UserCoupon.objects.filter(**filters).order_by(orderby)
            else:
                if start is not None and end is not None:
                    objects = models.UserCoupon.objects.filter(**filters)[start:end]
                else:
                    objects = models.UserCoupon.objects.filter(**filters)

            ## make results ##
            rows = []
            for obj in objects:
                obj = obj.dict()
                del obj['user']
                rows.append(obj)

            ## response data ##
            data = {
                'total': total,
                'rows': rows
            }

            return resp.success(data=data)
        else:
            return resp.failure(hint.ERR_FORM_DATA)
    except Exception as e:
        return resp.failure(str(e))
