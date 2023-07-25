#!/usr/bin/env python3
"""FIFO caching """

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """FIFO caching """
    cache_queue = []

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return
        if key not in self.cache_data:
            if len(self.cache_queue) >= self.MAX_ITEMS:
                diss_key = self.cache_queue.pop()
                print('DISCARD: {}'.format(diss_key))
                self.cache_data.pop(diss_key)
            self.cache_data[key] = item
            self.cache_queue.insert(0, key)
        # if the value the key points to has changed
        if self.cache_data.get(key) != item:
            # do not treat the key as a new entry in the queue, just update the value
            self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        return self.cache_data.get(key, None)
