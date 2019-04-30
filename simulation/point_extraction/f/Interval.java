package f;

public class Interval implements Comparable<Interval> {
	private double start;
	private double duration;
	
	public Interval(double _start, double _duration) {
		start = _start;
		duration = _duration;
	}
	
	public double getStart() {
		return start;
	}

	public double getDuration() {
		return start;
	}

	@Override
	public int compareTo(Interval arg0) {
		if(this.duration == arg0.duration)
			return 0;
		if(this.duration > arg0.duration || this.duration == -1)
			return 1;
		
		return -1;
	}
	
	@Override
	public String toString() {
		if(duration < 0)
			return "[" + start + ", )";
		return "[" + start + "," + (start + duration) + ")";
	}
	
}
