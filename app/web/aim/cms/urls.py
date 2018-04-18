from django.conf.urls import url
from cms import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login/$', views.login),
]
