from dataclasses import dataclass
from typing import Dict, Callable, List

import pendulum
from scipy import stats

from poe.valuation.framework.price_store import PriceStore
from poe.valuation.framework.transformationrule import TransformationRule
from poe.valuation.framework.valuation import Valuation
import numpy as np


@dataclass
class Manifester:
    prices: PriceStore

    def manifest(self, rule: TransformationRule) -> Valuation:
        concrete_ingredients = self.map_to_concrete_items(rule.ingredients)
        concrete_products = self.map_to_concrete_items(rule.products)
        costs = np.array([ingredient.estimate for ingredient in concrete_ingredients])
        gains = np.array([product.estimate for product in concrete_products])
        probabilities = np.array(rule.probabilities)
        params = {
            'mean': self.mean(costs, gains, probabilities) * rule.multiplier,
            'variance': self.variance(costs, gains, probabilities) * rule.multiplier,
            'rules': [rule],
            'concrete_ingredients': concrete_ingredients,
            'concrete_products': concrete_products
        }
        return Valuation(rule.ingredients[0],estimate=costs[0]+params['mean'],timestamp=pendulum.now().int_timestamp,info=rule.info,tags=['rule'])
        # return Outcome(**params)

    # 100 0.3, 200 0.4 400 0.3
    def mean(self, costs: np.ndarray, gains: np.ndarray, probabilities: np.ndarray):
        return stats.rv_discrete(name='myvalue', values=(gains - np.sum(costs), probabilities)).mean()
        # return np.sum((gains - np.sum(costs)) * probabilities)

    def variance(self, costs: np.ndarray, gains: np.ndarray, probabilities: np.ndarray):
        return stats.rv_discrete(name='myvalue', values=(gains - np.sum(costs), probabilities)).var()
        # return np.sum(probabilities * ((gains - np.sum(costs)) - mean) ** 2)

    def map_to_concrete_items(self, funcs: [Callable]):
        results = [list(self.prices.query(func)) for func in funcs]
        return [item for candidates in results for item in candidates]
