from dataclasses import dataclass

from valuation.framework.valuation import Valuation


@dataclass
class Profitability:
    valuation: Valuation
    absolute_profit: float
    relative_profit: float


def profitability_analysis(valuations: [Valuation]):
    lowest_purchasable = min(valuation.estimate for valuation in valuations if 'purchasable' in valuation.tags)
    return [Profitability(valuation,absolute_profit=valuation.estimate-lowest_purchasable,relative_profit=(valuation.estimate-lowest_purchasable)/lowest_purchasable) for valuation in valuations]
