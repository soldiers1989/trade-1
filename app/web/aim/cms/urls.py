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

    path('api/login/', apis.login, name="cms.api.login"),

    path('api/auth/admin/list/', apis.auth_admin_list, name="cms.api.auth.admin.list"),
    path('api/auth/admin/get/', apis.auth_admin_get, name="cms.api.auth.admin.get"),
    path('api/auth/admin/add/', apis.auth_admin_add, name="cms.api.auth.admin.add"),
    path('api/auth/admin/del/', apis.auth_admin_del, name="cms.api.auth.admin.del"),
    path('api/auth/admin/mod/', apis.auth_admin_mod, name="cms.api.auth.admin.mod"),

    path('api/auth/module/list/', apis.auth_module_list, name="cms.api.auth.module.list")
]
