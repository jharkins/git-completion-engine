import redis


def check_redis_connection(redis_url):
    r = redis.from_url(redis_url)
    try:
        r.ping()
        print("Successfully connected to Redis.")
    except redis.ConnectionError as e:
        print(f"Failed to connect to Redis: {e}")
        raise
