#!/usr/bin/env python3
'''
This module implements the Cache class that
stores data in Redis
'''
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    A decorator function to count how many times methods of
    the Cache class are called.
    It takes a single method Callable argument and
    returns a Callable.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A decorator function to store the history of inputs
    and outputs of a method of the Cache class.
    It takes a single method Callable argument and
    returns a Callable.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"
        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, result)
        return result
    return wrapper


def replay(method: Callable):
    """
    A decorator function to print the history of inputs
    and outputs of a method of the Cache class.
    It takes a single method Callable argument and
    returns None.
    """
    redis = method.__self__._redis
    r = redis.Redis()
    input_key = method.__qualname__ + ":inputs"
    output_key = method.__qualname__ + ":outputs"
    inputs = r.lrange(input_key, 0, -1)
    outputs = r.lrange(output_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for input, output in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{input.decode('utf-8')}) ->
              {output.decode('utf-8')}")


class Cache:
    '''
    Implements a Cache class that stores data in Redis
    '''
    def __init__(self):
        '''
        Constructor for the Cache class
        '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        Method to store data in Redis
        '''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self,
            key: str,
            fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float, None]:
        '''
        Method to get data from Redis
        '''
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        '''
        Method to get string data from Redis
        '''
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> int:
        '''
        Method to get int data from Redis
        '''
        return self.get(key, int)
