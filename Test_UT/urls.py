from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("<slug:title_slug>/", TemplateView.as_view(
        template_name="menu/index.html"), name="menu-item"),
    path("", TemplateView.as_view(template_name="menu/index.html")),
]
