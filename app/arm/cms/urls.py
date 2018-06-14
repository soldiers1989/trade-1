from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('api/', include('cms.apis.urls')),
    path('cms/', include('cms.sites.urls'))
]
