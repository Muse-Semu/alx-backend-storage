import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of times a method is called"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function that increments counter and calls original method"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """Decorator to store input and output history of a method in Redis lists"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function that stores inputs/outputs and calls original method"""
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, output)
        return output
    return wrapper

def replay(method: Callable) -> None:
    """Display the history of calls for a particular function"""
    cache = method.__self__._redis
    qualname = method.__qualname__
    call_count = cache.get(qualname)
    call_count = int(call_count) if call_count else 0
    
    print(f"{qualname} was called {call_count} times:")
    
    inputs = cache.lrange(f"{qualname}:inputs", 0, -1)
    outputs = cache.lrange(f"{qualname}:outputs", 0, -1)
    
    for input_args, output in zip(inputs, outputs):
        input_str = input_args.decode("utf-8")
        output_str = output.decode("utf-8")
        print(f"{qualname}(*{input_str}) -> {output_str}")

class Cache:
    def __init__(self):
        """Initialize Redis client and flush database"""
        self._redis = redis.Redis()
        self._redis.flushdb()
    
    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis with random key and return the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
    
    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """Retrieve data from Redis by key and apply optional conversion function"""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data
    
    def get_str(self, key: str) -> Optional[str]:
        """Retrieve data as string from Redis by key"""
        return self.get(key, fn=lambda d: d.decode("utf-8"))
    
    def get_int(self, key: str) -> Optional[int]:
        """Retrieve data as integer from Redis by key"""
        return self.get(key, fn=int)

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