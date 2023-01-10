import random
import statistics


probabilities = {"Divergent": 10, "Anomalous": 100, "Superior": 50}
values = {"Divergent": 975.56, "Anomalous": 39.0, "Superior": 1.0}
cost=240
reward=values['Divergent']
weights= dict(
    divergent=lambda: 0,
    superior= lambda: weights['divergent']()-cost+reward if random.randint(1, 110) <= 10 else weights['anomalous']()-cost,
    anomalous=lambda: weights['divergent']()-cost+reward if random.randint(1,60)<=10 else weights['superior']()-cost,
)
print(statistics.mean([weights['anomalous']() for x in range(1000)]))
