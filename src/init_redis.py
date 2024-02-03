import redis  # type: ignore

from config import REDIS_HOST, REDIS_PORT

redis_db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
