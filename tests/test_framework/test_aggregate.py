from poe.valuation.framework.aggregate import Aggregate
from poe.valuation.framework.valuation import Valuation


def test_valuation_can_be_constructed():
    valuation = Valuation('Home', 60)
    assert valuation


def test_aggregate_can_be_constructed():
    agg = Aggregate([Valuation('Home', 60), Valuation('Home', 40)])
