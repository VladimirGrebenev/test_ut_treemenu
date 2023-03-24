from django import template

from menu.models import Item, Menu

register = template.Library()


@register.inclusion_tag('menu/tree_menu.html', takes_context=True)
def draw_menu(context, menu):

    try:
        items = Item.objects.all().select_related('menu', 'parent').filter(
            menu__title=menu).order_by('parent_id').values()
        primary_item = [item for item in items if item['parent_id'] is None]
        selected_item_id = int(context['request'].GET[menu])
        selected_item = [item for item in items if
                         selected_item_id == item['id']][0]
        selected_item_id_list = get_selected_item_id_list(selected_item,
                                                          primary_item,
                                                          selected_item_id,
                                                          items)

        for item in primary_item:
            if item['id'] in selected_item_id_list:
                item['child_items'] = get_child_items(items, item['id'],
                                                      selected_item_id_list)
        result_dict = {'items': primary_item}

    except:
        result_dict = {
            'items': [
                item for item in
                Item.objects.filter(menu__title=menu, parent=None).values()
            ]
        }

    result_dict['menu'] = menu
    result_dict['other_querystring'] = get_querystring(context, menu)

    return result_dict


def get_querystring(context, menu):
    querystring_args = []
    for key in context['request'].GET:
        if key != menu:
            querystring_args.append(key + '=' + context['request'].GET[key])
    querystring = ('&').join(querystring_args)
    return querystring


def get_child_items(items, current_item_id, selected_item_id_list):
    item_list = [item for item in items if item['parent_id'] ==
                 current_item_id]
    for item in item_list:
        if item['id'] in selected_item_id_list:
            item['child_items'] = get_child_items(items, item['id'],
                                                  selected_item_id_list)
    return item_list


def get_selected_item_id_list(parent, primary_item, selected_item_id, items):
    selected_item_id_list = []

    while True:
        if parent['parent_id'] is not None:
            selected_item_id_list.append(parent['id'])
        else:
            selected_item_id_list.append(parent['id'])
            break
        for item in items:
            if item['id'] == parent['parent_id']:
                parent = item
    if not selected_item_id_list:
        for item in primary_item:
            if item['id'] == selected_item_id:
                selected_item_id_list.append(selected_item_id)
    return selected_item_id_list
