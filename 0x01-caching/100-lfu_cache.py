#!/usr/bin/env python3
"""LFU Caching """

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """LFU Caching """
    min_freq = 0         # freq or count of lfu
    freq_map = {}        # {freq: [list of keys based on lru]}
    key_count_map = {}  # {key: freq or count of keys}

    def update_tracking_metrics(self, key):
        """update cache_data, min_freq freq_map, and key_count_map
        for the existing key->val"""
        updated_key_freq = self.key_count_map[key]
        self.freq_map[updated_key_freq].remove(key)
        if len(self.freq_map[updated_key_freq]) == 0\
                and updated_key_freq == self.min_freq:
            self.min_freq += 1

        # update the freq of the updated key and ann it to a higher list in
        # frq_key_map
        updated_key_freq += 1
        self.key_count_map[key] = updated_key_freq
        if self.freq_map.get(updated_key_freq) is None\
                or self.freq_map.get(updated_key_freq) == []:
            self.freq_map[updated_key_freq] = [key]
        else:
            self.freq_map[updated_key_freq].append(key)

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return
        if key not in self.cache_data:
            if len(self.cache_data.values()) >= self.MAX_ITEMS:
                # remove lru_item from freq_map, key_count_map and
                # cache_data
                lru_list = self.freq_map[self.min_freq]
                lru_key = lru_list.pop(0)
                print("DISCARD: {}".format(lru_key))
                self.key_count_map.pop(lru_key)
                self.cache_data.pop(lru_key)
            # update min_freq freq_map, key_count_map and cache_data
            # for the new key->val
            self.min_freq = 1
            self.cache_data[key] = item
            self.key_count_map[key] = 1
            if self.freq_map.get(1) is None or self.freq_map.get(1) == []:
                self.freq_map[1] = [key]
            else:
                self.freq_map[1].append(key)
            return

        # it does not matter whether the value the key points to has changed.
        # update the cache regardless
        self.cache_data[key] = item
        self.update_tracking_metrics(key)

    def get(self, key):
        """ Get an item by key
        """
        # bring accessed item to the front
        if key in self.cache_data:
            self.update_tracking_metrics(key)

        return self.cache_data.get(key, None)
