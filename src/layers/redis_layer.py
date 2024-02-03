from init_redis import redis_db


class MenuRedis:
    def create(self, object: dict[str, str], menu_id: int = -1) -> None:
        if menu_id == -1:
            redis_db.hset(f'menu{object["id"]}', mapping=object)
        else:
            redis_db.hset(f'menu{menu_id}', mapping=object)

    def get(self, menu_id: int) -> dict[str, str] | None:
        cache = redis_db.hgetall(f'menu{menu_id}')
        if cache != {}:
            return cache
        return None

    def delete(self, menu_id: int) -> None:
        redis_db.delete(f'menu{menu_id}')

    def delete_children(self, menu_id: int) -> None:
        for key in redis_db.scan_iter(f'menu{menu_id}*'):
            redis_db.delete(key)


class SubmenuRedis:
    def create(self, object: dict[str, str], menu_id: int, submenu_id: int = -1) -> None:
        if submenu_id == -1:
            redis_db.hset(f'menu{menu_id}submenu{object["id"]}', mapping=object)
            if redis_db.hgetall(f'menu{menu_id}') != {}:
                redis_db.hincrby(f'menu{menu_id}', 'submenus_count')
        else:
            redis_db.hset(f'menu{menu_id}submenu{submenu_id}', mapping=object)

    def get(self, menu_id: int, submenu_id: int) -> dict[str, str] | None:
        cache = redis_db.hgetall(f'menu{menu_id}submenu{submenu_id}')
        if cache != {}:
            return cache
        return None

    def delete(self, menu_id: int, submenu_id: int) -> None:
        redis_db.delete(f'menu{menu_id}submenu{submenu_id}')

    def delete_children(self, menu_id: int, submenu_id: int) -> None:
        for key in redis_db.scan_iter(f'menu{menu_id}submenu{submenu_id}*'):
            redis_db.delete(key)
        redis_db.delete(f'menu{menu_id}')


class DishRedis:
    def create(self, object: dict[str, str], menu_id: int, submenu_id: int, dish_id: int = -1) -> None:
        if dish_id == -1:
            redis_db.hset(f'menu{menu_id}submenu{submenu_id}dish{object["id"]}', mapping=object)
            if redis_db.hgetall(f'menu{menu_id}') != {}:
                redis_db.hincrby(f'menu{menu_id}', 'dishes_count')
            if redis_db.hgetall(f'menu{menu_id}submenu{submenu_id}') != {}:
                redis_db.hincrby(f'menu{menu_id}submenu{submenu_id}', 'dishes_count')
        else:
            redis_db.hset(f'menu{menu_id}submenu{submenu_id}dish{dish_id}', mapping=object)

    def get(self, menu_id: int, submenu_id: int, dish_id: int) -> dict[str, str] | None:
        cache = redis_db.hgetall(f'menu{menu_id}submenu{submenu_id}dish{dish_id}')
        if cache != {}:
            return cache
        return None

    def delete(self, menu_id: int, submenu_id: int, dish_id: int) -> None:
        redis_db.delete(f'menu{menu_id}submenu{submenu_id}dish{dish_id}')

    def delete_children(self, menu_id: int, submenu_id: int, dish_id: int) -> None:
        for key in redis_db.scan_iter(f'menu{menu_id}submenu{submenu_id}dish{dish_id}*'):
            redis_db.delete(key)
        redis_db.delete(f'menu{menu_id}')
        redis_db.delete(f'menu{menu_id}submenu{submenu_id}')
