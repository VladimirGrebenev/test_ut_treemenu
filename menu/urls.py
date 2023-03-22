from django.urls import path

from menu.views import MainPageView


app_name = 'menu'

urlpatterns = [
    path('menu/', MainPageView.as_view(), name='index')
]