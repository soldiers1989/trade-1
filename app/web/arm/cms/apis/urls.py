from django.urls import path
from cms.apis import auth, order

urlpatterns = [
    path('admin/login', auth.admin.login, name="api.admin.login"),
    path('admin/logout', auth.admin.logout, name="api.admin.logout"),
    path('admin/pwd/change', auth.admin.pwd, name="api.admin.pwd.change"),

    path('auth/admin/list', auth.admin.list, name="api.auth.admin.list"),
    path('auth/admin/get', auth.admin.get, name="api.auth.admin.get"),
    path('auth/admin/add', auth.admin.add, name="api.auth.admin.add"),
    path('auth/admin/update', auth.admin.update, name="api.auth.admin.update"),
    path('auth/admin/delete', auth.admin.delete, name="api.auth.admin.delete"),
    path('auth/admin/resetpwd', auth.admin.resetpwd, name="api.auth.admin.resetpwd"),
    path('auth/admin/role/list', auth.admin.getroles, name="api.auth.admin.role.list"),
    path('auth/admin/role/add', auth.admin.addroles, name="api.auth.admin.role.add"),
    path('auth/admin/role/del', auth.admin.delroles, name="api.auth.admin.role.del"),

    path('auth/role/list', auth.role.list, name="api.auth.role.list"),
]
