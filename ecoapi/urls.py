from django.urls import path, include
from django.conf.urls import handler404
from django.contrib import admin
from api import urls as api_urls
from api.views import info_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
]

handler404 = 'api.views.custom_404'