from dataclasses import dataclass
from typing import Union
from poe.valuation.framework.models import ItemQuery

def domain_hash_key(key: Union[dict, ItemQuery]):
    if isinstance(key, ItemQuery):
        key = key.dict(exclude_none=True)
    return str(sorted(key.items()))


@dataclass
class Valuation:
    key: ItemQuery
    estimate: float
    timestamp: int
    tags: list
    info: str = ""
    breakdown: dict = None

    def details(self):
        print(self.info)
        return self.info

    @property
    def hash_key(self):
        return domain_hash_key(self.key)
