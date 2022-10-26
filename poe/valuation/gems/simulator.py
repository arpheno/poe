import random
import statistics

cost=70
reward=600
weights= dict(
    a=lambda: 0,
    b= lambda: weights['a']()-cost+reward if random.randint(1, 120) <= 20 else weights['c']()-cost,
    c=lambda: weights['a']()-cost+reward if random.randint(1,70)<=20 else weights['b']()-cost,
)
result='c'
print(statistics.mean([weights['c']() for x in range(1000)]))
