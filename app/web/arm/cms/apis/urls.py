from django.urls import path
from cms.apis import auth, trade

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
    path('auth/role/add', auth.role.add, name="api.auth.role.add"),
    path('auth/role/update', auth.role.update, name="api.auth.role.update"),
    path('auth/role/delete', auth.role.delete, name="api.auth.role.delete"),
    path('auth/role/module/tree', auth.role.moduletree, name="api.auth.role.module.tree"),
    path('auth/role/module/add', auth.role.addmodule, name="api.auth.role.module.add"),
    path('auth/role/module/del', auth.role.delmodule, name="api.auth.role.module.del"),

    path('auth/module/list', auth.module.list, name="api.auth.module.list"),
    path('auth/module/tree', auth.module.tree, name="api.auth.module.tree"),
    path('auth/module/add', auth.module.add, name="api.auth.module.add"),
    path('auth/module/update', auth.module.update, name="api.auth.module.update"),
    path('auth/module/delete', auth.module.delete, name="api.auth.module.delete"),

    path('trade/lever/list', trade.lever.list, name="api.trade.lever.list"),
    path('trade/lever/get', trade.lever.get, name="api.trade.lever.get"),
    path('trade/lever/add', trade.lever.add, name="api.trade.lever.add"),
    path('trade/lever/update', trade.lever.update, name="api.trade.lever.update"),
    path('trade/lever/delete', trade.lever.delete, name="api.trade.lever.delete"),
    path('trade/lever/reorder', trade.lever.reorder, name="api.trade.lever.reorder"),

    path('trade/order/list', trade.order.list, name="api.trade.order.list"),
]
