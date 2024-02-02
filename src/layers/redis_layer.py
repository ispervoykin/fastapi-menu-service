from init_redis import redis_db
class MenuRedis:
    def create(self, object, menu_id = -1):
        if menu_id == -1:
            redis_db.hset(f'menu{object["id"]}', mapping=object)
        else:
            redis_db.hset(f'menu{menu_id}', mapping=object)
    def get(self, menu_id):
        cache = redis_db.hgetall(f'menu{menu_id}')
        if cache != {}:
            return cache
    def delete(self, menu_id):
        redis_db.delete(f'menu{menu_id}')
    def delete_children(self, menu_id):
        for key in redis_db.scan_iter(f"menu{menu_id}*"):
            redis_db.delete(key)

class SubmenuRedis:
    def create(self, object, menu_id, submenu_id = -1):
        if submenu_id == -1:
            redis_db.hset(f'menu{menu_id}submenu{object["id"]}', mapping=object)
            if redis_db.hgetall(f'menu{menu_id}') != {}:
                redis_db.hincrby(f'menu{menu_id}', "submenus_count")
        else:
            redis_db.hset(f'menu{menu_id}submenu{submenu_id}', mapping=object)

    def get(self, menu_id, submenu_id):
        cache = redis_db.hgetall(f'menu{menu_id}submenu{submenu_id}')
        if cache != {}:
            return cache
        
    def delete(self, menu_id, submenu_id):
        redis_db.delete(f'menu{menu_id}submenu{submenu_id}')

    def delete_children(self, menu_id, submenu_id):
        for key in redis_db.scan_iter(f"menu{menu_id}submenu{submenu_id}*"):
            redis_db.delete(key)
        redis_db.delete(f"menu{menu_id}")

class DishRedis:
    def create(self, object, menu_id, submenu_id, dish_id = -1):
        if dish_id == -1:
            redis_db.hset(f'menu{menu_id}submenu{submenu_id}dish{object["id"]}', mapping=object)
            if redis_db.hgetall(f'menu{menu_id}') != {}:
                redis_db.hincrby(f'menu{menu_id}', "dishes_count")
            if redis_db.hgetall(f'menu{menu_id}submenu{submenu_id}') != {}:
                redis_db.hincrby(f'menu{menu_id}submenu{submenu_id}', "dishes_count")
        else:
            redis_db.hset(f'menu{menu_id}submenu{submenu_id}dish{dish_id}', mapping=object)

    def get(self, menu_id, submenu_id, dish_id):
        cache = redis_db.hgetall(f'menu{menu_id}submenu{submenu_id}dish{dish_id}')
        if cache != {}:
            return cache
        
    def delete(self, menu_id, submenu_id, dish_id):
        redis_db.delete(f'menu{menu_id}submenu{submenu_id}dish{dish_id}')

    def delete_children(self, menu_id, submenu_id, dish_id):
        for key in redis_db.scan_iter(f"menu{menu_id}submenu{submenu_id}dish{dish_id}*"):
            redis_db.delete(key)
        redis_db.delete(f"menu{menu_id}")
        redis_db.delete(f"menu{menu_id}submenu{submenu_id}")