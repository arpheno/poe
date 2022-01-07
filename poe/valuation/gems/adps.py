from collections import defaultdict
from pprint import pprint
from typing import List, Dict

from numpy import linalg

gem_names = {key: value for key, value in enumerate(["Anomalous", "Divergent", "Phantasmal", "Superior"])}
gem_indexes = {value: key for key, value in gem_names.items()}

import numpy as np
import pandas as pd


def adps(weight: Dict, value: Dict, value_f):
    _weight = [0, 0, 0, 0]
    _value = [0, 0, 0, 0]
    for key, v in weight.items():
        _weight[gem_indexes[key]] = v
    for key, v in value.items():
        _value[gem_indexes[key]] = v
    return adps_matrix(_weight, _value, value_f).T.rename(gem_names).rename(gem_names, axis=1)


def adps_matrix(weight: List, value: List, value_f: float):
    return pd.DataFrame(
        pd.Series(_adps_matrix(target, weight, value, value_f) if weight[target] else (0, 0, 0, 0))
        for target in range(len(weight))
    )


def _adps_matrix(target, weight, value, value_f):
    # This calculates the transition probabilities between states given weights
    denominators = np.array([weight[:x] + weight[x + 1 :] for x in range(len(weight))]).sum(axis=1)
    rho = np.array(weight) / (denominators.reshape(1, 4).T)
    # Set target transition out probabilities to 0
    rho[target] = 0
    # Get rid of invalid gems without weight
    if value[target] == 0:
        return np.array([0, 0, 0, 0])
    for i, w in enumerate(weight):
        if w < 0.1:
            rho[i] = 0
    # Things can't transition to themselves
    np.fill_diagonal(rho, -1)
    # each gem needs a transition to be worth something, so it costs `value_f`
    _value = np.array([value_f, value_f, value_f, value_f])
    # Except the target,which can sell
    _value[target] = -value[target]

    result = linalg.solve(rho, _value)
    return result


if __name__ == "__main__":
    print(adps_matrix([100, 20, 0, 50], [80, 1792, 0, 1], 240))
    print(
        adps(
            {"Divergent": 50, "Anomalous": 100, "Superior": 50},
            {"Divergent": 975.56, "Anomalous": 39.0, "Superior": 1.0},
            240,
        )
    )
