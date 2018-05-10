from django.urls import path
from cms import apis, views

urlpatterns = [
    path('index/', views.index, name='cms.index'),

    path('test/', views.test, name='cms.test'),

    path('login/', views.login, name='cms.login'),
    path('logout/', views.logout, name='cms.logout'),

    path('auth/admin/add/', views.auth_admin_list, name='cms.auth.admin.add'),
    path('auth/admin/delete/', views.auth_admin_list, name='cms.auth.admin.delete'),
    path('auth/admin/modify/', views.auth_admin_list, name='cms.auth.admin.modify'),
    path('auth/admin/list/', views.auth_admin_list, name='cms.auth.admin.list'),

    path('auth/module/list/', views.auth_module_list, name='cms.auth.module.list'),

    path('order/order/list/', views.order_order_list, name='cms.order.order.list'),

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
]
