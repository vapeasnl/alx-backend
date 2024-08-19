#!/usr/bin/env python3
""" define BasicCache class """
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """ inherits from BasicCaching and is a caching system """
    def put(self, key, item):
        """
        Must assign to the dictionary self.cache_data the item value
        for the key key.
        """
        if key is not None and item is not None:
            # self.cache_data.update({key: item})
            self.cache_data[key] = item

    def get(self, key):
        """
        return the value in self.cache_data linked to key
        """
        if key is None:
            return None
        return self.cache_data.get(key)
