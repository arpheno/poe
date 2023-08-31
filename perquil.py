import random

import numpy as np


def advantage(min, max):
    return np.mean([np.max([random.randint(min, max), random.randint(min, max)]) for i in range(10000)])


def regular(min, max):
    return np.mean([np.max([random.randint(min, max)]) for i in range(10000)])


a = advantage(30905, 112700)
r = regular(30905, 112700)
print(f'Without perquil:{r}')
print(f'With perquil:{a}')
print(f'{(a - r) / r * 100}% more damage')
