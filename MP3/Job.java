package CMSC_125.MP3;

public class Job {
    int id;
    int size;
    int burstTime;
    int waitingTime;
    boolean canBeAllocated;
    String status;

    Job(int id, int burstTime, int size) {
        this.id = id;
        this.size = size;
        this.burstTime = burstTime;
        this.waitingTime = 0;
        this.canBeAllocated = (size < 9500);
        this.status = "FREE";
    }
}
