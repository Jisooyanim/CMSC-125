package CMSC_125.MP3;

import java.util.Comparator;

public class DescComparator implements Comparator<Memory>{
    @Override
    public int compare(Memory o1, Memory o2) {
        if (o1.size == o2.size) {
            return 0;
        } else if (o1.size < o2.size) {
            return 1;
        } else {
            return -1;
        }
    }
}
