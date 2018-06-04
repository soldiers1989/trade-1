from cms.sites import index, login, auth
from django.urls import path

urlpatterns = [
    path('login/', login.login, name='cms.login'),

    path('', index.index, name='cms'),
    path('index/', index.index, name='cms.index'),

    path('auth/admin/', auth.admin, name="cms.auth.admin"),
    path('auth/module/', auth.module, name="cms.auth.module"),
    path('auth/authority/', auth.authority, name="cms.auth.module"),
]
