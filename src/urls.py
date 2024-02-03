def reverse(name: str, kwargs: dict[str, int] = {}) -> str:
    url = urls.get(name, None)
    if url is None:
        raise KeyError(name)
    return url.format(**kwargs)


urls = {
    'menus': '/api/v1/menus/',
    'menu': '/api/v1/menus/{menu_id}/',
    'submenus': '/api/v1/menus/{menu_id}/submenus/',
    'submenu': '/api/v1/menus/{menu_id}/submenus/{submenu_id}/',
    'dishes': '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/',
    'dish': '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}/',
}
