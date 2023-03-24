from django import template

from menu.models import Item, Menu

register = template.Library()


@register.inclusion_tag('menu/tree_menu.html', takes_context=True)
def draw_menu(context, menu):
    current_url = context['request'].path
    menu_items = Item.objects.all().select_related('menu', 'parent').filter(
        menu__title=menu).order_by('parent_id')
    sorted_menu_items = []
    tree = []

    for item in menu_items:
        if item.parent_id is None:
            sorted_menu_items.append(item)
        else:
            for i, sort_item in enumerate(sorted_menu_items):
                if item.parent_id == sort_item.id:
                    sorted_menu_items.insert(i + 1, item)

    active = True
    parent_last_id = sorted_menu_items[0].id
    root_id = sorted_menu_items[0].id
    for item in sorted_menu_items:
        if current_url == item.url:
            parent_last_id = item.parent_id

    last_active_id = sorted_menu_items[0].id
    for item in sorted_menu_items:
        tree.append({
            'id': item.id,
            'name': item.title,
            'menu_name': menu,
            'parent': item.parent_id,
            'url': item.url if item.url != '' else '/',
            'active': active,
        })
        if active:
            last_active_id = item.id
        if item.url == current_url:
            active = False
        if item.url == '' and current_url == '/':
            active = False

    for item in tree:
        if item['parent'] is None:
            item['active'] = True
        elif item['parent'] == last_active_id:
            item['active'] = True
        elif item['parent'] == parent_last_id:
            item['active'] = True
        elif item['parent'] == root_id:
            item['active'] = True
        else:
            item['active'] = False

    for item in tree:
        if item['url'] == current_url:
            item['active'] = True
            parent_id = item['parent']
            while parent_id is not None:
                for parent_item in tree:
                    if parent_item['id'] == parent_id:
                        parent_item['active'] = True
                        parent_id = parent_item['parent']
                        break
                else:
                    parent_id = None
                if parent_id == 1:
                    break
        else:
            continue

    return {
        'menu_tree': tree,
    }

@register.simple_tag(takes_context=True)
def render_menu(context, menu_tree, current_item=None):
    result = ''
    for item in menu_tree:
        if item['parent'] == current_item and item['active'] == True:
            result += f'<li><a href="{item["url"]}" ' \
                      f'{"class=active" if item["active"] else ""}>' \
                      f'{item["name"]}</a>'
            sub_menu = render_menu(context, menu_tree, item['id'])
            if sub_menu:
                result += f'<ul>{sub_menu}</ul>'
            result += '</li>'
    return result
