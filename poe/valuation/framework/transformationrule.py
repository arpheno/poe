from dataclasses import dataclass, field
from typing import List, Union
from poe.valuation.framework.models import Ingredient, ItemQuery

@dataclass
class TransformationRule:
    ingredients: List[Ingredient]
    products: List[ItemQuery]
    probabilities: List[float]
    multiplier: float = 1
    info: str = ''
    tags: List[str] = field(default_factory=list)
