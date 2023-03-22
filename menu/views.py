from django.views.generic import TemplateView
from menu.models import Item

class MainPageView(TemplateView):
    template_name = "menu/index.html"
    model = Item
    queryset = Item.objects.select_related('items').prefetch_related(
        'childrens').all()
