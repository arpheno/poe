from pydtmc import MarkovChain

probabilities = {"Divergent": 10, "Anomalous": 100, "Superior": 50}
values = {"Divergent": 975.56, "Anomalous": 39.0, "Superior": 1.0},
mc = MarkovChain(
    [[0, 100 / 150, 50 / 150],
     [10 / 60, 0, 50 / 60],
     [10 / 110, 100 / 110, 0]],
    ['Divergent', 'Anomalous', 'Superior']
)
