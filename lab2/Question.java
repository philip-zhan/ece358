import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

public class Question {
    public static void main(String[] args) {
        int[] N = {4, 6, 8, 10, 12, 14, 16};
        int[] A = {4, 6, 8, 10, 12, 14, 16};
        int W = 1000000;
        int L = 8000;

        int ticksPerSec = Integer.parseInt(args[0]);
        int totalSimulationTime = Integer.parseInt(args[1]);
        boolean persistent = Boolean.parseBoolean(args[2]);
        int trails = Integer.parseInt(args[3]);

        Path path = Paths.get("/Users/philipzhan/Google Drive/ECE 358L/2/log/" +
                ticksPerSec + "_" +
                totalSimulationTime + "_" +
                persistent + "_" +
                trails + "_" +
                LocalDateTime.now() +
                ".csv"
        );
        List<String> lines = new ArrayList<>();

        System.out.println("A\tN\tTPut(kbps)\tDelay(ms)\tErrors\tCollisions\tPacketsLeft");
        lines.add("A,N,TPut(kbps),Delay(ms),Errors,Collisions,PacketsLeft");

        for (int a : A) {
            for (int n : N) {
                double avgThroughput = 0;
                double avgDelay = 0;
                double avgCollisions = 0;
                double avgError = 0;
                double avgPacketsLeft = 0;
                for (int i = 0; i < trails; i++) {
                    LAN lan = new LAN(n, a, W, L, ticksPerSec, totalSimulationTime, persistent);
                    lan.simulate();
                    avgThroughput += (lan.totalThroughput - avgThroughput) / (i+1);
                    avgDelay += (lan.avgDelay - avgDelay) / (i+1);
                    avgCollisions += (lan.totalCollisions - avgCollisions) / (i+1);
                    avgError += (lan.totalErrors - avgError) / (i+1);
                }
                System.out.printf("%2d\t%2d\t%10.2f\t%9.2f\t%6.2f\t%10.2f\t%11.2f\n", a, n, avgThroughput, avgDelay,avgError, avgCollisions, avgPacketsLeft);
                lines.add(String.format(
                        "%2d,%2d,%10.2f,%9.2f,%6.2f,%10.2f,%11.2f", a, n, avgThroughput, avgDelay,avgError, avgCollisions, avgPacketsLeft));
            }
        }
        try {
            Files.write(path, lines);
        }
        catch (IOException e) {
            System.out.print("Error writing log file!");
        }
    }
}
