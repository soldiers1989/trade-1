from cms.sites import index, login, auth, trade, user, stock, sys
from django.urls import path

urlpatterns = [
    path('login/', login.login, name='cms.login'),

    path('', index.index, name='cms'),
    path('index/', index.index, name='cms.index'),

    path('auth/admin/', auth.admin, name="cms.auth.admin"),
    path('auth/module/', auth.module, name="cms.auth.module"),
    path('auth/role/', auth.role, name="cms.auth.role"),

    path('trade/account/', trade.account, name="cms.trade.account"),
    path('trade/lever/', trade.lever, name="cms.trade.lever"),
    path('trade/order/', trade.order, name="cms.trade.order"),
    path('trade/dash/', trade.dash, name="cms.trade.dash"),


    path('user/user/', user.user, name="cms.user.user"),
    path('user/bill/', user.bill, name="cms.user.bill"),
    path('user/coupon/', user.coupon, name="cms.user.coupon"),
    path('user/charge/', user.charge, name="cms.user.charge"),
    path('user/draw/', user.draw, name="cms.user.draw"),
    path('user/trade/', user.trade, name="cms.user.trade"),
    path('user/order/', user.order, name="cms.user.order"),

    path('stock/stock/', stock.stock, name="cms.stock.stock"),

    path('sys/crond/', sys.crond, name="cms.sys.crond"),
]
