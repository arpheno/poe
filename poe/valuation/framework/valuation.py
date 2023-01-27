import math
from dataclasses import dataclass
from typing import List

from scipy.stats import norm

from poe.valuation.framework.rule import Rule


@dataclass
class Outcome:
    rules: [Rule]
    mean: float
    variance: float
    concrete_ingredients: List
    concrete_products: List

    def __repr__(self):
        return f'{self.type_line.ljust(25)} mean:{self.mean:.2f} stdev:{self.stdev:.2f} ctl:{self.chance_to_lose:.2f} {self.rules[0].info}'

    @property
    def type_line(self):
        return self.rules[0].type_line

    @property
    def stdev(self):
        return math.sqrt(self.variance)

    @property
    def chance_to_lose(self):
        return norm(loc=self.mean, scale=self.stdev).cdf(0)

    def __add__(self, other):
        return Outcome(rules=self.rules + other.rules, mean=self.mean + other.mean,
                       variance=self.variance + other.variance,
                       concrete_products=self.concrete_products + other.concrete_products,
                       concrete_ingredients=self.concrete_ingredients + other.concrete_ingredients)

    def __mul__(self, other: int):
        return Outcome(rules=[self.rules] * other,
                       mean=self.mean * other,
                       variance=self.variance * other,
                       concrete_products=self.concrete_products * other,
                       concrete_ingredients=self.concrete_ingredients * other)
