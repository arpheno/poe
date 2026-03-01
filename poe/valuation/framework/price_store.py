import logging
from collections import defaultdict
from itertools import groupby
from operator import attrgetter

from poe.valuation.framework.valuation import Valuation, domain_hash_key

logger = logging.getLogger(__name__)


from poe.valuation.framework.models import ItemQuery

class PriceStore:
    def query(self, query: ItemQuery):
        pass


class FlatPriceStore(PriceStore):
    def __init__(self, prices: [dict]):
        self.prices = prices

    def query(self, query: ItemQuery):
        # This is slow and legacy, but we keep it for now
        return [p for p in self.prices if query.matches(p)]


class ItemNotFound(Exception):
    pass


class HashKeyPriceStore(PriceStore):
    def __init__(self, valuations: [Valuation]):
        self._store = defaultdict(list)
        # Group valuations by their hash key
        sorted_valuations = sorted(valuations, key=attrgetter('hash_key'))
        for k, values in groupby(sorted_valuations, key=attrgetter('hash_key')):
            self._store[k] = list(values)
            
        offending_keys = [key for key, value in self._store.items() if len(value) > 1]
        for key in offending_keys:
            logger.warning(f'Multiple entries for key {key}, removing.')
            del self._store[key]

    def add(self, valuations: [Valuation]):
        for valuation in valuations:
            self._store[valuation.hash_key].append(valuation)

    def values(self):
        return self._store.values()

    def query(self, query: ItemQuery):
        if isinstance(query, list):
            return [self.query(v) for v in query]
            
        key = domain_hash_key(query)
        results = self._store.get(key)
        
        if not results:
            # Fallback logic (legacy) - maybe remove this later
            # Try with quality 20 if not specified?
            if query.gem_quality is None:
                 # Create a new query with quality 20
                 q20 = query.copy(update={'gem_quality': 20})
                 results = self._store.get(domain_hash_key(q20))

        if not results:
            return []
            # raise ItemNotFound
        return results
