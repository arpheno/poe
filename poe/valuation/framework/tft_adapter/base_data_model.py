from typing import List

from pydantic import BaseModel

from poe.valuation.framework.valuation import Valuation


class WholesalePriceData(BaseModel):
    name: str
    divine: float
    chaos: float
    lowConfidence: bool
    ratio: float


class TimestampedWholesalePrices(BaseModel):
    timestamp: int
    data: List[WholesalePriceData]

    def as_valuations(self):
        return [Valuation({'name': item.name}, estimate=item.chaos, timestamp=self.timestamp, info='tft_bulk_prices',
                          tags=['sellable', 'purchasable', 'bulk']) for item in self.data]
