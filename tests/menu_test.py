from conftest import client

from src.urls import reverse

menu_id = 1


def test_get_menus_empty() -> None:
    response = client.get(reverse('menus'))
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert response.json() == []


def test_create_menu() -> None:
    global menu_id
    post_json = {
        'title': 'My menu 1',
        'description': 'My menu description 1'
    }
    response = client.post(reverse('menus'), json=post_json)
    response_json = response.json()
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 201
    assert 'id' in response_json
    menu_id = response_json['id']


def test_get_menus_not_empty() -> None:
    response = client.get(reverse('menus'))
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert response.json() != []


def test_get_menu_success() -> None:
    response = client.get(reverse('menu', {'menu_id': menu_id}))
    response_json = response.json()
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert 'id' in response_json
    assert 'title' in response_json
    assert 'description' in response_json


def test_patch_menu() -> None:
    patch_json = {
        'title': 'My updated menu 1',
        'description': 'My updated menu description 1'
    }
    response = client.patch(reverse('menu', {'menu_id': menu_id}), json=patch_json)
    response_json = response.json()
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert 'title' in response_json
    assert 'description' in response_json


def test_get_menu_patched() -> None:
    response = client.get(reverse('menu', {'menu_id': menu_id}))
    response_json = response.json()
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert 'id' in response_json
    assert 'title' in response_json
    assert 'description' in response_json


def test_delete_menu() -> None:
    response = client.delete(reverse('menu', {'menu_id': menu_id}))
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.json() is None


def test_get_menus_empty2() -> None:
    response = client.get(reverse('menus'))
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert response.json() == []


def test_get_menu_not_found() -> None:
    response = client.get(reverse('menu', {'menu_id': menu_id}))
    response_json = {
        'detail': 'menu not found'
    }
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 404
    assert response.json() == response_json
