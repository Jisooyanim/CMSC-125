package CMSC_125.MP3;

import java.util.*;

public class Memory {
    int id;
    int size;
    int jobCount;
    int unusedSpace;
    String status;
    Job job;
    ArrayList<Integer> freeSpace = new ArrayList<>();
    ArrayList<Integer> usedSpace = new ArrayList<>();

    Memory(int id, int size) {
        this.id = id;
        this.size = size;
        this.job = null;
        this.status = "FREE";
        this.jobCount = 0;
    }

    void allocateJob(Job job) {
        this.job = job;
        this.jobCount++;
        this.status = "OCCUPIED";
        this.usedSpace.add(job.size);
        this.freeSpace.add(this.size - job.size);
    }

    void deallocate() {
        this.job = null;
        this.status = "FREE";
    }

    int calculateUsedSpace() {
        Collections.sort(this.usedSpace);
        if(!this.usedSpace.isEmpty())
            return this.usedSpace.get(0);
        else    
            return -1;
    }

    void maxFreeSpace() {
        int t = this.calculateUsedSpace();
        if(t > 0)
            Collections.sort(this.freeSpace);
    }

    int calculateTotalIntFrag() {
        int sum = 0;
        for(int intFrag: this.freeSpace) {
            sum += intFrag;
        }
        return sum;
    }
}
