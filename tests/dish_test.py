from conftest import client

pref = '/api/v1/menus'
menu_id = 1
submenu_id = 1
dish_id = 1


def test_create_menu1() -> None:
    global menu_id
    post_json = {
        'title': 'My menu 1',
        'description': 'My menu description 1'
    }
    response = client.post(pref, json=post_json)
    response_json = response.json()
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 201
    assert 'id' in response_json
    menu_id = response_json['id']


def test_create_submenu1() -> None:
    global submenu_id
    post_json = {
        'title': 'My submenu 1',
        'description': 'My submenu description 1'
    }
    response = client.post(pref + f'/{menu_id}/submenus', json=post_json)
    response_json = response.json()
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 201
    assert 'id' in response_json
    submenu_id = response_json['id']


def test_get_dishes1() -> None:
    response = client.get(pref + f'/{menu_id}/submenus' + f'/{submenu_id}/dishes')
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert response.json() == []


def test_create_dish1() -> None:
    global dish_id
    post_json = {
        'title': 'My dish 1',
        'description': 'My dish description 1',
        'price': '12.50'
    }
    response = client.post(pref + f'/{menu_id}/submenus' + f'/{submenu_id}/dishes', json=post_json)
    response_json = response.json()
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 201
    assert 'id' in response_json
    assert 'title' in response_json
    assert 'description' in response_json
    dish_id = response_json['id']


def test_get_dishes2() -> None:
    response = client.get(pref + f'/{menu_id}/submenus' + f'/{submenu_id}/dishes')
    response_json = response.json()
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert response_json != []


def test_get_dish1() -> None:
    response = client.get(pref + f'/{menu_id}/submenus' + f'/{submenu_id}/dishes' + f'/{dish_id}')
    response_json = response.json()
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert 'id' in response_json
    assert 'title' in response_json
    assert 'description' in response_json
    assert 'price' in response_json


def test_patch_dish1() -> None:
    patch_json = {
        'title': 'My updated dish 1',
        'description': 'My updated dish description 1',
        'price': '14.50'
    }
    response = client.patch(pref + f'/{menu_id}/submenus' + f'/{submenu_id}/dishes' + f'/{dish_id}', json=patch_json)
    response_json = response.json()
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert 'title' in response_json
    assert 'description' in response_json
    assert 'price' in response_json


def test_get_dish2() -> None:
    response = client.get(pref + f'/{menu_id}/submenus' + f'/{submenu_id}/dishes' + f'/{dish_id}')
    response_json = response.json()
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert 'id' in response_json
    assert 'title' in response_json
    assert 'description' in response_json
    assert 'price' in response_json


def test_delete_dish1() -> None:
    response = client.delete(pref + f'/{menu_id}/submenus' + f'/{submenu_id}/dishes' + f'/{dish_id}')
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.json() is None


def test_get_dishes3() -> None:
    response = client.get(pref + f'/{menu_id}/submenus' + f'/{submenu_id}/dishes')
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert response.json() == []


def test_get_dish3() -> None:
    response = client.get(pref + f'/{menu_id}/submenus' + f'/{submenu_id}/dishes' + f'/{dish_id}')
    response_json = {
        'detail': 'dish not found'
    }
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 404
    assert response.json() == response_json


def test_delete_submenu1() -> None:
    response = client.delete(pref + f'/{menu_id}/submenus' + f'/{submenu_id}')
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.json() is None


def test_get_submenus1() -> None:
    response = client.get(pref + f'/{menu_id}/submenus')
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert response.json() == []


def test_delete_menu1() -> None:
    response = client.delete(pref + f'/{menu_id}')
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.json() is None


def test_get_menus1() -> None:
    response = client.get(pref)
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert response.json() == []
