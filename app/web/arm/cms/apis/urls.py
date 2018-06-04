from django.urls import path
from cms.apis import auth, order

urlpatterns = [
    path('admin/login', auth.admin.login, name="api.admin.login"),
    path('admin/logout', auth.admin.logout, name="api.admin.logout"),
    path('admin/pwd/change', auth.admin.pwd, name="api.admin.pwd.change"),

    path('auth/admin/list', auth.admin.list, name="api.auth.admin.list"),
]
