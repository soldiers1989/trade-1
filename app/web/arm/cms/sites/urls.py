from cms.sites import home
from django.urls import path

urlpatterns = [
    path('index/', home.index, name='cms.index'),
    path('login/', home.login, name='cms.login'),
    path('logout/', home.logout, name='cms.logout')
]
