from src.main import app


def reverse(name: str, kwargs: dict[str, int] = {}) -> str:
    routes = [{'path': route.path, 'name': route.name} for route in app.routes]
    url = ''
    for route in routes:
        if route['name'] == name:
            url = route['path']

    assert url != '', f'No route with the name "{name}"'

    return url.format(**kwargs)
