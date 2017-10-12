import queue_simulation

TICKS = 100000
L = 20009
C = 1000000
for i in range(2, 10):
    mu = i / 10
    LAM = mu * C / L
    queue_simulation.main([TICKS, LAM, L, C])
