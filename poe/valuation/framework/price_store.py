import logging
from collections import defaultdict
from itertools import groupby
from operator import attrgetter

from poe.valuation.framework.valuation import Valuation, domain_hash_key

logger = logging.getLogger(__name__)


class PriceStore:
    def query(self, func: dict):
        pass


class FlatPriceStore(PriceStore):
    def __init__(self, prices: [dict]):
        self.prices = prices

    def query(self, func):
        return filter(func, self.prices)


class ItemNotFound(Exception):
    pass


class HashKeyPriceStore(PriceStore):
    def __init__(self, valuations: [Valuation]):
        self._store = defaultdict(list)
        self._store.update(dict((k, list(values)) for k, values in
                                groupby(sorted(valuations, key=attrgetter('hash_key')), key=attrgetter('hash_key'))))
        offending_keys = [key for key, value in self._store.items() if len(value) > 1]
        for key in offending_keys:
            logger.warning(f'Multiple entries for key {key}, removing.')
            del self._store[key]

    def add(self, valuations: [Valuation]):
        for valuation in valuations:
            self._store[valuation.hash_key].append(valuation)

    def values(self):
        return self._store.values()

    def query(self, func: dict):
        if isinstance(func, list):
            return [self.query(v) for v in func]
        results = self._store[domain_hash_key(func)]
        if not results:
            results = self._store[domain_hash_key({**func, 'gem_quality': 20})]
        if not results:
            pass
            # raise ItemNotFound
        return results
