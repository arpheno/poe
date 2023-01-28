from dataclasses import dataclass
from typing import Callable


@dataclass
class Rule:
    ingredients: [dict]
    products: [dict]
    probabilities: [dict]
    multiplier: float = 1
    info: str = ''
    tags: [str] = list
