import queue_simulation
import time

TICKS = 1000000
L = 2000
C = 1000000

f = open("result/q2_{}.csv".format(int((time.time()-1507925570)/30)), 'w')
f.write("p,E[N],E[T],P_IDLE")

for i in range(2, 10):
    p = i / 10
    LAM = p * C / L
    print('simulating p =', p)
    EN, ET, P_LOSS, P_IDLE = queue_simulation.main([TICKS, LAM, L, C])
    f.write("\n{},{},{},{}".format(p, EN, ET, P_IDLE))

f.close()
