from typing import List, Dict

from numpy import linalg

gem_names = {
    key: value
    for key, value in enumerate(["Anomalous", "Divergent", "Phantasmal", "Superior"])
}
gem_indexes = {value: key for key, value in gem_names.items()}

import numpy as np
import pandas as pd



import pandas as pd
from pydtmc import MarkovChain





def markov_adps(probabilities: dict, values: dict, cost: float):
    df = average_lenses_to_hit(probabilities)
    df = df * -cost  # Cost for regrading lenses
    df = df + pd.Series(values)  # Value from selling gem
    return df.sub(pd.Series(values), axis=0)  # Subtract cost of buying gem


def average_lenses_to_hit(probabilities):
    transitions = {quality: {q: probabilities.get(q, 0) for q in probabilities.keys() if q != quality} for quality in
                   probabilities.keys()}
    df = pd.DataFrame(transitions).T.fillna(0)[probabilities.keys()].apply(lambda x: x / x.sum(), axis=1)
    mc = MarkovChain(
        df.to_numpy(), list(probabilities.keys())
    )
    df = pd.DataFrame(mc.mean_first_passage_times_to(), index=probabilities.keys(), columns=probabilities.keys())
    return df


if __name__ == "__main__":
    print(
        markov_adps(
            {"Divergent": 50, "Anomalous": 100, "Superior": 50},
            {"Divergent": 975.56, "Anomalous": 39.0, "Superior": 1.0},
            240,
        )
    )
    print(
        markov_adps(
            {"Divergent": 10, "Anomalous": 100, "Superior": 50},
            {"Divergent": 975.56, "Anomalous": 39.0, "Superior": 1.0},
            100,
        )
    )
