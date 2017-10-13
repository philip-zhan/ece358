import queue_simulation

TICKS = 100000
L = 2000
C = 1000000
K1 = 10
K2 = 25
K3 = 50
for i in range(5, 15):
	mu = i / 10
	LAM = mu * C / L
	queue_simulation.main([TICKS, LAM, L, C, K1])
for i in range(5, 15):
	mu = i / 10
	LAM = mu * C / L
	queue_simulation.main([TICKS, LAM, L, C, K2])
for i in range(5, 15):
	mu = i / 10
	LAM = mu * C / L
	queue_simulation.main([TICKS, LAM, L, C, K3])

