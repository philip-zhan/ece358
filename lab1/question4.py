import queue_simulation
import time

TICKS = 1000000
L = 2000
C = 1000000
K = [10, 25, 50]

f = open("result/q4_{}.csv".format(int((time.time()-1507925570)/30)), 'w')
f.write("p,E[N],E[T],P_LOSS,P_IDLE,E[N],E[T],P_LOSS,P_IDLE,E[N],E[T],P_LOSS,P_IDLE")

for i in range(5, 16):
    p = i / 10
    LAM = p * C / L
    line = [p]
    for k in K:
        print('simulating p = {}, K = {}'.format(p, k))
        EN, ET, P_LOSS, P_IDLE = queue_simulation.main([TICKS, LAM, L, C, k])
        line += [EN, ET, P_LOSS, P_IDLE]
    f.write("\n" + ",".join(map(str, line)))

f.close()
