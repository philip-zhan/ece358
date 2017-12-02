import java.util.*;

public class LAN {

    private int N; // the number of computers connected to the LAN (variable)
    private int A; // Data packets arrive at the MAC layer following a Poisson process with an average arrival rate of A packets/second (variable)
    private int W; // the speed of the LAN (fixed)
    private int L; // packet length (fixed)
    private int ticksPerSec;
    private int totalSimulationTime;
    private boolean persistent;
    private double delay; // delay in terms of seconds

    public double totalThroughput;
    public double avgDelay;
    public int totalCollisions;
    public int totalErrors;

    LAN(int N, int A, int W, int L, int ticksPerSec, int simulatedSecs, boolean persistent) {
        this.N = N;
        this.A = A;
        this.W = W;
        this.L = L;
        this.ticksPerSec = ticksPerSec;
        this.totalSimulationTime = simulatedSecs;
        this.persistent = persistent;
        this.delay = 0.0000256;

        this.totalThroughput = 0;
        this.avgDelay = 0;
        this.totalCollisions = 0;
        this.totalErrors = 0;
    }

    public void simulate(){
        Computer[] computers = new Computer[N];
        boolean[][] statusQInit = new boolean[(int)(delay * ticksPerSec + 1)][N];
        ArrayDeque<boolean[]> statusQ = new ArrayDeque<>(Arrays.asList(statusQInit));
        for (int i = 0; i < N; i++) {
            computers[i] = new Computer(A, ticksPerSec, W, L, persistent);
        }
        for (int currentTick = 0; currentTick < totalSimulationTime * ticksPerSec; currentTick++) {
            boolean[] currentNetworkStatus = statusQ.remove();
            boolean[] futureNetworkStatus = new boolean[N];
            for (int i = 0; i < computers.length; i++) {
                boolean mediumBusy = false;
                for (int j = 0; j < currentNetworkStatus.length; j++) {
                    if (j != i && currentNetworkStatus[j]) { // another computer is using the network
                        mediumBusy = true;
                    }
                }
                futureNetworkStatus[i] = computers[i].tick(currentTick, mediumBusy);
            }
            statusQ.add(futureNetworkStatus);
        }
        computePerformance(computers);
    }

    private void computePerformance(Computer[] computers) {
        int M = 0; // Total number of transmitted packets
        int totalDelayTicks = 0;
        for (Computer computer : computers) {
            M += computer.outputList.size();
            for (int delay : computer.outputList) {
                totalDelayTicks += delay;
            }
            totalErrors += computer.errorCounter;
            totalCollisions += computer.collisionCounter;
        }
        totalThroughput = (double)M * L / totalSimulationTime / 1000; // Throughput in kbps
        avgDelay = (double)totalDelayTicks / M / (ticksPerSec/1000); // Delay in milliseconds
    }
}
