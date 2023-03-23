from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from menu.views import index


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    re_path(r'^(.*)/$', index, name='index')
]
