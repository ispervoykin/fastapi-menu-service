from conftest import client
pref = "/api/v1/menus"
menu_id = 1

def test_get_menus1():
    response = client.get(pref)
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert response.json() == []

def test_create_menu1():
    global menu_id
    post_json = {
        "title": "My menu 1",
        "description": "My menu description 1"
    }
    response = client.post(pref, json=post_json)
    response_json = response.json()
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 201
    assert "id" in response_json
    menu_id = response_json["id"]

def test_get_menus2():
    response = client.get(pref)
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert response.json() != []

def test_get_menu1():
    response = client.get(pref + f"/{menu_id}")
    response_json = response.json()
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert "id" in response_json
    assert "title" in response_json
    assert "description" in response_json

def test_patch_menu1():
    patch_json = {
        "title": "My updated menu 1",
        "description": "My updated menu description 1"
    }
    response = client.patch(pref + f"/{menu_id}", json=patch_json)
    response_json = response.json()
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert "title" in response_json
    assert "description" in response_json

def test_get_menu2():
    response = client.get(pref + f"/{menu_id}")
    response_json = response.json()
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert "id" in response_json
    assert "title" in response_json
    assert "description" in response_json

def test_delete_menu1():
    response = client.delete(pref + f"/{menu_id}")
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.json() == None

def test_get_menus3():
    response = client.get(pref)
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 200
    assert response.json() == []

def test_get_menu3():
    response = client.get(pref + f"/{menu_id}")
    response_json = {
        "detail": "menu not found"
    }
    assert response.headers.get('Content-Type') == 'application/json'
    assert response.status_code == 404
    assert response.json() == response_json