#!/usr/bin/env python3

import sys
import packet
from collections import deque
import math
import random


Q: deque        # a queue representing the input buffer
TICKS: int      # tick is an integer constant that represents the duration of simulation
LAM: float      # average number of packets generated / arrived(packets per second)
L: int          # length of a packet in bits
C: int          # the service time received by a packet (example: the transmission rate of the output link in bits per second)
K: int          # the size of the buffer in number of packets
MU: float       # utilization of the queue
EN: float = 0.0 # average number of packets in the buffer/queue
ET: float = 0.0 # average sojourn time
P_IDLE: float   # the proportion of time the server is idle
P_LOSS: float   # the packet loss probability (for M/D/1/K queue)
M: int = 1      # the number of times you repeat your experiments
TICKS_PER_SEC = 1000  # the number of ticks in one second


def main(argv):
    global Q, TICKS, LAM, L, C, K
    K = None
    if len(argv) >= 4:
        TICKS = int(argv[0])
        LAM = float(argv[1])
        L = int(argv[2])
        C = int(argv[3])
        if len(argv) == 5:
            K = int(argv[4])
    else:
        TICKS = int(input("TICKS: "))
        LAM = float(input("LAMBDA: "))
        L = int(input("L: "))
        C = int(input("C: "))
        k = input("K (press Enter if performing the M/D/1 simulation): ")
        if k != "":
            K = int(k)

    for i in range(M):
        Q = deque(maxlen=K)
        discrete_time()
        compute_performance()


def discrete_time():
    global EN
    next_arrival = 1
    # ticks_served = 0
    for tick in range(1, TICKS+1):
        # print("tick:", tick)
        next_arrival = packet_generator(tick, next_arrival)
        packet_server(tick)
        EN += (len(Q) - EN) / tick


def packet_generator(tick, next_arrival):
    if tick == next_arrival and (K is None or len(Q) <= K):
        new_packet = packet.Packet(tick)
        Q.appendleft(new_packet)
        next_arrival += get_random_var()
        print("packet arrived at tick:", new_packet.generated_tick)
        print("size of the queue:", len(Q))
        # print("next packet arrives at:", next_arrival)
        # for item in q:
        #     print(int(packet.Packet(item).generated_tick))
    return next_arrival


def packet_server(tick):
    service_time = - (-L // C)  # ceiling integer division
    # print("service time:", service_time)
    if tick % service_time == 0 and Q:
        Q.pop()
    # if ticks_served < service_time:
    #     ticks_served += 1
    # elif q:
    #     q.pop()
    # if q:
    #     ticks_served = 1


def get_random_var():
    return int((-1 / LAM) * math.log(1 - random.random()))


def compute_performance():
    print("E[N]:", EN)
    print("E[T]:", ET)
    print("P_IDLE:", P_IDLE)
    return


if __name__ == '__main__':
    main(sys.argv[1:])
    # print(ticks, lam, l, c, k)
