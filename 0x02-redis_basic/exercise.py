#!/usr/bin/env python3
"""
Implement Redis Module

This module contains the Cache class that stores and retrieves data
from a Redis server.

This module provides the following decorators:

    - count_calls
    - call_history
    - replay
"""

import redis
import requests
from typing import Callable, Optional, Union
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and
    outputs for a particular function.
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper for decorator functionality.
        """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


def replay(method: Callable) -> None:
    """
    Replays the history of a function.
    Args:
        method: The function to be decorated
    Returns:
        None
    """
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name)
    if calls:
        calls = calls.decode("utf-8")
        print(f"{name} was called {calls} times:")
        inputs = cache.lrange(name + ":inputs", 0, -1)
        outputs = cache.lrange(name + ":outputs", 0, -1)
        for i, o in zip(inputs, outputs):
            print(f"{name}(*{i.decode('utf-8')}) -> {o.decode('utf-8')}")
    else:
        print(f"{name} was not called.")


class Cache:
    """
    Implement Cache class.
    """
    def __init__(self):
        """
        Initialize the cache.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in the cache.
        """
        random_key = str(uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self,
            key: str,
            fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float]:
        """
        Get data from the cache.
        """
        value = self._redis.get(key)
        if value and fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        Get a string from the cache.
        """
        value = self._redis.get(key)
        if value:
            return value.decode('utf-8')
        return ""

    def get_int(self, key: str) -> int:
        """
        Get an int from the cache.
        """
        value = self._redis.get(key)
        if value:
            try:
                return int(value.decode('utf-8'))
            except ValueError:
                return 0
        return 0


def count_requests(method: Callable) -> Callable:
    """
    Decorator to count and cache requests.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Wrapper for the decorator.
        """
        redis_client = redis.Redis()
        redis_client.incr(f"count:{url}")
        cached_html = redis_client.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')
        html = method(url)
        redis_client.setex(f"cached:{url}", 10, html)
        return html
    return wrapper


@count_requests
def get_page(url: str) -> str:
    """
    Obtain the HTML content of a URL.
    """
    response = requests.get(url)
    return response.text


# Example usage
if __name__ == "__main__":
    cache = Cache()

    # Store and retrieve examples
    key = cache.store("example data")
    print(f"Stored data with key: {key}")
    print(f"Retrieved data: {cache.get_str(key)}")

    # Replay history example
    cache.store("first call")
    cache.store("second call")
    replay(cache.store)

    # Get page example
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))
    print(get_page(url))
    print(get_page(url))
