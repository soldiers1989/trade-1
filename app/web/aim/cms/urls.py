from django.urls import path
from cms import apis, views


urlviews = [
    path('index/', views.home.index, name='cms.index'),

    path('login/', views.auth.admin.login, name='cms.login'),
    path('logout/', views.auth.admin.logout, name='cms.logout'),

    path('auth/admin/list/', views.auth.admin.list, name='cms.auth.admin.list'),
    path('auth/module/list/', views.auth.module.list, name='cms.auth.module.list'),
    path('auth/auth/list/', views.auth.auth.list, name='cms.auth.auth.list'),

    path('order/lever/list/', views.order.lever.list, name='cms.order.lever.list'),

    path('order/order/mgmt/', views.order.order.mgmt, name='cms.order.order.mgmt')
]


urlapis = [
    path('apis/auth/admin/login/', apis.auth.admin.login, name="cms.apis.auth.admin.login"),
    path('apis/auth/admin/list/', apis.auth.admin.list, name="cms.apis.auth.admin.list"),
    path('apis/auth/admin/get/', apis.auth.admin.get, name="cms.apis.auth.admin.get"),
    path('apis/auth/admin/add/', apis.auth.admin.add, name="cms.apis.auth.admin.add"),
    path('apis/auth/admin/del/', apis.auth.admin.delete, name="cms.apis.auth.admin.del"),
    path('apis/auth/admin/mod/', apis.auth.admin.modify, name="cms.apis.auth.admin.mod"),

    path('apis/auth/module/list/', apis.auth.module.list, name="cms.apis.auth.module.list"),
    path('apis/auth/module/get/', apis.auth.module.get, name="cms.apis.auth.module.get"),
    path('apis/auth/module/add/', apis.auth.module.add, name="cms.apis.auth.module.add"),
    path('apis/auth/module/del/', apis.auth.module.delete, name="cms.apis.auth.module.del"),
    path('apis/auth/module/mod/', apis.auth.module.modify, name="cms.apis.auth.module.mod"),

    path('apis/auth/auth/list/', apis.auth.auth.list, name="cms.apis.auth.auth.list"),
    path('apis/auth/auth/get/', apis.auth.auth.get, name="cms.apis.auth.auth.get"),
    path('apis/auth/auth/add/', apis.auth.auth.add, name="cms.apis.auth.auth.add"),
    path('apis/auth/auth/del/', apis.auth.auth.delete, name="cms.apis.auth.auth.del"),
    path('apis/auth/auth/mod/', apis.auth.auth.modify, name="cms.apis.auth.auth.mod"),

    path('apis/order/lever/list/', apis.order.lever.list, name="cms.apis.order.lever.list"),
    path('apis/order/lever/get/', apis.order.lever.get, name="cms.apis.order.lever.get"),
    path('apis/order/lever/add/', apis.order.lever.add, name="cms.apis.order.lever.add"),
    path('apis/order/lever/del/', apis.order.lever.delete, name="cms.apis.order.lever.del"),
    path('apis/order/lever/mod/', apis.order.lever.modify, name="cms.apis.order.lever.mod"),
    path('apis/order/lever/ord/', apis.order.lever.reorder, name="cms.apis.order.lever.ord"),

    path('apis/order/order/list/', apis.order.order.list, name="cms.apis.order.order.list")
]

urlpatterns = urlviews + urlapis
