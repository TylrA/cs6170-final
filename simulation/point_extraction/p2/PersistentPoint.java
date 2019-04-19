//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by Fernflower decompiler)
//

package p2;

public class PersistentPoint {
    private double birth;
    private double lifespan;

    public PersistentPoint(double _birth, double _death) {
        this.birth = _birth;
        this.lifespan = _death - _birth;
    }
}
