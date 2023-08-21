package CMSC_125.MP3;

import java.text.DecimalFormat;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        JobList jobList = new JobList();
        MemoryList memoryList = new MemoryList();

        System.out.println("Choose Algorithm: [1] Worst-Fit [2] Best Fit [3] First-Fit");
        Scanner scanner= new Scanner(System.in);
        
        int fit = scanner.nextInt();

        if (fit == 1) {
            memoryList.sortDesc();
        } else if (fit == 2) {
            memoryList.sortAsc();
        } else if (fit > 3) {
            System.out.println("NICE CHOICE");
            scanner.close();
            return;
        }

        int time = 1;

        while (!jobList.isDone()) {
            if (!memoryList.isFull()) {
                if (memoryList.isEmpty() && time > 1)
                    break;
                memoryList.allocate(jobList);
            }

            run(memoryList, time);
            jobList.addWaitingTime();

            time++;
        }

        displayPerformance(memoryList, time, fit);
        scanner.close();
    }

    static void run(MemoryList memList, int time) {
        System.out.println("------------------------------ AT TIME t = " + time + " ------------------------------");
        System.out.println();

        for (Memory m: memList.memoryList) {
            if (m.job != null) {
                System.out.println("Job " + m.job.id + " has been allocated in memory block " + m.id + " and will reside for " + m.job.burstTime + " ms");
                m.job.burstTime--;
                memList.processedJobsCount++;

                if (m.job.burstTime == 0) {
                    m.job.status = "DONE";
                    memList.completedJobs.add(m.job);
                    m.deallocate();
                }
            } else {
                m.calculateUsedSpace();
                m.maxFreeSpace();
            }
        }

        System.out.println();
    }

    static void displayPerformance(MemoryList memList, int time, int fit) {
        int totalUnused, totalUsed, sumWT;

        totalUsed = totalUnused = sumWT = 0;

        DecimalFormat format = new DecimalFormat();
        format.setMaximumFractionDigits(2);
        
        for (Job job:memList.completedJobs) {
            sumWT += job.waitingTime;
        }

        for (Memory m:memList.memoryList) {
            if (m.usedSpace.size() > 0) 
                totalUsed += m.usedSpace.get(0);
            
            m.maxFreeSpace();
            if (m.freeSpace.size() > 0) {
                totalUnused += m.freeSpace.get(0);
            }
        }

        System.out.println();
        if (fit == 1)
            System.out.println("=============================== WORST-FIT ===============================");
        else if (fit == 2)
            System.out.println("=============================== BEST-FIT ===============================");
        else
            System.out.println("=============================== FIRST-FIT ===============================");

            System.out.println();
            System.out.println("AVERAGE THROUGHPUT: " + format.format(memList.processedJobsCount / (float)(time-1)) + " jobs per unit of time");
            System.out.println("AVERAGE WAITING QUEUE LENGTH: " + format.format(memList.processInQueueCount / (float) (time-1)) + " jobs per unit of time");
            System.out.println("AVERAGE WAITING TIME: " + format.format((float) sumWT/ (float)(memList.completedJobs.size())) + " unit of time");
    
            System.out.println();
            System.out.println("TOTAL UNUSED PARTITION: " + format.format(((float) totalUnused / 50000) * 100) + "% out of 50 000 memory capacity");
            System.out.println("TOTAL HEAVILY USED PARTITION: " + format.format(((float) totalUsed / 50000) * 100) + "% out of 50 000 memory capacity");
    
            System.out.println();
            System.out.println("------------------------ INTERNAL FRAGMENTATION ------------------------");
            System.out.println("Note: I.F. refers to free spaces in each allocation, where current job's size < block's size.");
            System.out.println();
        
        for (Memory m:memList.memoryList) {
            if (m.calculateTotalIntFrag() > 0) {
                System.out.println("Block " + m.id + "'s total internal fragmentation: " + m.calculateTotalIntFrag() + " units of memory");
                System.out.println("Block " + m.id + "'s average internal fragmentation: " + format.format((float) m.calculateTotalIntFrag() / (time-1)) + " units of memory");
                System.out.println();
            } else
                System.out.println("Block " + m.id + " was not allocated to any job.");        
        }
    }
}
