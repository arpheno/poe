from poe.valuation.framework.tft_adapter.adapter import TftAdapter
from poe.valuation.framework.tft_adapter.factory import TimestampedWholesalePricesFactory
from poe.valuation.framework.valuation import Valuation


def test_tft_adapter():
    adapter = TftAdapter()
    response = adapter.adapt()
    assert isinstance(response[0],Valuation)

