from dataclasses import dataclass
import pandas as pd


@dataclass
class SplinterInfo:
    splinter_price: pd.Series
    completed_set_price: pd.Series
    set_size: int

    @property
    def value(self):
        return pd.concat([self.completed_set_price / self.set_size, self.splinter_price], axis=1).max(axis=1)
