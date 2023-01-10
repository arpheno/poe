from dataclasses import dataclass
from itertools import groupby

from poe.valuation.framework.valuation import Valuation


@dataclass
class Aggregate:
    def __init__(self, valuations: [Valuation]):
        self._store=dict(groupby(sorted(valuations,key=lambda x: x.type_line),key=lambda x:x.type_line))
