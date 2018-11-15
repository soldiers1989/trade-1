from django.urls import path

from cms.apis import auth, trade, user, stock
from cms.apis import echo, enum


urlpatterns = [
    path('echo', echo.echo, name="api.echo"),
    path('enum', enum.list, name="api.enum"),

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

    path('trade/account/list', trade.account.list, name="api.trade.account.list"),
    path('trade/account/add', trade.account.add, name="api.trade.account.add"),
    path('trade/account/update', trade.account.update, name="api.trade.account.update"),
    path('trade/account/delete', trade.account.delete, name="api.trade.account.delete"),

    path('trade/order/list', trade.order.list, name="api.trade.order.list"),
    path('trade/order/get', trade.order.get, name="api.trade.order.get"),
    path('trade/order/add', trade.order.add, name="api.trade.order.add"),
    path('trade/order/update', trade.order.update, name="api.trade.order.update"),
    path('trade/order/delete', trade.order.delete, name="api.trade.order.delete"),
    path('trade/order/status', trade.order.status, name="api.trade.order.status"),
    path('trade/order/process', trade.order.process, name="api.trade.order.process"),

    path('user/user/list', user.user.list, name="api.user.user.list"),
    path('user/user/query', user.user.query, name="api.user.user.query"),
    path('user/user/has', user.user.has, name="api.user.user.has"),
    path('user/user/banks', user.user.banks, name="api.user.user.banks"),
    path('user/user/trades', user.user.trades, name="api.user.user.trades"),
    path('user/user/bills', user.user.bills, name="api.user.user.bills"),
    path('user/user/coupons', user.user.coupons, name="api.user.user.coupons"),
    path('user/user/stocks', user.user.stocks, name="api.user.user.stocks"),
    path('user/user/charges', user.user.charges, name="api.user.user.charges"),
    path('user/user/draws', user.user.draws, name="api.user.user.draws"),
    path('user/user/resetpwd', user.user.resetpwd, name="api.user.user.resetpwd"),

    path('user/trade/list', user.trade.list, name="api.user.trade.list"),
    path('user/trade/get', user.trade.get, name="api.user.trade.get"),
    path('user/trade/add', user.trade.add, name="api.user.trade.add"),
    path('user/trade/update', user.trade.update, name="api.user.trade.update"),
    path('user/trade/delete', user.trade.delete, name="api.user.trade.delete"),
    path('user/trade/fees', user.trade.fees, name="api.user.trade.fees"),
    path('user/trade/margins', user.trade.margins, name="api.user.trade.margins"),
    path('user/trade/orders', user.trade.orders, name="api.user.trade.orders"),
    path('user/trade/lever', user.trade.lever, name="api.user.trade.lever"),
    path('user/trade/status', user.trade.status, name="api.user.trade.status"),
    path('user/trade/process', user.trade.process, name="api.user.trade.process"),

    path('user/order/list', user.order.list, name="api.user.order.list"),
    path('user/order/get', user.order.get, name="api.user.order.get"),
    path('user/order/add', user.order.add, name="api.user.order.add"),
    path('user/order/update', user.order.update, name="api.user.order.update"),
    path('user/order/delete', user.order.delete, name="api.user.order.delete"),
    path('user/order/status', user.order.status, name="api.user.order.status"),
    path('user/order/process', user.order.process, name="api.user.order.process"),

    path('user/coupon/list', user.coupon.list, name="api.user.coupon.list"),
    path('user/coupon/add', user.coupon.add, name="api.user.coupon.add"),
    path('user/coupon/update', user.coupon.update, name="api.user.coupon.update"),
    path('user/coupon/delete', user.coupon.delete, name="api.user.coupon.delete"),

    path('user/bill/list', user.bill.list, name="api.user.bill.list"),
    path('user/bill/add', user.bill.add, name="api.user.bill.add"),
    path('user/bill/update', user.bill.update, name="api.user.bill.update"),
    path('user/bill/delete', user.bill.delete, name="api.user.bill.delete"),

    path('user/charge/list', user.charge.list, name="api.user.charge.list"),
    path('user/charge/add', user.charge.add, name="api.user.charge.add"),
    path('user/charge/update', user.charge.update, name="api.user.charge.update"),
    path('user/charge/delete', user.charge.delete, name="api.user.charge.delete"),

    path('user/draw/list', user.draw.list, name="api.user.draw.list"),
    path('user/draw/add', user.draw.add, name="api.user.draw.add"),
    path('user/draw/update', user.draw.update, name="api.user.draw.update"),
    path('user/draw/delete', user.draw.delete, name="api.user.draw.delete"),

    path('stock/stock/list', stock.stock.list, name="api.stock.stock.list"),
    path('stock/stock/add', stock.stock.add, name="api.stock.stock.add"),
    path('stock/stock/update', stock.stock.update, name="api.stock.stock.update"),
    path('stock/stock/delete', stock.stock.delete, name="api.stock.stock.delete"),
    path('stock/stock/query', stock.stock.query, name="api.stock.stock.query"),
    path('stock/stock/has', stock.stock.has, name="api.stock.stock.has"),
]
