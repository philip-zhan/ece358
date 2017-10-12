import queue_simulation
import math
import random

TICKS = 100000
L = 2000
C = 1000000
for i in range(2, 10):
    mu = i / 10
    LAM = mu * C / L
    # print(LAM)
    # random_var = 1000000 * (-1 / LAM) * math.log(1 - random.random())
    # print(random_var)
    queue_simulation.main([TICKS, LAM, L, C])
