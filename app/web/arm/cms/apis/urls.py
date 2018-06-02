from django.urls import path
from cms.apis import user, auth, order

urlpatterns = [
    path('login/', user.login, name="api.user.login"),
    path('user/', user.user, name="api.user.user"),
    path('logout/', user.logout, name="api.user.logout")
]
