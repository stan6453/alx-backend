#!/usr/bin/env python3
"""LIFO caching """

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """LIFO caching """
    cache_stack = []

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return
        if key not in self.cache_data:
            if len(self.cache_stack) >= self.MAX_ITEMS:
                diss_key = self.cache_stack.pop()
                print('DISCARD: {}'.format(diss_key))
                self.cache_data.pop(diss_key)
            self.cache_data[key] = item
            self.cache_stack.append(key)
        # if the value the key points to has changed
        if self.cache_data.get(key) != item:
            # treat the key as a new entry in the stack since
            # its value changed.
            self.cache_stack.remove(key)
            self.cache_stack.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        return self.cache_data.get(key, None)
