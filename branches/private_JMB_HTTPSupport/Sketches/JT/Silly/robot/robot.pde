import noc.*;
import oscP5.*;
import netP5.*;
float leftVel, rightVel, angle, turnRate;
Vector3D pos, vel;
OscP5 osc;
NetAddress remoteLocation;

void setup() {
  size(200, 200);
  rectMode(CENTER);
  leftVel = 0;
  rightVel = 0;
  angle = 0;
  turnRate = 0.02;
  
  pos = new Vector3D(100, 100);
  vel = new Vector3D(0, 0);
  osc = new OscP5(this, 2000);
  remoteLocation = new NetAddress("127.0.0.1", 2000);
}
  
void draw() {
  background(0);
  if (pos.x < 0) {
    pos.setX(200);
  }
  if (pos.x > 200) {
    pos.setX(0);
  }
  if (pos.y < 0) {
    pos.setY(200);
  }
  if (pos.y > 200) {
    pos.setY(0);
  }

  vel = new Vector3D((leftVel + rightVel)*sin(angle),
                     (leftVel + rightVel)*cos(angle));
  pos.add(vel);
  angle = angle + ((leftVel - rightVel) * turnRate);
  fill(255);
  rect(pos.x, pos.y, 20, 20);  
}

void oscEvent(OscMessage message) {
  if (message.checkAddrPattern("/Jam/PianoRoll/On")) {
    if (message.get(0).floatValue() == 261.62558) {
      leftVel = message.get(1).floatValue();
    }
    if (message.get(0).floatValue() == 293.66476) {
      rightVel = message.get(1).floatValue();
    }
  }
  if (message.checkAddrPattern("/Jam/PianoRoll/Off")) {
    if (message.get(0).floatValue() == 261.62558) {
      leftVel = 0;
    }
    if (message.get(0).floatValue() == 293.66476) {
      rightVel = 0;
    }
  }
}
  
