import queue_simulation
import math
import random

TICKS = 1000000
L = 2000
C = 1000000

print("p,E[N],E[T],P_IDLE")

for i in range(2, 10):
    p = i / 10
    LAM = p * C / L
    EN, ET, P_LOSS, P_IDLE = queue_simulation.main([TICKS, LAM, L, C])
    print("{},{},{},{}".format(p, EN, ET, P_IDLE))
    # print(LAM)
    # random_var = 1000000 * (-1 / LAM) * math.log(1 - random.random())
    # print(random_var)
# en = list()
# en.append(1)
# en.append(1.1)
# print(sum(en))
