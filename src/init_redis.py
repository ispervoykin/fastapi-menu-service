import redis

redis_db = redis.Redis(host="localhost", port=6379, decode_responses=True)