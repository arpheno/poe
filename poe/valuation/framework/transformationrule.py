from dataclasses import dataclass, field
from typing import Callable

@dataclass
class TransformationRule:
    ingredients: [dict]
    products: [dict]
    probabilities: [dict]
    multiplier: float = 1
    info: str = ''
    tags: [str] = field(default_factory=list)
