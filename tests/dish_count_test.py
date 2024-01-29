from conftest import client
menu_id = 1
submenu_id = 1
dish_id = 1

def test_create_menu1():
    global menu_id
    post_json = {
        "title": "My menu 1",
        "description": "My menu description 1"
    }
    response = client.post("/api/v1/menus", json=post_json)
    response_json = response.json()
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 201
    assert "id" in response_json
    menu_id = response_json["id"]

def test_create_submenu1():
    global submenu_id
    post_json = {
        "title": "My submenu 1",
        "description": "My submenu description 1"
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=post_json)
    response_json = response.json()
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 201
    assert "id" in response_json
    submenu_id = response_json["id"]

def test_create_dish1():
    global dish_id
    post_json = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=post_json)
    response_json = response.json()
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 201
    assert "id" in response_json
    dish_id = response_json["id"]

def test_create_dish2():
    global dish_id
    post_json = {
        "title": "My dish 2",
        "description": "My dish description 2",
        "price": "12.50"
    }
    response = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=post_json)
    response_json = response.json()
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 201
    assert "id" in response_json
    dish_id = response_json["id"]

def test_get_menu1():
    response = client.get(f"/api/v1/menus/{menu_id}")
    response_json = response.json()
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert "id" in response_json
    assert "submenus_count" in response_json
    assert "dishes_count" in response_json

def test_get_submenu1():
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    response_json = response.json()
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert "id" in response_json
    assert "dishes_count" in response_json

def test_delete_submenu1():
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.json() == None

def test_get_submenus1():
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert response.json() == []

def test_get_dishes1():
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert response.json() == []

def test_get_menu2():
    response = client.get(f"/api/v1/menus/{menu_id}")
    response_json = response.json()
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert "id" in response_json
    assert "submenus_count" in response_json
    assert "dishes_count" in response_json

def test_delete_menu1():
    response = client.delete(f"/api/v1/menus/{menu_id}")
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.json() == None

def test_get_menus1():
    response = client.get(f"/api/v1/menus/")
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert response.json() == []