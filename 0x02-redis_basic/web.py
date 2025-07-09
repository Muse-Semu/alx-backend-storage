import redis
import requests
from typing import Callable
from functools import wraps

# Initialize Redis client
redis_client = redis.Redis()

def count_access(method: Callable) -> Callable:
    """Decorator to count the number of times a URL is accessed"""
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper function that increments access count and calls original method"""
        count_key = f"count:{url}"
        redis_client.incr(count_key)
        return method(url)
    return wrapper

def cache_page(method: Callable) -> Callable:
    """Decorator to cache the page content with a 10-second expiration"""
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper function that caches result and returns cached or fresh content"""
        cache_key = f"cache:{url}"
        cached_content = redis_client.get(cache_key)
        if cached_content is not None:
            return cached_content.decode("utf-8")
        content = method(url)
        redis_client.setex(cache_key, 10, content)
        return content
    return wrapper

@count_access
@cache_page
def get_page(url: str) -> str:
    """Fetch HTML content from a URL and return it"""
    response = requests.get(url)
    return response.text