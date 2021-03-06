import sys
from collections import deque
import math
import random


Q: deque            # a queue representing the input buffer
TICKS: int          # tick is an integer constant that represents the duration of simulation
LAM: float          # average number of packets generated / arrived(packets per second)
L: int              # length of a packet in bits
C: int              # the service time received by a packet
K: int              # the size of the buffer in number of packets
SERVICE_TICKS: int  # the number of ticks it takes to serve a packet
EN = 0.0            # average number of packets in the buffer/queue
ET = 0.0            # average sojourn time
P_IDLE = 0.0        # the proportion of time the server is idle
P_LOSS = 0.0        # the packet loss probability (for M/D/1/K queue)
M = 10              # the number of times you repeat your experiments
TICK_DURATION = 0.000001  # the duration of a tick in seconds


def main(argv):
    global Q, TICKS, LAM, L, C, K, SERVICE_TICKS, EN, ET, P_IDLE, P_LOSS
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
        avg_queue_size, avg_sojourn_time, loss_rate, idle_rate = discrete_time()
        EN += (avg_queue_size - EN) / i
        ET += (avg_sojourn_time - ET) / i
        P_LOSS += (loss_rate - P_LOSS) / i
        P_IDLE += (idle_rate - P_IDLE) / i

    return EN, ET, P_LOSS, P_IDLE


def discrete_time():
    global Q
    Q = deque(maxlen=K)
    queue_size_list = []
    sojourn_time_list = []
    total_loss = 0
    total_idle = 0
    next_arrival = 1
    ticks_served = 1
    for tick in range(1, TICKS+1):
        next_arrival, loss = packet_generator(tick, next_arrival)
        total_loss += loss

        ticks_served, sojourn_time, idle = packet_server(tick, ticks_served)
        queue_size_list.append(len(Q))
        if sojourn_time != 0:
            sojourn_time_list.append(sojourn_time)
        total_idle += idle
    return compute_performance(queue_size_list, sojourn_time_list, total_loss, total_idle)


def packet_generator(tick, next_arrival):
    loss = 0
    if tick == next_arrival:
        if K is None or len(Q) < K:
            Q.appendleft(tick)
        else:
            loss = 1
        next_arrival += get_random_var()
    return next_arrival, loss


def packet_server(tick, ticks_served):
    sojourn_time = 0
    idle = 0
    if not Q:  # Q is empty
        idle = 1
    else:  # Q is not empty
        if ticks_served < SERVICE_TICKS:  # not the last tick of the current packet
            ticks_served += 1
        else:  # the last tick of the current packet
            ticks_served = 1
            sojourn_time = tick - Q.pop()
    return ticks_served, sojourn_time, idle


def get_random_var():
    return int((-1 / LAM) * math.log(1 - random.random()) / TICK_DURATION)


def compute_performance(queue_size_list, sojourn_time_list, total_loss, total_idle):
    avg_queue_size = sum(queue_size_list) / len(queue_size_list)
    avg_sojourn_time = TICK_DURATION * sum(sojourn_time_list) / len(sojourn_time_list)
    loss_rate = total_loss / len(sojourn_time_list)
    idle_rate = total_idle / TICKS
    return avg_queue_size, avg_sojourn_time, loss_rate, idle_rate


if __name__ == '__main__':
    main(sys.argv[1:])
