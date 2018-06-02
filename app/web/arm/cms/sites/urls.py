from cms.sites import home
from django.urls import path

urlpatterns = [
    path('login/', home.login, name='cms.login'),

    path('', home.index, name='cms'),
    path('index/', home.index, name='cms.index'),
    path('index/header/', home.header, name="cms.index.header"),
    path('index/footer/', home.footer, name="cms.index.footer"),
    path('index/menus/', home.menus, name="cms.index.menus"),
    path('index/welcome/', home.header, name="cms.index.welcome"),
]
