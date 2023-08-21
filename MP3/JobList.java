package CMSC_125.MP3;

import java.util.*;

public class JobList {
    ArrayList<Job> jobList = new ArrayList<>();

    JobList() {
        ArrayList<Job> jobList = new ArrayList<>();

        jobList.add(new Job(1, 5, 5760));
        jobList.add(new Job(2, 4, 4190));
        jobList.add(new Job(3, 8, 3290));
        jobList.add(new Job(4, 2, 2030));
        jobList.add(new Job(5, 2, 2550));
        jobList.add(new Job(6, 6, 6990));
        jobList.add(new Job(7, 8, 8940));
        jobList.add(new Job(8, 10, 740));
        jobList.add(new Job(9, 7, 3930));
        jobList.add(new Job(10, 6, 6890));
        jobList.add(new Job(11, 5, 6580));
        jobList.add(new Job(12, 8, 3820));
        jobList.add(new Job(13, 9, 9140));
        jobList.add(new Job(14, 10, 420));
        jobList.add(new Job(15, 10, 220));
        jobList.add(new Job(16, 7, 7540));
        jobList.add(new Job(17, 3, 3210));
        jobList.add(new Job(18, 1, 1380));
        jobList.add(new Job(19, 9, 9850));
        jobList.add(new Job(20, 3, 3610));
        jobList.add(new Job(21, 7, 7540));
        jobList.add(new Job(22, 2, 2710));
        jobList.add(new Job(23, 8, 8390));
        jobList.add(new Job(24, 5, 5950));
        jobList.add(new Job(25, 10, 760));

        this.jobList = jobList;
    }

    void displayJobs() {
		System.out.println("Job Stream #   |   Time   |   Job Size");
		System.out.println("--------------------------------------");
		for(int i = 0; i < jobList.size(); i++) {
			System.out.println("      " + ((Job)jobList.get(i)).id + "             " + 
				((Job)jobList.get(i)).burstTime + "           " + ((Job)jobList.get(i)).size);
		}  
    }

    ArrayList<Job> getJob() {
        return this.jobList;
    }

    void addWaitingTime() {
        for (Job job: this.jobList) {
            if (job.status.equals("ASSIGNED"))
                job.waitingTime++;
        }
    }

    boolean isDone() {
        for (Job job: this.jobList) {
            if (!job.status.equals("DONE"))
                return false;
        }
        return true;
    }
}
