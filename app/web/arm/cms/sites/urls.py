from cms.sites import home
from django.urls import path

urlpatterns = [
    path('', home.index, name='cms'),
    path('index/', home.index, name='cms.index'),
    path('login/', home.login, name='cms.login')
]
