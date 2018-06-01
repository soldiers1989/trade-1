from django.urls import path
from cms.apis import auth, order

urlpatterns = [
    path('login/', auth.admin.login, name="cms.api.auth.admin.login"),
    path('logout/', auth.admin.login, name="cms.api.auth.admin.logout")
]
