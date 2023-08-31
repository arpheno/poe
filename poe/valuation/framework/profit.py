from dataclasses import dataclass

from valuation.framework.valuation import Valuation


@dataclass
class Profitability:
    valuation: Valuation
    cost_base: Valuation

    def __mul__(self, other):
        return other * (1 + self.relative_profit)

    @property
    def absolute_profit(self):
        return self.valuation.estimate - self.cost_base.estimate

    @property
    def relative_profit(self):
        return (self.valuation.estimate - self.cost_base.estimate) / self.cost_base.estimate


def profitability_analysis(valuations: [Valuation]):
    lowest_purchasable = min((valuation for valuation in valuations if 'purchasable' in valuation.tags),
                             key=lambda x: x.estimate)
    return [Profitability(valuation, cost_base=lowest_purchasable) for valuation in valuations]
