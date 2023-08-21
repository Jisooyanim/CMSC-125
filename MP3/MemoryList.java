package CMSC_125.MP3;

import java.util.*;

public class MemoryList {
    boolean isFull;
    int processedJobsCount;
    int processInQueueCount;
    int totalWt;
    ArrayList<Memory> memoryList = new ArrayList<>();
    ArrayList<Job> completedJobs = new ArrayList<>();
    Queue<Job> jobInWaiting = new LinkedList<>();

    MemoryList() {
        ArrayList<Memory> memoryList = new ArrayList<>(); 

        memoryList.add(new Memory(1, 9500));
        memoryList.add(new Memory(2, 7000));
        memoryList.add(new Memory(3, 4500));
        memoryList.add(new Memory(4, 8500));
        memoryList.add(new Memory(5, 3000));
        memoryList.add(new Memory(6, 9000));
        memoryList.add(new Memory(7, 1000));
        memoryList.add(new Memory(8, 5500));
        memoryList.add(new Memory(9, 1500));
        memoryList.add(new Memory(10, 500));

        this.memoryList = memoryList;
        this.processedJobsCount = 0;
        this.processInQueueCount = 0;
        this.totalWt = 0;
        this.isFull = false;
    }

    void sortAsc() {
        this.memoryList.sort(new AscComparator());
    }

    void sortDesc() {
        this.memoryList.sort(new DescComparator());
    }

    boolean isFull() {
        for (Memory mem: this.memoryList) {
            if (mem.status.equals("FREE"))
                return false;
        }
        return true;
    }

    boolean isEmpty() {
        for (Memory mem: this.memoryList) {
            if (!mem.status.equals("FREE"))
                return false;
        }
        return true;
    }

    void displayMemOccu() {
        for (Memory mem: this.memoryList) {
            if (mem.job != null) 
                System.out.println(mem.id + ": " + mem.size + " | " + mem.job.id + ": " + mem.job.size);
            else
                System.out.println(mem.id + ": " + mem.size + " | " + "No job occupant");
        }
    }

    void allocate(JobList jobList) {
        for (Job job: jobList.jobList) {
            if (job.status.equals("FREE")) {
                if (!this.isFull()) {
                    for (Memory mem: this.memoryList) {
                        if (mem.status.equals("FREE")) {
                            if (job.size <= mem.size) {
                                mem.allocateJob(job);
                                job.canBeAllocated = false;
                                job.status = "ASSIGNED";
                                break;
                            }
                        }
                    }

                    if (job.canBeAllocated) {
                        this.totalWt++;
                        this.jobInWaiting.add(job);
                        this.processInQueueCount++;
                    }
                }
            }
        }
        
        this.isFull = true;
    }
}
