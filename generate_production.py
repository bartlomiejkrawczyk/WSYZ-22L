import statistics
import math
import random
import sys

S = int(sys.argv[1])
W = 34  # 34 for ziemniaki & kapusta, 10 for buraki & marchew

samples = statistics.NormalDist(0.5, 0.05).samples(52)
samples_sum = sum(samples)

prod = [S*i/samples_sum for i in samples]

assert math.isclose(sum(prod), S)
prod.sort()

for i in range(13):
    scl = prod[4*i:4*i+4]
    random.shuffle(scl)
    prod[4*i:4*i+4] = scl

prod = prod[0::2] + prod[-2::-2]
prod = prod[26-W:] + prod[:26-W]

# print(sum(prod))

for e in prod:
    print(f'{e:.4f}'.replace('.', ','))
