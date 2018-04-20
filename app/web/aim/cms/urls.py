from django.conf.urls import url
from cms import apis, views

urlpatterns = [
    url(r'^index/$', views.index, name='cms.index'),
    url(r'^login/$', views.login, name='cms.login'),
    url(r'^logout/$', views.logout, name='cms.logout'),

    url(r'^api/login/$', apis.login, name="cms.api.login")
]
