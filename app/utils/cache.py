import time
from typing import Any


class CacheItem:
    def __init__(self, key: str, value: list, ttl: int):
        self.key = key
        self.value = value
        self.ttl = ttl
        self.created_at = time.time()

    def is_expired(self):
        return time.time() - self.created_at > self.ttl


class Cache:
    def __init__(self):
        self.cache = {}

    def get(self, key: str) -> Any:
        if key in self.cache:
            item = self.cache[key]
            if not item.is_expired():
                return item.value
            else:
                del self.cache[key]
        return None

    def set(self, key: str, value: Any, ttl: int) -> None:
        item = CacheItem(key, value, ttl)
        self.cache[key] = item

    def delete(self, key: str) -> None:
        if key in self.cache:
            del self.cache[key]
