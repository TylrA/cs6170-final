//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by Fernflower decompiler)
//

package p1;

public class Interval implements Comparable<Interval> {
    private double start;
    private double duration;

    public Interval(double _start, double _duration) {
        this.start = _start;
        this.duration = _duration;
    }

    public double getStart() {
        return this.start;
    }

    public double getDuration() {
        return this.start;
    }

    public int compareTo(Interval arg0) {
        if (this.duration == arg0.duration) {
            return 0;
        } else {
            return this.duration <= arg0.duration && this.duration != -1.0D ? -1 : 1;
        }
    }

    public String toString() {
        return this.duration < 0.0D ? "[" + this.start + ", )" : "[" + this.start + "," + (this.start + this.duration) + ")";
    }
}
