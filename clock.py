#!/usr/bin/env python3

from enum import Enum
from sys import argv
from os.path import realpath, dirname
from time import sleep, clock_getres, CLOCK_MONOTONIC
from site import addsitedir
addsitedir(dirname(realpath(argv[0])))

class Clock:
 class ClockMode(Enum):
  STEP = False
  RUN = True

 def __init__(self, mode=Clock.ClockMode.STEP):
  self.inputs = {}
  self.inputs['halt'] = False
  self.bus = ()
  self.state = {}
  self.state['Hz'] = 1
  self.state['time_since_last_tick'] = 0

 def subscribe(self,consumer):
  self.bus.append(consumer)

 def tick(self):
  while self.inputs['halt'] == False:
    for consumer in self.bus:
      consumer.pulse()
 
if __name__ == "__main__":
 clk = clock()
 
