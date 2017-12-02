import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Random;

public class Computer {
    enum State {
        SENSE_MEDIUM,
        TRANSMIT,
        SEND_JAMMING_BITS,
        BEB,
        SUCCESS,
        ERROR
    }

    private int A; // Data packets arrive at the MAC layer following a Poisson process with an average arrival rate of A packets/second (variable)
    private int ticksPerSec; // Number of ticks in a second
    private double bitTime; // Number of ticks it takes to transmit a bit
    private int serviceTicks; // Number of ticks it takes to serve a packet
    private int nextArrivalTick; // The tick in which the next packet arrives
    private int nextServiceTick; // The tick in which the packet will be served again
    private int i; // Number of collisions the current packet has experience
    private int currentTick; // A tick number that get updated every tick
    private int ticksServed; // Number of ticks remaining in current transmitted packet
    private int K; // 512 bit-time
    private int mediumFreeCounter;
    private boolean persistent; // Whether running persistent CSMA/CD protocol
    private boolean mediumBusy; // Whether the LAN is busy, get updated every tick
    private State state;
    private ArrayDeque<Integer> queue; // An infinite queue containing the start tick of each packet

    // Public fields
    public ArrayList<Integer> outputList;
    public int collisionCounter;
    public int errorCounter;

    Computer(int A, int ticksPerSec, int W, int L, boolean persistent) {
        this.A = A;
        this.ticksPerSec = ticksPerSec;
        this.bitTime = (double) ticksPerSec / W;
        this.serviceTicks = (int)(L * bitTime);
        this.nextArrivalTick = 0;
        this.nextServiceTick = 0;
        this.i = 0;
        this.currentTick = 0;
        this.ticksServed = 0;
        this.K = (int) (512 * bitTime);
        this.mediumFreeCounter = 0;
        this.persistent = persistent;
        this.mediumBusy = false;
        this.queue = new ArrayDeque<>();

        // Public fields
        this.outputList = new ArrayList<>();
        this.collisionCounter = 0;
        this.errorCounter = 0;
        this.state = State.SENSE_MEDIUM;
    }

    public boolean tick(int currentTick, boolean mediumBusy) {
        this.currentTick = currentTick;
        this.mediumBusy = mediumBusy;
        if (currentTick == nextArrivalTick) {
            generatePacket();
        }
        if (currentTick == nextServiceTick) {
            if (!queue.isEmpty()) {
                return servePacket();
            }
            else {
                nextServiceTick++;
                return false;
            }
        }
        else {
            return false; // Not transmitting
        }
    }

    private void generatePacket() {
        queue.add(currentTick);
        nextArrivalTick += (int)( - ticksPerSec * Math.log(new Random().nextDouble()) / A);
    }

    private boolean servePacket() {
        switch (state) {
            case SENSE_MEDIUM:
                nextServiceTick = senseMedium();
                return false;
            case TRANSMIT:
                nextServiceTick = transmitFrameWhileDetectingCollision();
                return true;
            case SEND_JAMMING_BITS:
                nextServiceTick = sendJammingBits();
                // TODO: return true?
                return false;
            case BEB:
                nextServiceTick = binaryExponentialBackoff();
                return false;
            case ERROR:
                nextServiceTick = errorState();
                return false;
            case SUCCESS:
                nextServiceTick = successState();
                return false;
            default:
                return false;
        }
    }

    private int senseMedium() {
        if (mediumBusy) {
            mediumFreeCounter = 0;
            if (persistent) {
                return nextServiceTick+1; // wait is 0
            }
            else {
                // TODO: BEB?
                return nextServiceTick + new Random().nextInt(K) + 1;
            }
        }
        else { // Medium free
            if (mediumFreeCounter < 96 * bitTime) {
                // Keep sensing
                mediumFreeCounter++;
            }
            else { // 96 bit-time consecutive free
                mediumFreeCounter = 0;
                state = State.TRANSMIT;
            }
            return nextServiceTick+1;
        }
    }

    private int transmitFrameWhileDetectingCollision() {
        if (mediumBusy) { // Collision
            ticksServed = 0;
            collisionCounter++;
            state = State.SEND_JAMMING_BITS;
        }
        else {
            ticksServed++;
            if (ticksServed == serviceTicks) { // Success
                state = State.SUCCESS;
            }
        }
        return nextServiceTick+1;
    }

    private int sendJammingBits() {
        state = State.BEB;
        return nextServiceTick + (int)(48 * bitTime);
    }

    private int binaryExponentialBackoff() {
        i++;
        if (i > 10) {
            state = State.ERROR;
            return nextServiceTick + 1;
        }
        else {
            int R = new Random().nextInt((int)Math.pow(2, i));
            int Tb = R * K + 1;
            state = State.SENSE_MEDIUM;
            return nextServiceTick + Tb;
        }
    }

    private int errorState() {
        errorCounter++;
        queue.remove();
        ticksServed = 0;
        i = 0;
        state = State.SENSE_MEDIUM;
        return nextServiceTick+1;
    }

    private int successState() {
        outputList.add(currentTick - queue.remove());
        ticksServed = 0;
        i = 0;
        state = State.SENSE_MEDIUM;
        return nextServiceTick+1;
    }
}
