from django.urls import path
from cms.apis import auth, trade, user, stock

urlpatterns = [
    path('admin/login', auth.admin.login, name="api.admin.login"),
    path('admin/logout', auth.admin.logout, name="api.admin.logout"),
    path('admin/whoami', auth.admin.whoami, name="api.admin.whoami"),
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
    path('trade/order/add', trade.order.add, name="api.trade.order.add"),
    path('trade/order/fees', trade.order.fees, name="api.trade.order.fees"),
    path('trade/order/margins', trade.order.margins, name="api.trade.order.margins"),
    path('trade/order/orders', trade.order.orders, name="api.trade.order.orders"),
    path('trade/order/lever', trade.order.lever, name="api.trade.order.lever"),

    path('user/user/list', user.user.list, name="api.user.user.list"),
    path('user/user/query', user.user.query, name="api.user.user.query"),
    path('user/user/has', user.user.has, name="api.user.user.has"),
    path('user/user/stat', user.user.stat, name="api.user.user.stat"),
    path('user/user/banks', user.user.banks, name="api.user.user.banks"),
    path('user/user/trades', user.user.trades, name="api.user.user.trades"),
    path('user/user/bills', user.user.bills, name="api.user.user.bills"),
    path('user/user/coupons', user.user.coupons, name="api.user.user.coupons"),
    path('user/user/stocks', user.user.stocks, name="api.user.user.stocks"),
    path('user/user/charges', user.user.charges, name="api.user.user.charges"),
    path('user/user/draws', user.user.draws, name="api.user.user.draws"),
    path('user/user/resetpwd', user.user.resetpwd, name="api.user.user.resetpwd"),


    path('user/coupon/list', user.coupon.list, name="api.user.coupon.list"),
    path('user/coupon/add', user.coupon.add, name="api.user.coupon.add"),
    path('user/coupon/update', user.coupon.update, name="api.user.coupon.update"),
    path('user/coupon/delete', user.coupon.delete, name="api.user.coupon.delete"),

    path('stock/stock/list', stock.stock.list, name="api.stock.stock.list"),
    path('stock/stock/add', stock.stock.add, name="api.stock.stock.add"),
    path('stock/stock/update', stock.stock.update, name="api.stock.stock.update"),
    path('stock/stock/delete', stock.stock.delete, name="api.stock.stock.delete"),
    path('stock/stock/query', stock.stock.query, name="api.stock.stock.query"),
    path('stock/stock/has', stock.stock.has, name="api.stock.stock.has"),
]
