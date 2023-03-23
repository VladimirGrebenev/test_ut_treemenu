from django.contrib import admin
from menu.models import Menu, Item


class ItemAdmin(admin.ModelAdmin):
    # form = MenuItemForm
    list_display = ('title', 'menu', 'parent', 'url')
    list_filter = ('menu', 'parent',)
    prepopulated_fields = {'url': ('title',)}

    def save_model(self, request, obj, form, change):
        obj.url = '/' + obj.menu.title + '/' + obj.url + '/'
        obj.save()


admin.site.register(Item, ItemAdmin)
admin.site.register(Menu)


