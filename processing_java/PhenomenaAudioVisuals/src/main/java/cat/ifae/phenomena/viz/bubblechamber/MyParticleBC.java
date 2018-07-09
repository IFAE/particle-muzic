package cat.ifae.phenomena.viz.bubblechamber;

import cat.ifae.phenomena.viz.MyParticle;
import cat.ifae.phenomena.viz.MyParticleData;
import cat.ifae.phenomena.viz.bubblechamber.display.MyTrack;
import cat.ifae.phenomena.viz.bubblechamber.dynamics.MyDynamics;
import processing.core.PApplet;
import processing.core.PVector;

public class MyParticleBC extends MyParticle {

    protected MyDynamics myDinamics;
    protected static float topVelocity = 20f;
    protected MyTrack myTrack;

    protected PVector acceleration;

    public MyParticleBC(PApplet p, PVector location, float theta, float beta, MyParticleData particleData) {
        super(p ,location,theta,beta,particleData);

        myDinamics = new MyDynamics(particleData);
        myTrack = new MyTrack(p, particleData);

    }

    public MyParticleBC(PApplet p, float theta, float beta, MyParticleData particleData) {
        super(p, theta,beta,particleData);
        this.location = new PVector(0f, (float) p.height / 2);

        myDinamics = new MyDynamics(particleData);
        myTrack = new MyTrack(p, particleData);
    }

    protected PVector setAcceleration(){
        return myDinamics.getAcceleration(velocity);
    }

    protected void update() {
        acceleration = setAcceleration();
        velocity.add(acceleration);
        PApplet.println(particleData.getName() + " Vel "+velocity);
        velocity.limit(topVelocity);
        location.add(velocity);
        PApplet.println(particleData.getName() + " Loc "+location);
    }

    protected void draw() {
        myTrack.drawDotTrack(location);
    }

    public void display(){
        update();
        draw();
    }

    @Override
    public PVector getLocation() {
        return location;

    }
}
