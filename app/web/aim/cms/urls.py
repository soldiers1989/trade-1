from django.urls import path
from cms import apis, views

urlpatterns = [
    path('index/', views.index, name='cms.index'),

    path('login/', views.login, name='cms.login'),
    path('logout/', views.logout, name='cms.logout'),

    path('auth/admin/list/', views.auth_admin_list, name='cms.auth.admin.list'),

    path('auth/module/list/', views.auth_module_list, name='cms.auth.module.list'),

    path('api/login/', apis.login, name="cms.api.login")
]
