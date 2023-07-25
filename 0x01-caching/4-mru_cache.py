#!/usr/bin/env python3
"""MRU Caching"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """MRU Caching"""
    cache_queue = []

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return
        if key not in self.cache_data:
            if len(self.cache_queue) >= self.MAX_ITEMS:
                # remove the last updated/ accessed item
                diss_key = self.cache_queue.pop(0)
                print('DISCARD: {}'.format(diss_key))
                self.cache_data.pop(diss_key)
            self.cache_data[key] = item
            self.cache_queue.insert(0, key)
        # if the value the key points to has changed
        if self.cache_data.get(key) != item:
            # insert the key in the head since it was just accessed.
            self.cache_queue.remove(key)
            self.cache_queue.insert(0, key)
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        # bring accessed item to the front
        if key in self.cache_queue:
            self.cache_queue.remove(key)
            self.cache_queue.insert(0, key)
        return self.cache_data.get(key, None)
