#!/usr/bin/env python3
"""
Redis Module
This module provides functionality to count requests
to a URL and cache the HTML content of the URL using Redis.
"""

from functools import wraps
import redis
import requests
from typing import Callable

# Initialize the Redis client
redis_client = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """
    Decorator to count the number of times a URL is requested.
    It also caches the HTML content of the URL for 10 seconds.

    Args:
        method (Callable): The function to be decorated.

    Returns:
        Callable: The wrapped function.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Wrapper function for the decorator.

        Args:
            url (str): The URL to be requested.

        Returns:
            str: The HTML content of the URL.
        """
        # Increment the count for the URL
        redis_client.incr(f"count:{url}")

        # Check if the HTML content is already cached
        cached_html = redis_client.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')

        # If not cached, fetch the HTML content
        html = method(url)

        # Cache the HTML content for 10 seconds
        redis_client.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a URL.

    Args:
        url (str): The URL to fetch the HTML content from.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
