import timeit
from collections import defaultdict
from functools import partial

from typing import List, Dict, Callable

from contextlib import contextmanager
import matplotlib.pyplot as plt


@contextmanager
def data_provider(data_size, setup=lambda N: N, teardown=lambda: None):
    data = setup(data_size)
    yield data
    teardown(*data)


def run_performance_comparison(approaches: List[Callable],
                               data_size: List[int],
                               *,
                               setup=lambda N: [N],
                               teardown=lambda *N: None,
                               number_of_repetitions=5,
                               title='Performance Comparison',
                               data_name='N',
                               yscale='log',
                               xscale='log'):
    approach_times = defaultdict(list)
    for N in data_size:
        with data_provider(N, setup, teardown) as data:
            print(f'Running performance comparison for {data_name}={N}')

            for approach in approaches:
                function = partial(approach, *data)
                approach_time = min(timeit.Timer(function).repeat(repeat=number_of_repetitions, number=1))
                approach_times[approach].append(approach_time)

    for approach in approaches:
        plt.plot(data_size, approach_times[approach], label=approach.__name__)
    plt.yscale(yscale)
    plt.xscale(xscale)

    plt.xlabel(data_name)
    plt.ylabel('Execution Time (seconds)')
    plt.title(title)
    plt.legend()
    plt.show()
