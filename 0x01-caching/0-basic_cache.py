#!/usr/bin/env python3
"""Basic Cache"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """Basic Cache"""

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        return self.cache_data.get(key, None)
