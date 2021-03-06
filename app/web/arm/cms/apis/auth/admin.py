"""
    api for cms
"""
import time, util, datetime
from django.db.models import Q
from adb import models
from cms import auth, resp, hint, forms


def login(request):
    """
        login
    :param request:
    :return:
    """
    try:
        login_form = forms.auth.admin.Login(request.POST)
        if login_form.is_valid():
            # get login data form user input
            username = login_form.cleaned_data.get('user')
            password = util.hash.sha1(login_form.cleaned_data.get('pwd'))
            remember = login_form.cleaned_data.get('remember')

            # get admin data from database
            admin = models.Admin.objects.get(user=username)

            # check password
            if admin.pwd == password:
                # user has been disabled
                if admin.disable:
                    return resp.failure(hint.ERR_LOGIN_DISABLED)

                # set session expire for not remember choice
                if not remember:
                    request.session.set_expiry(0)

                # save admin id to session
                auth.set_admin_id(request, admin.id)

                return resp.success(hint.MSG_LOGIN_SUCCESS)
            else:
                return resp.failure(hint.ERR_LOGIN_PASSWORD)
        else:
            return resp.failure(hint.ERR_LOGIN_INPUT)
    except Exception as e:
        return resp.failure(e)


@auth.need_login
def logout(request):
    """
        logout
    :param request:
    :return:
    """
    try:
        request.session.clear()
        return resp.success(hint.MSG_LOGOUT_SUCCESS)
    except Exception as e:
        return resp.failure(e);


@auth.need_login
def pwd(request):
    """
        change password
    :param request:
    :return:
    """
    try:
        form = forms.auth.admin.Pwd(request.POST)
        if form.is_valid():
            # get new password
            pwd = util.hash.sha1(form.cleaned_data['pwd'])
            # get current admin
            id = auth.get_admin_id(request)
            # update password
            models.Admin.objects.filter(id=id).update(pwd=pwd)

            #
            return resp.success(hint.MSG_CHANGEPWD_SUCCESS)
        else:
            return resp.failure(hint.ERR_FORM_DATA)
    except Exception as e:
        return resp.failure(e);


@auth.need_login
def list(request):
    """
        list api
    :param request:
    :return:
    """
    try:
        form = forms.auth.admin.List(request.POST)
        if form.is_valid():
            ## form parameters ##
            params = form.cleaned_data

            ## filters ##
            sdate, edate = params['sdate'], params['edate']
            filters = {}
            if sdate:
                filters['ctime__gte'] = util.time.utime(sdate)
            if edate:
                filters['ctime__lt'] = util.time.utime(edate+datetime.timedelta(days=1))

            q = Q()
            ## search words ##
            words = params['words']
            if words:
                if words.isdigit() and len(filters) == 0:
                   filters['id']=int(words)
                else:
                    q = Q(user__contains=words) | Q(name__contains=words) | Q(phone__contains=words)

            ## get total count ##
            total = models.Admin.objects.filter(q, **filters).count()

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
                    objects = models.Admin.objects.filter(q, **filters).order_by(orderby)[start:end]
                else:
                    objects = models.Admin.objects.filter(q, **filters).order_by(orderby).all()
            else:
                if start is not None and end is not None:
                    objects = models.Admin.objects.filter(q, **filters).all()[start:end]
                else:
                    objects = models.Admin.objects.filter(q, **filters).all()

            s = str(objects.query)

            ## make results ##
            rows = []
            for object in objects:
                item = object.ddata()
                del item['pwd']
                rows.append(item)

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


@auth.need_login
def whoami(request):
    try:
        # get admin id from session
        id = auth.get_admin_id(request);

        # get admin
        admin = models.Admin.objects.get(id=id)

        qs = None
        # get admin roles
        roles = admin.roles.filter(disable=False).all()
        for role in roles:
            if qs is None:
                qs = Q(role__id=role.id)
            else:
                qs = qs | Q(role__id=role.id)

        # get admin's modules
        mobjs = models.Module.objects.filter(qs, disable=False).distinct().order_by('order')

        # get modules of admin
        modules, mtrees = [], []
        # pack modules to session
        if mobjs is not None:
            for mobj in mobjs:
                modules.append(mobj.ddata())
                mtrees.append({
                   'id': mobj.id,
                   'parent': mobj.parent_id,
                   'order': mobj.order,
                   'text': mobj.name,
                   'attributes':{
                       'url': mobj.path,
                   }
               })

        # save admin modules to session
        auth.set_admin_modules(request, modules)

        # make results
        data = {
            'admin': {
                'user': admin.user,
                'name': admin.name,
                'phone': admin.phone
            },
            'modules': util.tree.make(mtrees)
        }

        return resp.success(data=data)

    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def get(request):
    """
        get api
    :param request:
    :return:
    """
    try:
        id = request.POST['id']
        item = models.Admin.objects.get(id=id)
        return resp.success(data=item.ddata())
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def add(request):
    """
        add api
    :param request:
    :return:
    """
    try:
        form = forms.auth.admin.Add(request.POST)
        if form.is_valid():
            params = form.cleaned_data

            item = models.Admin(user=params['user'],
                                pwd=util.hash.sha1(params['pwd']),
                                name=params['name'],
                                phone=params['phone'],
                                disable=params['disable'],
                                ctime=int(time.time()))
            item.save()
            return resp.success(data=item.ddata())
        else:
            return resp.failure(str(form.errors))
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def update(request):
    """
        modify admin
    :param request:
    :return:
    """
    try:
        form = forms.auth.admin.Update(request.POST)
        if form.is_valid():
            params = form.cleaned_data

            models.Admin.objects.filter(id=params['id']).update(name=params['name'],
                                                                phone=params['phone'],
                                                                disable=params['disable'])
            return resp.success()
        else:
            return resp.failure(str(form.errors))
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def delete(request):
    """
        delete api
    :param request:
    :return:
    """
    try:
        form = forms.auth.admin.Delete(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            models.Admin.objects.filter(id=id).delete()
            return resp.success()
        else:
            return resp.failure(str(form.errors))
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def resetpwd(request):
    """
        delete api
    :param request:
    :return:
    """
    try:
        form = forms.auth.admin.ResetPwd(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            pwd = util.hash.sha1(form.cleaned_data['pwd'])

            models.Admin.objects.filter(id=id).update(pwd=pwd)

            return resp.success()
        else:
            return resp.failure(str(form.errors))
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def getroles(request):
    """
        get admin
    :param request:
    :return:
    """
    try:
        form = forms.auth.admin.Get(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']

            # get admin's roles
            roleids = []
            roles = models.Role.objects.filter(admin__id=id).all()
            for role in roles:
                roleids.append(role.id)

            # get all roles
            roles = models.Role.objects.all()

            total = roles.count()
            rows = []

            for role in roles:
                items = role.ddata()

                if role.id in roleids:
                    items['checked'] = True
                else:
                    items['checked'] = False

                rows.append(items);

            data = {
                'total': total,
                'rows': rows
            }

            return resp.success(data=data)
        else:
            roles = models.Role.objects.all()

            total = roles.count()
            rows = []

            for role in roles:
                items = role.ddata()
                items['checked'] = False
                rows.append(items);

            data = {
                'total': total,
                'rows': rows
            }
            return resp.success(data=data)
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def addroles(request):
    """
        update roles
    :param request:
    :return:
    """
    try:
        form = forms.auth.admin.AddRoles(request.POST)
        if form.is_valid():
            params = form.cleaned_data
            id = params['id']
            roles = params['roles'].split(',')

            adminroles = models.Admin.objects.get(id=id).roles.all()
            for role in roles:
                if not adminroles.filter(id=role).exists():
                    models.AdminRole(admin_id=id, role_id=role, ctime=int(time.time())).save()

            return resp.success()
        else:
            return resp.failure(str(form.errors))
    except Exception as e:
        return resp.failure(str(e))


@auth.need_login
def delroles(request):
    """
        update roles
    :param request:
    :return:
    """
    try:
        form = forms.auth.admin.AddRoles(request.POST)
        if form.is_valid():
            params = form.cleaned_data
            id = params['id']

            qs = None
            roles = params['roles'].split(',')
            for role in roles:
                if qs is None:
                    qs = Q(role__id=role)
                else:
                    qs = qs | Q(role__id=role)

            admin = models.Admin.objects.get(id=id)
            if qs is not None:
                admin.adminrole_set.filter(qs).delete()

            return resp.success()
        else:
            return resp.failure(str(form.errors))
    except Exception as e:
        return resp.failure(str(e))
