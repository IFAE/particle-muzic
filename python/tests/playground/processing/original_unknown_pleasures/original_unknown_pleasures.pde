float bg = 20;
float s = 255;

float xoff = 0;
float yoff = 100;

float u(float n) {
  return width/10 * n;
}

void setup() {
  size(1000,1000);
  //pixelDensity(displayDensity());
  background(bg);
  strokeWeight(20);
  stroke(s);
  smooth();
  
  
}

void draw() {
  background(bg);
  for(float y = height*0.1; y < height*0.9; y += u(1.5)) {
    pushMatrix();
    translate(0, y);
    noFill();
    beginShape();
    for(float x = width*0.1; x < width*0.9; x++) {
      float ypos = map(noise(x/500 + xoff, y/100 + yoff), 0, 1, -100, 100);
      float magnitude = x < width*0.5 ? map(x, width*0.1, width*0.5, 0, 1) : map(x, width*0.5, width*0.9, 1, 0) ;
      //ypos *= magnitude;
      ypos *= 1.5;
      if(ypos > 0) ypos = 0;
      vertex(x, ypos);
    }
    endShape();
    popMatrix();
  }
  //saveFrame("line-######.png");
  xoff += 0.01;
  yoff += -0.01;
}
