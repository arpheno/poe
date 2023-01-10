from dataclasses import dataclass

from poe.ninja import CHAOS_ORB


@dataclass
class Valuation:
    type_line: str
    estimate: float
    info: str = ''
    confidence: float = 1
    currency: str = CHAOS_ORB

    @property
    def details(self):
        return f'Item: {self.type_line} Estimate: {self.estimate} Info: {self.info}'
