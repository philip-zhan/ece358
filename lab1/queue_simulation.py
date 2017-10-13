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
EN = 0.0        # average number of packets in the buffer/queue
ET = 0.0        # average sojourn time
P_IDLE = 0.0    # the proportion of time the server is idle
P_LOSS = 0.0    # the packet loss probability (for M/D/1/K queue)
M = 10           # the number of times you repeat your experiments
# TICKS_PER_SEC = 1000000
TICK_DURATION = 0.000001  # the duration of a tick in seconds
SERVICE_TICKS: int  # the number of ticks it takes to serve a packet
IDLE = 0        # the number ticks that the server is idle


def main(argv):
    global Q, TICKS, LAM, L, C, K, SERVICE_TICKS, EN
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

    SERVICE_TICKS = int(L / C / TICK_DURATION)

    for i in range(1, M+1):
        EN += (discrete_time() - EN) / i

    print(EN)


def discrete_time():
    global Q
    Q = deque(maxlen=K)
    en = 0.0
    next_arrival = 1
    ticks_served = 1
    for tick in range(1, TICKS+1):
        # print("tick:", tick)
        next_arrival = packet_generator(tick, next_arrival)
        ticks_served = packet_server(tick, ticks_served)
        en += (len(Q) - en) / tick
    # compute_performance()
    return en


def packet_generator(tick, next_arrival):
    if tick == next_arrival and (K is None or len(Q) <= K):
        new_packet = packet.Packet(tick)
        Q.appendleft(new_packet)
        next_arrival += get_random_var()
        # print("packet arrived at tick:", new_packet.generated_tick)
        # print("size of the queue:", len(Q))
        # print("next packet arrives at:", next_arrival)
        # for item in q:
        #     print(int(packet.Packet(item).generated_tick))
    return next_arrival


def packet_server(tick, ticks_served):
    global IDLE
    if ticks_served == SERVICE_TICKS and Q:  # the last tick of the current packet and Q is not empty
        Q.pop()
        ticks_served = 1
    elif Q:  # not the last tick of the current packet and Q is not empty
        ticks_served += 1
    elif ticks_served == SERVICE_TICKS:  # the last tick of the current packet and Q is empty
        print("Error in Q")
    else:  # not the last tick of the current packet and Q is empty
        IDLE += 1
    return ticks_served


def get_random_var():
    random_var = int((-1 / LAM) * math.log(1 - random.random()) / TICK_DURATION)
    # print(random_var)
    return random_var


def compute_performance():
    print("E[N]:", EN)
    print("E[T]:", ET)
    print("P_IDLE:", P_IDLE)
    return


if __name__ == '__main__':
    main(sys.argv[1:])
    # print(ticks, lam, l, c, k)
