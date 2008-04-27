import nxt.locator
import axon
from nxt.sensor import *

class KamaeliaNXT(Axon.Component.component):
   Inboxes = {"rmotor" : "control signals for the right motor",
              "lmotor" : "control signals for the left motor",
              }
   Outboxes = {"outbox" : "data collected from sensors",
              }
   def __init__(self, sock):
      self.rmotor = Motor(sock, PORT_B)
      self.lmotor = Motor(sock, PORT_C)
      self.light = LightSensor(b, PORT_3)
      self.sock = sock
      
   def stop(self):
      self.send(0, "rmotor")
      self.send(0, "lmotor")
      
   def main(self):
      while 1:
         self.send(light.get_sample()), "outbox")
         if self.dataReady("rmotor"):
            rmotor.power = self.recv("rmotor") # Right motor control
            rmotor.mode = MODE_MOTOR_ON
            rmotor.run_state = RUN_STATE_RUNNING
         if self.dataReady("lmotor"):
            lmotor.power = self.recv("lmotor") # Left motor control
            lmotor.mode = MODE_MOTOR_ON
            lmotor.run_state = RUN_STATE_RUNNING
         if TouchSensor(b, PORT_1).get_sample(): 
             self.stop()
             break
         yield 1
