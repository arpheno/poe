from collections import Callable
from dataclasses import dataclass
import pandas as pd


@dataclass
class SplinterInfo:
    splinter_price: pd.Series
    completed_set_price: pd.Series
    splinter_query: Callable
    set_size: int
