import redis
from flask import current_app


def check_redis_connection():
    redis_url = current_app.config['REDIS_URL']
    r = redis.from_url(redis_url)
    try:
        r.ping()
        print("Successfully connected to Redis.")
    except redis.ConnectionError as e:
        print(f"Failed to connect to Redis: {e}")
        raise
