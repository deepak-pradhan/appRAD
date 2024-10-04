from functools import wraps
from redis import Redis

redis_client = Redis(host='localhost', port=6379, db=0)

def cache(expire=300, backend='memory'):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{args}:{kwargs}"
            if backend == 'redis':
                result = redis_client.get(key)
                if result:
                    return result
            # Implement your caching logic here
            result = await func(*args, **kwargs)
            redis_client.set(key, result, ex=expire)
            return result
        return wrapper
    return decorator    