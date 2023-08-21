package CMSC_125.MP3;

import java.util.Comparator;

public class AscComparator implements Comparator<Memory> {
    @Override
    public int compare(Memory o1, Memory o2) {
        return Integer.compare(o1.size, o2.size);
    }
}
