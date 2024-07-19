#!/usr/bin/env python3
'''
This script counts and caches requests to a given URL
'''

from functools import wraps
import redis
import requests
from typing import Callable

# Initialize the Redis client
redis_client = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """Decorator for counting and caching requests"""
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper for the decorator"""
        # Increment the count for this URL
        redis_client.incr(f"count:{url}")

        # Check if the HTML content is already cached
        cached_html = redis_client.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')

        # If not cached, fetch the HTML content and cache it
        html = method(url)
        redis_client.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """Obtain the HTML content of a URL"""
    response = requests.get(url)
    return response.text
